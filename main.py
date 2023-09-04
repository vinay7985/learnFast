from typing import Dict, List, Union
from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from database import engine,SessionLocal
import models,schemas
from models import Items
from schemas import  Items
from sqlalchemy.orm import Session
import services as _services
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()   


models.Base.metadata.create_all(engine)




@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html",  {"request": request})



@app.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    posts = db.query(models.Items).all()
    return {"data": posts}

@app.get("/items/{id}")
def read_item(id: int,db: Session = Depends(get_db)):
   posts = db.query(models.Items).filter(models.Items.id ==id).first()
   
   return {"data": posts}

@app.post("/items",response_model=schemas.Items)
def create_item(item:schemas.Items, db:Session=Depends(get_db)):
    db_item=models.Items(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/item/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    item=db.query(models.Items).filter(models.Items.id==id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"item with id {id} not found")
    item.delete(synchronize_session=False)
    db.commit()
    return {"massage": "deleted successfully"}

@app.put("/item/{id}",response_model=schemas.Items)
def update_item(id: int, item:schemas.UpdateItem, db: Session = Depends(get_db)):

    try:
          item2=db.query(models.Items).filter(models.Items.id==id).first()
          for attr, value in item.dict().items():
              setattr(item2, attr, value)
          db.commit()
          db.refresh(item2)
          return item2
    except:
          return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"item with id {id} not found")    
    

@app.post("/api/users")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with that email already exists")

    user = await _services.create_user(user=user, db=db)

    return await _services.create_token(user=user)
