from pydantic import BaseModel
from typing import Optional
from datetime import date


class VisitHistorySearchRequest(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    department: Optional[str] = None
    status: Optional[str] = None
    start_date: date
    end_date: date