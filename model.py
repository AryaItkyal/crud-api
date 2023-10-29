from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    # id: int
    title: str
    user: str
    img_link: Optional[str] = None

class Post(PostCreate):
    id: int
    