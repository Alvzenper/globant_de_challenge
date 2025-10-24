from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/batch")
def insert_batch(payload: list[schemas.HiredEmployeeCreate],
                 db: Session = Depends(get_db)):
    n = len(payload)
    if n == 0 or n > 1000:
        raise HTTPException(status_code=400,
            detail="Batch size must be between 1 and 1000")

    objs = [models.HiredEmployee(**p.dict()) for p in payload]
    try:
        db.bulk_save_objects(objs)  
        db.commit()
        return {"inserted": n}
    except IntegrityError as e:
        db.rollback()
        
        raise HTTPException(status_code=409, detail="Integrity error") from e
