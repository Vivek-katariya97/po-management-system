from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os

from .database import engine, Base
from .routes import vendors, products, purchase_orders
from .auth import create_access_token, verify_token

# Create tables in PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Purchase Order Management System")

# Allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protect modular routes with the JWT verify dependency
app.include_router(vendors.router, dependencies=[Depends(verify_token)])
app.include_router(products.router, dependencies=[Depends(verify_token)])
app.include_router(purchase_orders.router, dependencies=[Depends(verify_token)])

class LoginRequest(BaseModel):
    google_token: str

@app.post("/login")
async def login(request: LoginRequest):
    """
    Verifies the Google OAuth token with Google's API,
    then issues a backend JWT token.
    """
    # Accept a mock token for easier manual testing if Google Auth isn't fully set up yet
    if request.google_token == "mock-google-token":
        user_info = {"email": "test@example.com", "name": "Test User"}
    else:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={request.google_token}")
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid Google token")
            user_info = response.json()
            
    # Issue a secure JWT
    jwt_payload = {"sub": user_info.get("email", ""), "name": user_info.get("name", "")}
    jwt_token = create_access_token(data=jwt_payload)
    
    return {"access_token": jwt_token, "token_type": "bearer"}

class DescriptionRequest(BaseModel):
    product_name: str
    category: str

@app.post("/generate-description", dependencies=[Depends(verify_token)])
async def generate_description(request: DescriptionRequest):
    """
    Calls Gemini API to generate a marketing description for a product.
    Protected by JWT authentication.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        return {"description": f"Marketing text for {request.product_name} in {request.category} (Gemini API key not configured)."}
    
    prompt = f"Generate a professional 2 sentence marketing description for a product named {request.product_name} in the {request.category} category."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {"description": text.strip()}
            except (KeyError, IndexError):
                pass
                
    raise HTTPException(status_code=500, detail="Failed to communicate with AI service")
