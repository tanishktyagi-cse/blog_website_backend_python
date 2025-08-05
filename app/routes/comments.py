from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from typing import List
from datetime import datetime

from app.db.mongodb import mongodb
from app.models.comments import CommentModel
from app.schemas.comments import CommentCreate, CommentResponse, CommentUpdate
from app.schemas.user import UserResponse
from app.security.hashing import get_current_user

router = APIRouter()


@router.post("/", response_model=CommentResponse)
async def create_comment(comment: CommentCreate, current_user: UserResponse = Depends(get_current_user)):
    comments_collection = mongodb.db["comments"]

    comment_data = CommentModel(
        post_id=comment.post_id,
        author_id=current_user.id,
        content=comment.content,
        created_at=datetime.utcnow()
    )
    result = await comments_collection.insert_one(comment_data.to_dict())

    comment_dict = comment_data.dict()
    comment_dict["id"] = str(result.inserted_id)
    return CommentResponse(**comment_dict)


@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def get_comments_for_post(post_id: str):
    comments_collection = mongodb.db["comments"]
    comments_cursor = comments_collection.find({"post_id": post_id})

    comments = []
    async for comment in comments_cursor:
        comment["id"] = str(comment["_id"])
        comments.append(CommentResponse(**comment))
    return comments


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(comment_id: str, updated_data: CommentUpdate, current_user: UserResponse = Depends(get_current_user)):
    comments_collection = mongodb.db["comments"]

    comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment["user_email"] != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    update_fields = {k: v for k, v in updated_data.dict().items() if v is not None}
    update_fields["updated_at"] = datetime.utcnow()

    await comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": update_fields})

    updated_comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
    updated_comment["id"] = str(updated_comment["_id"])
    return CommentResponse(**updated_comment)


@router.delete("/{comment_id}")
async def delete_comment(comment_id: str, current_user: UserResponse = Depends(get_current_user)):
    comments_collection = mongodb.db["comments"]

    comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment["user_email"] != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    await comments_collection.delete_one({"_id": ObjectId(comment_id)})
    return {"message": "Comment deleted successfully"}
