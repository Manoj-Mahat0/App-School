from fastapi import FastAPI
from routes import admin, auth, verify
from database import users_collection
from bson import ObjectId
import bcrypt

app = FastAPI()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(verify.router)

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
