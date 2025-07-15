from passlib.context import CryptContext

# This is the "hashing engine" setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  Hash a plain-text password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#  Check if password matches hashed version
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
