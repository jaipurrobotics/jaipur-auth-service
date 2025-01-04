from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    contact: Optional[str] = None
    company: str
    role: str  # "operator" or "manager"

class RegisterResponse(BaseModel):
    user_id: str
    message: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    user_id: str
    role: str
    message: str
