from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class AppointmentCreateRequest(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str = "scheduled"
    notes: Optional[str] = None


class AppointmentUpdateRequest(BaseModel):
    status: str 
    diagnosis: Optional[str] = None
    notes: Optional[str] = None