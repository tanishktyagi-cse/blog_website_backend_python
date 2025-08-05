from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content: str = Field(..., max_length=200)

class CommentCreate(CommentBase):
    post_id: str  # Reference to the MongoDB _id of the post

class CommentUpdate(CommentBase):
    content: Optional[str] = Field(None, max_length=200)

class CommentResponse(CommentBase):
    id: Optional[str] = Field(None, alias="_id")
    post_id: str
    author_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True