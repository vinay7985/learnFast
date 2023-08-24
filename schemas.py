from pydantic import BaseModel
from typing import Optional

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
    id: int
    is_active: bool

    class Config:
        orm_mode = True
