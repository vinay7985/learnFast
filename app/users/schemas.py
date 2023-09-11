from pydantic import BaseModel
from typing import Optional
import datetime as _dt

class UserBase(BaseModel):
    
    email: str

class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes=True
class User(BaseModel):
    
    email: str

    id: int
    date_created: _dt.datetime

    class Config:
        from_attributes=True
class _PostBase(BaseModel):
    post_text: str

class PostCreate(_PostBase):
    pass

class Post(_PostBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
