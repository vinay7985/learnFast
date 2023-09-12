
from fastapi.testclient import TestClient
from .database import engine,SessionLocal
from .app.Items import models
from .app.users import models
from .main import app
from fastapi import APIRouter
from typing import  Annotated
from fastapi import Depends
from .app.Items import models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()   


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)



client = TestClient(app)

def test_get_all_items(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    response = client.get("/items/")
    posts = db.query(models.Items).all()
    assert response.status_code == 200
    assert response.json() == {"data": posts, "token": token}
