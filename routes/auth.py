from fastapi import APIRouter, HTTPException
from models import UserLogin
from database import users_collection
from auth import create_access_token
import bcrypt

router = APIRouter()

@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({
        "email": db_user["email"],
        "role": db_user["role"]
    })
    
    return {
        "access_token": token,
    }
