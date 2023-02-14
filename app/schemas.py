from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBased(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBased):
    pass


class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
# Response schema


class PostResponse(PostBased):
    created_at: datetime
    owner_id: int
    id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True
# User schema


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

# Class Schema


class ClassSchema(BaseModel):
    class_name: str
    teacher: str


class ClassResponse(BaseModel):
    class_name: str
    teacher: str
    created_at: datetime
    id: int

    class Config:
        orm_mode = True

# Login class


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
