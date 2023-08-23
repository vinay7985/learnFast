from pydantic import BaseModel
data = []
class Items(BaseModel):
    name: str
    description:str
    tax:str

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
