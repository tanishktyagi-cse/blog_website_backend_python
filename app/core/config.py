from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
