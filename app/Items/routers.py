from fastapi import APIRouter
from typing import Dict, List, Union, Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from database import engine,SessionLocal
# import models,schemas 
from app.Items import models,schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.Items.schemas import  Login
from sqlalchemy.orm import Session
import app.Items.services as _services
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import jwt

router = APIRouter(prefix='/api', tags=["Items"])
                  



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()   

_JWT_SECRET = 'JWT_SECRET'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# templates = Jinja2Templates(directory="templates")
# @app.get("/login", response_class=HTMLResponse )
# async def login_page(request: Request):
#     return templates.TemplateResponse('index.html', {'request': request})

@router.post("/token" )
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

@router.get("/items/")
def get_all_items(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    posts = db.query(models.Items).all()
    return {"data": posts, "token": token}

@router.get("/items/{id}")
def read_item(id: int,token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)):
   posts = db.query(models.Items).filter(models.Items.id ==id).first()
   
   return {"data": posts, "token": token}

@router.post("/items",response_model=schemas.Items)
def create_item(token: Annotated[str, Depends(oauth2_scheme)], item:schemas.Items, db:Session=Depends(get_db)):
    db_item=models.Items(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/item/{id}")
def delete_item(id: int,token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    item=db.query(models.Items).filter(models.Items.id==id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"item with id {id} not found")
    item.delete(synchronize_session=False)
    db.commit()
    return {"massage": "deleted successfully", "token": token}

@router.put("/item/{id}",response_model=schemas.Items)
def update_item(id: int, item:schemas.UpdateItem, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):

    try:
          item2=db.query(models.Items).filter(models.Items.id==id).first()
          for attr, value in item.dict().items():
              setattr(item2, attr, value)
          db.commit()
          db.refresh(item2)
          return item2
    except:
          return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"item with id {id} not found")    
    

@router.post("/api/users")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with that email already exists")

    user = await _services.create_user(user=user, db=db)

    return await _services.create_token(user=user)

# @app.post("/token")
# async def get_token(user: schemas.User, db : Session = Depends(get_db)):
#     data=jsonable_encoder(user)
#     if data['email']==models.User['email'] and data['password']==models.User['password']:
#      token=jwt.encode(data,_JWT_SECRET, algorithm='HS256')
#      return {'access_token':token}