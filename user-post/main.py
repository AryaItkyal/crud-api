from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import List
from schema import Post, PostResponse, PostCreate, UserCreate, UserResponse
from random import randrange
import sqlite3
from sqlalchemy.orm import Session
import database
from database import engine, get_db
from router import post, user, auth


database.Base.metadata.create_all(bind=engine)

app = FastAPI()

## sql alchemy trials 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


## sql alchemy trials ^



