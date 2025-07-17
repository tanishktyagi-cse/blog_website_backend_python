from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Request Schema for Posts

class PostBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: Optional[str] = Field(None, alias="_id")
    author_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True