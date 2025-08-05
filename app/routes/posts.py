# app/routes/posts.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserResponse
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.models.post import Post
from app.db.mongodb import mongodb
from app.security.hashing import get_current_user
from bson import ObjectId
from typing import List
from datetime import datetime

router = APIRouter()

# Create Post
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, current_user: UserResponse = Depends(get_current_user)):
    posts_collection = mongodb.db["posts"]

    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        author_id=str(current_user.email),  # using email as author_id for now
    )

    result = await posts_collection.insert_one(new_post.to_dict())
    new_post.id = str(result.inserted_id)
    return new_post.to_dict()

# Get All Posts
@router.get("/", response_model=List[PostResponse])
async def get_all_posts():
    posts_collection = mongodb.db["posts"]
    posts_cursor = posts_collection.find({})
    posts = []
    async for post in posts_cursor:
        post["id"] = str(post["_id"])
        post.pop("_id", None) 
        posts.append(PostResponse(**post))
    return posts

# Get Single Post by ID
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    posts_collection = mongodb.db["posts"]
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post["id"] = str(post["_id"])
    post.pop("_id", None) 
    return PostResponse(**post)

# Update Post
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: str, post_data: PostUpdate, current_user: UserResponse = Depends(get_current_user)):
    posts_collection = mongodb.db["posts"]
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post["author_id"] != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    update_data = {k: v for k, v in post_data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    await posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": update_data}
    )

    updated_post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    updated_post["id"] = str(updated_post["_id"])
    updated_post.pop("_id", None) 
    return PostResponse(**updated_post)

# Delete Post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, current_user: UserResponse = Depends(get_current_user)):
    posts_collection = mongodb.db["posts"]
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post["author_id"] != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    await posts_collection.delete_one({"_id": ObjectId(post_id)})
    return
