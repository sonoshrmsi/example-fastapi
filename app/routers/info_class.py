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
    prefix="/classes",
    tags=['Info classes']
)


# Create a class for students
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=ClassResponse)
def create_class(class_info: ClassSchema, db: Session = Depends(get_db)):
# store the class in the database
    new_class = models.ClassInfo(**class_info.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


# Get all classes
@router.get("/", response_model=List[ClassResponse])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.ClassInfo).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Users does not exist")

    return users


# Get one class
@router.get("/{id}", response_model=ClassResponse)
def get_user(id: int ,db: Session = Depends(get_db)):
    class_ = db.query(models.ClassInfo).filter(models.ClassInfo.id == id).first()

    if not class_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Class does not exist")

    return class_