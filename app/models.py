from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from sqlalchemy.orm import validates

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=False, unique=True)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=False, unique=True)

class HiredEmployee(Base):  
    __tablename__ = "hired_employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    datetime = Column(DateTime, nullable=False) 
    department_id = Column(Integer, ForeignKey("departments.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    @validates("datetime")
    def _coerce_datetime(self, key, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                pass
            try:
                from dateutil import parser
                return parser.parse(value)
            except Exception:
                pass
        return value

Index("ix_employee_datetime", HiredEmployee.datetime)
Index("ix_employee_dept_job", HiredEmployee.department_id, HiredEmployee.job_id)