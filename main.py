from typing import Dict, List, Union, Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from database import engine,SessionLocal
from app.Items import  routers as items
from app.users import  routers as user
from app.Items import models
from app.users import models
models.Base.metadata.create_all(engine)

                  
app = FastAPI()


app.include_router(items.router)
app.include_router(user.router_users)

