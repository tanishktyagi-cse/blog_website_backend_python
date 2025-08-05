from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class CommentModel(BaseModel):
    post_id: str
    author_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "author_id": self.author_id,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
