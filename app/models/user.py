# app/models/user.py

from typing import Optional
from datetime import datetime

class User:
    def __init__(
        self,
        email: str,
        username: str,
        hashed_password: str,
        is_role: str = "user",  # "user" or "superadmin"
        is_active: bool = True,
        created_at: Optional[datetime] = None,
    ):
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.is_role = is_role
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "is_role": self.is_role,
            "is_active": self.is_active,
            "created_at": self.created_at,
        }
