from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ScanOut(BaseModel):
    id: int
    user_id: int
    image_path: str
    heatmap_path: str
    prediction: str
    confidence: float
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True
