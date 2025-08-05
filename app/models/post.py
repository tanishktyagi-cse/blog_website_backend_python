from typing import Optional
from datetime import datetime

# Posts Model

class Post:
    def __init__(self, title: str, content: str, author_id: str):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.utcnow()
        self.updated_at = None
        self.id = None

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }