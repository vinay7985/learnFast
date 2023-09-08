from pydantic import BaseModel
from typing import Optional
import datetime as _dt

class Login(BaseModel):
    email: str
    password:str
    

class Items(BaseModel):
    name: str
    description:str
    tax:str

class UpdateItem(BaseModel):
    name: Optional[str]=None 
    description: Optional[str]=None 
    tax: Optional[str]=None 

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes=True
class User(BaseModel):
    username: str
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

    class Config:
       from_attributes=True