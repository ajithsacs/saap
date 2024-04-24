from fastapi import Depends, FastAPI
from database import SessionLocal, engine, Base, get_db
from . import models
from sqlalchemy.orm import Session   # Import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()




