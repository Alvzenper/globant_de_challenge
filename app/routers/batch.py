# app/routers/batch.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from .. import models
from ..schemas import EmployeeBatchIn

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/batch")
def insert_employees_batch(payload: EmployeeBatchIn, db: Session = Depends(get_db)):
    # Preload valid FKs to avoid N queries
    dep_ids = {d.id for d in db.execute(select(models.Department)).scalars().all()}
    job_ids = {j.id for j in db.execute(select(models.Job)).scalars().all()}

    try:
        # Check duplicates in request
        ids_in_request = set()
        for e in payload.employees:
            if e.id in ids_in_request:
                raise HTTPException(status_code=400, detail=f"Duplicate id in request: {e.id}")
            ids_in_request.add(e.id)

        # Existing ids in DB
        existing = {
            x[0] for x in db.execute(
                select(models.Employee.id).where(models.Employee.id.in_(list(ids_in_request)))
            ).all()
        }
        if existing:
            raise HTTPException(status_code=400, detail=f"IDs already exist in DB: {sorted(existing)[:5]}{'...' if len(existing)>5 else ''}")

        # FK validation
        for e in payload.employees:
            if e.department_id not in dep_ids:
                raise HTTPException(status_code=400, detail=f"Unknown department_id: {e.department_id}")
            if e.job_id not in job_ids:
                raise HTTPException(status_code=400, detail=f"Unknown job_id: {e.job_id}")

        # Insert all in one transaction
        objs = [
            models.Employee(
                id=e.id,
                name=e.name.strip(),
                datetime=e.datetime,
                department_id=e.department_id,
                job_id=e.job_id,
            )
            for e in payload.employees
        ]
        db.add_all(objs)
        db.commit()
        return {"inserted": len(objs)}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Insert error: {e}")
