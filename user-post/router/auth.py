from fastapi import APIRouter, Depends, status, HTTPException, Response
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
from schema import UserLogin
import database
from oauth2 import create_access_token
from utils import verify

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):

    user = db.query(database.User).filter(database.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create token
    access_token = create_access_token(data={"user_id": user.id})

    return {'access_token': access_token, "token_type": "bearer"}