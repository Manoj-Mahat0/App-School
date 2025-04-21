from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["STUDENT", "TEACHER", "PRINCIPAL", "LIBRARIAN", "PARENT"]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    email: EmailStr
    role: str
    name: Optional[str]
    message: str
