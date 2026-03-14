# Purchase Order Management System

A full-stack Purchase Order Management System built with Python FastAPI, PostgreSQL, and a responsive HTML/Bootstrap frontend. Features include Google OAuth authentication and an AI-powered product description generator using the Google Gemini API.

## Project Structure
```text
po-management-system/
 ├─ backend/
 │   ├─ main.py                # FastAPI app and OAuth/Gemini endpoints
 │   ├─ database.py            # PostgreSQL connection logic
 │   ├─ models.py              # SQLAlchemy DB models
 │   ├─ schemas.py             # Pydantic schemas for request/response validation
 │   ├─ auth.py                # JWT creation and dependency verification
 │   ├─ routes/                # Modular REST API endpoints
 │   └─ services/              # Business logic (e.g., PO tax calculations)
 ├─ frontend/
 │   ├─ index.html             # Dashboard viewing all POs
 │   ├─ create-po.html         # Form to create a PO with dynamic rows
 │   ├─ css/styles.css         # Glassmorphism aesthetic and custom styles
 │   └─ js/app.js              # Auth handling, API calls, and logic
 ├─ database/
 │   └─ schema.sql             # SQL script to create original tables
 └─ README.md                  # This documentation
```

## Setup Instructions

### 1. Database Setup
1. Ensure PostgreSQL is installed and running on your machine.
2. Create a new database named `po_db`.
3. You can either import the schema manually using the provided script:
   ```bash
   psql -U postgres -d po_db -f database/schema.sql
   ```
   *(Note: The backend is also configured to automatically create tables on first run using SQLAlchemy)*
4. If your Postgres username/password differs from `postgres:password`, update the `SQLALCHEMY_DATABASE_URL` string in `backend/database.py`.

### 2. Backend Setup
1. Open a terminal in the `po-management-system` folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```
3. Install required packages:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic httpx python-jose
   ```
4. Set your Gemini API key as an environment variable (Required for the Auto Description feature):
   ```bash
   # Windows Command Prompt
   set GEMINI_API_KEY="your_api_key_here"
   
   # Windows PowerShell
   $env:GEMINI_API_KEY="your_api_key_here"
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
   *The backend will start at `http://localhost:8000`*

### 3. Frontend Setup
1. The frontend utilizes vanilla HTML/JS and relies on external CDNs. Thus, you can execute it by simply running a local static server from the `po-management-system` root folder.
   ```bash
   python -m http.server 8080
   ```
2. Open `http://localhost:8080/frontend/index.html` in your browser.
3. **Authentication Details:**
   - In `frontend/js/app.js`, you can safely replace the placeholder `client_id` in `google.accounts.id.initialize` if you wish to set up real Google Identity Services.
   - For rapid testing without GCP configuration, click the **"Bypass Login (Test Mode)"** button on the sign-in screen to receive a functional mock session and navigate the app instantly.

## API Examples (cURL)
*Run these commands after your backend server is active to seed some base data.*

**1. Create a Vendor:**
```bash
curl -X POST "http://localhost:8000/vendors" -H "Content-Type: application/json" -H "Authorization: Bearer mock-jwt-token-for-testing" -d "{\\"name\\":\\"Acme Corp\\",\\"contact\\":\\"contact@acmecorp.com\\",\\"rating\\":4.5}"
```

**2. Create a Product:**
```bash
curl -X POST "http://localhost:8000/products" -H "Content-Type: application/json" -H "Authorization: Bearer mock-jwt-token-for-testing" -d "{\\"name\\":\\"Wireless Mouse\\",\\"sku\\":\\"M-001\\",\\"unit_price\\":25.50,\\"stock_level\\":100,\\"category\\":\\"Electronics\\"}"
```

**3. Generate AI Description (Optional test):**
```bash
curl -X POST "http://localhost:8000/generate-description" -H "Content-Type: application/json" -H "Authorization: Bearer mock-jwt-token-for-testing" -d "{\\"product_name\\":\\"Wireless Mouse\\",\\"category\\":\\"Electronics\\"}"
```
