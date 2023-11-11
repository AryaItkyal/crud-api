from schema import Post, PostResponse, PostCreate
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from database import engine, get_db
import database
from oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(database.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    # new_post = database.Post(title = post.title, content = post.content,
    #               published = post.published)
    
    new_post = database.Post(user_id=current_user.id, **post.dict()) # unpacks the dictionary in the above format

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    post = db.query(database.Post).filter(database.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    return post

@router.delete("/{id}")
def del_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    post_query = db.query(database.Post).filter(database.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")


    post_query.delete(synchronize_session=False)
    db.commit()

    return {'message': 'post was successfully deleted!'}

@router.put("/{id}")
def update_post(id: int, post: PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    post_query = db.query(database.Post).filter(database.Post.id == id)
    
    post = post_query.first()
    # ind = find_post_index(id)
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"message": 'Post updated!'}