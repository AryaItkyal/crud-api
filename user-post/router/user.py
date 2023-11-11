from schema import UserCreate, UserResponse
from fastapi import status, HTTPException, Depends, APIRouter 
from typing import List
from utils import hash
from sqlalchemy.orm import Session
import database
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = database.User(**user.dict()) # unpacks the dictionary in the above format

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(database.User).filter(database.User.id == id).first() 

    if user == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} not found")
    
    return user

@router.delete("/{id}")
def del_user(id: int, db: Session = Depends(get_db)):

    user = db.query(database.User).filter(database.User.id == id).first() 

    if user == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} not found")
    
    db.delete(user)

    db.commit()

    return {'message': 'user was successfully deleted!'}


