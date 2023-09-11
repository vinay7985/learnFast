from fastapi import APIRouter
from typing import Dict, List, Union, Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from database import engine,SessionLocal
from app.Items import models,schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.Items.schemas import  Login
from sqlalchemy.orm import Session
import app.Items.services as _services
import app.users.services as _services
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import jwt
from app.Items import services as _services
from app.users import services as _services
import app.users.schemas as schemas

router_users = APIRouter(prefix='/api', tags=["users"])
                  



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()   

_JWT_SECRET = 'JWT_SECRET'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router_users.post("/token" )
async def login( token: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    email= token.username
    password= token.password
    errors=[]
    try:
       user = await _services.get_user_by_email(email=email, db=db)

       if not user:
        errors.append('Email is not exist')
        return {'errors':errors}
    
       if not user.verify_password(password):
        errors.append('Password not found')
        return {'errors':errors}
       
       data={"sub":email}
       jwt_token= jwt.encode(data, _JWT_SECRET , algorithm="HS256")
       _services.create_token(user)
       msg="Login successfully"
       return { 'access_token':jwt_token, 'token_Type': 'bearer'}

    except:
        errors.append('something went wrong')
        return {'errors':errors}


@router_users.post("/api/users")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with that email already exists")

    user = await _services.create_user(user=user, db=db)

    return await _services.create_token(user=user)

