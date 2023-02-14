from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
import time
from .. import models
from ..database import engine, get_db
from ..schemas import *
from ..utils import *

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# Create a new post 
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # Hass the password
    hashed_password = hash(user.password)
    user.password = hashed_password
    
    # store the user in the database

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user    

# Get a user
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id, {id}, does not exist")

    return user

# Get all users
@router.get("/", response_model=List[UserResponse])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Users does not exist")

    return users