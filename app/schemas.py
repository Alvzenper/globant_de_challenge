from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, field_validator


class EmployeeIn(BaseModel):
    id: int = Field(..., ge=0)
    name: str = Field(..., min_length=1)
    datetime: datetime
    department_id: int = Field(..., ge=0)
    job_id: int = Field(..., ge=0)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("name cannot be blank")
        return s


class EmployeeBatchIn(BaseModel):
    employees: list[EmployeeIn]

    @field_validator("employees")
    @classmethod
    def check_batch_size(cls, v):
        if not (1 <= len(v) <= 1000):
            raise ValueError("batch size must be between 1 and 1000")
        return v


class HiredEmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

    @field_validator("datetime", mode="before")
    @classmethod
    def coerce_datetime(cls, v: Any) -> datetime:
        if isinstance(v, datetime):
            return v
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v, tz=timezone.utc).replace(tzinfo=None)
        if isinstance(v, str):
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(v, fmt)
                except ValueError:
                    pass

            try:
                from dateutil import parser

                return parser.parse(v)
            except Exception:
                pass
        raise ValueError(
            "datetime debe ser ISO8601 (p.ej. '2021-05-10T10:00:00') o un datetime de Python"
        )
