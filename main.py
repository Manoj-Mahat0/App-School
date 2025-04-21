from fastapi import FastAPI, Request
from routes import admin, auth, verify
from database import users_collection
from bson import ObjectId
import bcrypt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS middleware for frontend access (like React, Vue, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify frontend domain like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Example logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"🔄 {request.method} {request.url}")
    response = await call_next(request)
    print(f"✅ Response status: {response.status_code}")
    return response

# ✅ Route registration
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(verify.router)

# ✅ Default admin creation
@app.on_event("startup")
def create_default_admin():
    default_email = "admin@example.com"
    default_password = "admin123"

    if not users_collection.find_one({"email": default_email}):
        hashed_pw = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
        users_collection.insert_one({
            "_id": str(ObjectId()),
            "name": "Admin",
            "email": default_email,
            "password": hashed_pw,
            "role": "ADMIN"
        })
        print("✅ Default admin created.")
    else:
        print("ℹ️ Default admin already exists.")
