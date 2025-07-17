from fastapi import FastAPI
from app.routes import auth, posts
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Connect to MongoDB at startup
    await connect_to_mongo()
    yield
    # ✅ Close MongoDB at shutdown
    await close_mongo_connection()

# Create FastAPI app with the lifespan manager
app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])