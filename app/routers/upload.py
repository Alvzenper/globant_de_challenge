
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd
from datetime import datetime

from ..database import get_db
from .. import models

router = APIRouter(prefix="/upload", tags=["upload"])

def _read_csv(file: UploadFile, expected_cols: list[str]) -> pd.DataFrame:
    try:
        df = pd.read_csv(file.file, header=None, names=expected_cols)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {e}")
    if set(df.columns) != set(expected_cols):
        raise HTTPException(status_code=400, detail=f"CSV must have columns {expected_cols} (no header)")
    return df

@router.post("/departments")
def upload_departments(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = _read_csv(file, ["id", "department"])
    inserted, skipped = 0, 0
    try:
        for _, row in df.iterrows():
            if pd.isna(row["id"]) or pd.isna(row["department"]):
                skipped += 1
                continue
            exists = db.execute(select(models.Department).where(models.Department.id == int(row["id"]))).scalar_one_or_none()
            if exists:
                skipped += 1
                continue
            db.add(models.Department(id=int(row["id"]), department=str(row["department"]).strip()))
            inserted += 1
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Insert error: {e}")
    return {"inserted": inserted, "skipped": skipped}

@router.post("/jobs")
def upload_jobs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = _read_csv(file, ["id", "job"])
    inserted, skipped = 0, 0
    try:
        for _, row in df.iterrows():
            if pd.isna(row["id"]) or pd.isna(row["job"]):
                skipped += 1
                continue
            exists = db.execute(select(models.Job).where(models.Job.id == int(row["id"]))).scalar_one_or_none()
            if exists:
                skipped += 1
                continue
            db.add(models.Job(id=int(row["id"]), job=str(row["job"]).strip()))
            inserted += 1
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Insert error: {e}")
    return {"inserted": inserted, "skipped": skipped}

@router.post("/hired_employees")
def upload_hired_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = _read_csv(file, ["id", "name", "datetime", "department_id", "job_id"])
    inserted, skipped, fk_errors = 0, 0, 0

    # Parse types
    def parse_dt(x):
        try:
            return pd.to_datetime(x, utc=False, format=None)
        except Exception:
            return pd.NaT

    df["name"] = df["name"].astype(str).str.strip()
    df["datetime"] = df["datetime"].apply(parse_dt)

    try:
        for _, r in df.iterrows():
            # Minimal validation
            if pd.isna(r["id"]) or not r["name"] or pd.isna(r["datetime"]) or pd.isna(r["department_id"]) or pd.isna(r["job_id"]):
                skipped += 1
                continue

            # FK check
            dep = db.execute(select(models.Department.id).where(models.Department.id == int(r["department_id"]))).scalar_one_or_none()
            job = db.execute(select(models.Job.id).where(models.Job.id == int(r["job_id"]))).scalar_one_or_none()
            if dep is None or job is None:
                fk_errors += 1
                continue

            exists = db.execute(select(models.Employee).where(models.Employee.id == int(r["id"]))).scalar_one_or_none()
            if exists:
                skipped += 1
                continue

            db.add(models.Employee(
                id=int(r["id"]),
                name=r["name"],
                datetime=pd.to_datetime(r["datetime"]).to_pydatetime(),
                department_id=int(r["department_id"]),
                job_id=int(r["job_id"]),
            ))
            inserted += 1

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Insert error: {e}")

    return {"inserted": inserted, "skipped": skipped, "fk_errors": fk_errors}
