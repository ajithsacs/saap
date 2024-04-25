from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import Base, engine
import app.student_assessment.api as api
from app.login.api import loginroute

app = FastAPI()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(api.router)
app.include_router(loginroute)
