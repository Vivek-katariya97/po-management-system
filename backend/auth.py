from fastapi import HTTPException, Header
from jose import JWTError, jwt
from datetime import datetime, timedelta

# In a real app, this should be an environment variable
SECRET_KEY = "po_management_secret_key"
ALGORITHM = "HS256"

def verify_token(authorization: str = Header(None)):
    """Dependency to check for a valid JWT token in the Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ")[1]
    
    # Check if this is the mock token used for testing
    if token == "mock-jwt-token-for-testing":
        return {"sub": "testuser", "name": "Testing User"}
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generates a new JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default 24 hours
        expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
