from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# title: str, content: str, Bool: published/draft(true/false)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(Post):
    pass

class PostResponse(Post): # schema of output
    id: int
    created_at: datetime
    user_id: int


    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
