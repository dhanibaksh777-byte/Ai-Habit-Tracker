from fastapi import FastAPI
from app.Routers import auth,habits,logs
from app.database import base 
from app import models
from app.database import engine

models.base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(logs.router)
app.include_router(auth.router)
app.include_router(habits.router)