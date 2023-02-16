from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
import psycopg2
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import *
from ..utils import *
from typing import Optional
from .. import oauth2
from sqlalchemy import func
import json
# from sqlalchemy.sql.functions import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# GET ALL POSTS
@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# GET ONE POST
@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        # cleaner version of status not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id, {id}, was not found")

    return post


# CREATE POSTS
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # print(type(new_post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# DELETE POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post_ = deleted_post.first()
    if post_ == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id, {id}, does not exist")

    if current_user.id == post_.owner_id:
        deleted_post.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorize to perform requested action")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE POST
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post_ = updated_post.first()
    if post_ == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id, {id}, does not exist")

    if current_user.id == post_.owner_id:
        updated_post.update(post.dict(), synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorize to perform requested action")

    db.commit()

    return updated_post.first()
