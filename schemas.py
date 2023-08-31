from pydantic import BaseModel
from typing import Optional
import datetime as _dt

class Items(BaseModel):
    name: str
    description:str
    tax:str

class UpdateItem(BaseModel):
    name: Optional[str]=None 
    description: Optional[str]=None 
    tax: Optional[str]=None 

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):

   

    class Config:
        orm_mode = True
