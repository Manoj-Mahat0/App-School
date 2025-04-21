from fastapi import APIRouter, HTTPException
from models import UserCreate
from database import users_collection
from bson import ObjectId
import bcrypt

router = APIRouter()

@router.post("/admin/create-user")
def create_user(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict["password"] = hashed_pw
    user_dict["_id"] = str(ObjectId())
    
    users_collection.insert_one(user_dict)
    return {"message": "User created successfully"}
