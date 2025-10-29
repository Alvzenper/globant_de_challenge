from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers.upload import router as upload_router
from app.routers.employee import router as employee_router
from app.routers.reports import router as reports_router
from app.routers.batch import router as batch_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Globant DE Challenge API")


@app.get("/")
def root():
    return {"message": "API up"}


app.include_router(upload_router)
app.include_router(employee_router)
app.include_router(reports_router)
app.include_router(batch_router)
