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

