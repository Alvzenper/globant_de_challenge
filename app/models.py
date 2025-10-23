from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from .database import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from .database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=False, unique=True)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=False, unique=True)

class Employee(Base):
    __tablename__ = "hired_employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)

    department = relationship("Department")
    job = relationship("Job")


Index("ix_employee_datetime", Employee.datetime)
Index("ix_employee_dept_job", Employee.department_id, Employee.job_id)