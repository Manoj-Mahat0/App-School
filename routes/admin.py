from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import UserCreate, ClassCreate
from database import users_collection, class_collection
from bson import ObjectId
import bcrypt
from auth import verify_token

router = APIRouter()
security = HTTPBearer()

# ✅ Dependency to ensure only ADMIN can access
def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload or payload.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Access denied: Admins only")
    return payload

# ✅ Admin can create users
@router.post("/admin/create-user")
def create_user(user: UserCreate, admin: dict = Depends(get_current_admin)):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict["password"] = hashed_pw
    user_dict["_id"] = str(ObjectId())
    
    users_collection.insert_one(user_dict)
    return {"message": "User created successfully"}

# ✅ Admin can create class
@router.post("/admin/create-class")
def create_class(new_class: ClassCreate, admin: dict = Depends(get_current_admin)):
    if class_collection.find_one({"name": new_class.name}):
        raise HTTPException(status_code=400, detail="Class already exists")
    
    class_collection.insert_one({"name": new_class.name})
    return {"message": f"Class '{new_class.name}' created successfully"}

# ✅ Admin can view all classes
@router.get("/admin/all-classes")
def get_all_classes(admin: dict = Depends(get_current_admin)):
    classes = list(class_collection.find({}, {"_id": 0}))
    return {"classes": classes}
