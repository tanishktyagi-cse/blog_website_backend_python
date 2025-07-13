# app/db/mongodb.py

from pymongo.mongo_client import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongodb = MongoDB()

async def connect_to_mongo():
    uri = f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}?authSource={settings.MONGO_USERNAME}"
    mongodb.client = AsyncIOMotorClient(uri)
    mongodb.db = mongodb.client[settings.MONGO_DB_NAME]

async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
