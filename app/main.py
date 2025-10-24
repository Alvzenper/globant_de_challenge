# app/main.py
from fastapi import FastAPI
from app.routers import reports
from .database import Base, engine
from .routers import upload, batch
from . import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Globant DE Challenge API")

@app.get("/")
def root():
    return {"message": "API up"}

# Routers
app.include_router(upload.router)
app.include_router(batch.router)
app = FastAPI()
app.include_router(reports.router)
