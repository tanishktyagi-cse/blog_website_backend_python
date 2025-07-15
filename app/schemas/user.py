# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

#  Request schema for registering a new user
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=25)
    password: str = Field(..., min_length=8)

#  Request schema for logging in
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#  Response schema (what we return in APIs)
class UserResponse(BaseModel):
    email: EmailStr
    username: str
    is_role: str
    is_active: bool
    created_at: datetime

    class Config:               
        from_attributes = True
