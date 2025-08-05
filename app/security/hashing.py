from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import UserResponse
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.db.mongodb import mongodb

# Setup for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

# This should match your router prefix + login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Function to get user from JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        username: str = payload.get("username")
        is_role: str = payload.get("is_role")

        if email is None or username is None or is_role is None:
            raise credentials_exception

        user_collection = mongodb.db["users"]
        user = await user_collection.find_one({"email": email})
        if user is None:
            raise credentials_exception

        return UserResponse(
            id=str(user["_id"]),
            email=email,
            username=username,
            is_role=is_role,
            is_active=True,
            created_at=datetime.utcnow()  # For now; replace with DB value if needed
        )

    except JWTError:
        raise credentials_exception
