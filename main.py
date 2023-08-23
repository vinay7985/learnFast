from typing import Dict, List
from fastapi import FastAPI, Request, Depends, HTTPException, status
from database import engine,SessionLocal
import models,schemas
from models import Items
from schemas import  Items
from sqlalchemy.orm import Session

app = FastAPI()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()   



models.Base.metadata.create_all(engine)

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
def update_item(id: int, name:str,description:str, tax:str,db: Session = Depends(get_db)):

    try:
          item=db.query(models.Items).filter(models.Items.id==id).first()
          item.name =name
          item.description = description
          item.tax = tax
          db.add(item)
          db.commit()
          return item
    except:
          return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"item with id {id} not found")
    


   