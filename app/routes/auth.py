from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.models.user import User
from app.security.hashing import hash_password, verify_password, create_access_token
from app.db.mongodb import mongodb  # use existing DB connection
from app.schemas.tokens import TokenResponse

router = APIRouter()

# User Register Route
@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    # Using it inside because outside it wont be able to call DB Collection because it is still NONE.(MongoDB is NONE not connected)
    users_collection = mongodb.db["users"]
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pw
    )

    await users_collection.insert_one(new_user.to_dict())

    return UserResponse(
        email=new_user.email,
        username=new_user.username,
        is_role=new_user.is_role,
        is_active=new_user.is_active,
        created_at=new_user.created_at
    )

# User Login Route
@router.post("/login", response_model=TokenResponse)
async def login_user(user_data: UserLogin):
    users_collection = mongodb.db["users"]
    user = await users_collection.find_one({"email": user_data.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token = create_access_token({
        "sub": user["email"],
        "username": user["username"],
        "is_role": user["is_role"]
    })
    
    return TokenResponse(access_token=access_token, token_type="bearer")
