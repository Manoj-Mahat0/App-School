from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal[
        "ADMIN", "STUDENT", "TEACHER", "PRINCIPAL", "LIBRARIAN", "PARENT"
    ]  # ✅ Added "ADMIN"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    email: EmailStr
    role: Literal[
        "ADMIN", "STUDENT", "TEACHER", "PRINCIPAL", "LIBRARIAN", "PARENT"
    ]  # ✅ Also here
    name: Optional[str]
    message: str

class ClassCreate(BaseModel):
    name: str  # e.g., "10A", "6B"
