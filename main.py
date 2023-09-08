from typing import Dict, List, Union, Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from database import engine,SessionLocal
from app.Items import  routers


                  
app = FastAPI()


app.include_router(routers.router)

