from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from typing import List

app = FastAPI()

# Database 
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class User(UserCreate):
    id: int

class UserInDB(User):
    hashed_password: str

class PostCreate(BaseModel):
    title: str
    text: str

class Post(PostCreate):
    id: int
    author_id: int

# SQLAlchemy models
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)

class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(bind=engine)

# Password hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# new user
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict(), hashed_password=password_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# user by ID
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# new post
@app.post("/posts/", response_model=Post)
def create_post(post: PostCreate, current_user: User = Depends(read_user), db: Session = Depends(get_db)):
    db_post = PostModel(**post.dict(), author_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Delete a post (only admin)
@app.delete("/posts/{post_id}", response_model=dict)
def delete_post(post_id: int, current_user: User = Depends(read_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}

# list of all posts
@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    db_posts = db.query(PostModel).all()
    return db_posts
