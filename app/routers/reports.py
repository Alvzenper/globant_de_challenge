from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/reports", tags=["reports"])

quarter_2021 = text("""
with  
J as (select * from jobs j ) ,
H as (select *,  
             strftime('%Y', substr(datetime, 1, 19)) AS year, 
             CAST(strftime('%m', substr(datetime, 1, 19)) AS INTEGER) AS month from hired_employees),
D as (select * from departments)
select 
D.department, J.job,
case when H.month BETWEEN 1 AND 3 then 1 else 0 end as Q1, 
case when H.month BETWEEN 4 AND 6 then 1 else 0 end as Q2 , 
case when H.month BETWEEN 7 AND 9 then 1 else 0 end as Q3, 
case when H.month BETWEEN 10 AND 12 then 1 else 0 end as Q4 
from H
join J on J.id = H.job_id
join D on D.id = H.department_id
WHERE H.year = '2021'
group by D.department, J.job
order by D.department, J.job
 """)

depts_above_mean = text("""
 WITH hires_per_department AS (
    SELECT 
        department_id, 
        COUNT(*) AS hires
    FROM hired_employees
    WHERE strftime('%Y', substr(datetime, 1, 19)) = '2021'
    GROUP BY department_id
)
SELECT 
    d.id, 
    d.department, 
    h.hires
FROM hires_per_department h
JOIN departments d ON d.id = h.department_id
WHERE h.hires > (SELECT AVG(hires) FROM hires_per_department)
ORDER BY h.hires DESC;

 """)

@router.get("/hired-by-quarter-2021")
def hired_by_quarter(db: Session = Depends(get_db)):
    rows = db.execute(quarter_2021).mappings().all()
    return [dict(r) for r in rows]

@router.get("/departments-above-mean-2021")
def departments_above_mean(db: Session = Depends(get_db)):
    rows = db.execute(depts_above_mean).mappings().all()
    return [dict(r) for r in rows]