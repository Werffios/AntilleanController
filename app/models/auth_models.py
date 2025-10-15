from pydantic import BaseModel
from app.models.user_models import UserResponse

class RegisterRequest(BaseModel):
    name: str
    email_encrypted: str
    password_encrypted: str

class LoginRequest(BaseModel):
    email_encrypted: str
    password_encrypted: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

