from fastapi import APIRouter, Header, HTTPException
from auth import verify_token
from models import TokenPayload
from database import users_collection

router = APIRouter()

@router.get("/verify-token", response_model=TokenPayload)
def verify_user_token(Authorization: str = Header(...)):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid token format. Use Bearer <token>")
    
    token = Authorization.split(" ")[1]
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = users_collection.find_one({"email": payload.get("email")})
    
    return {
        "email": payload.get("email"),
        "role": payload.get("role"),
        "name": user.get("name") if user else None,
        "message": "Token is valid"
    }
