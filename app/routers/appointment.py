from asyncio.log import logger
import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_db
from app.dependencies import get_service
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.search import VisitHistorySearchRequest
from app.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentCreateRequest
from app.schemas.appointment import AppointmentUpdateRequest
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)




@router.post("/history")
def search_patient_history(
    request: VisitHistorySearchRequest,
    service: AppointmentService = Depends(get_service),
    current_user=Depends(get_current_user)
):
    return service.search_patient_history(request)


@router.post("/appointments", status_code=201)
def create_appointment(
    request: AppointmentCreateRequest,
    service: AppointmentService = Depends(get_service),
    current_user=Depends(get_current_user)
):

    try:

        logger.info("Create Appointment API called.")

        response = service.create_appointment(request)

        logger.info("Appointment created successfully.")

        return response

    except Exception:

        logger.exception("Create Appointment API failed.")

        raise
    
@router.put("/appointments/{appointment_id}")
def update_appointment(
    appointment_id: int,
    request: AppointmentUpdateRequest,
    service: AppointmentService = Depends(get_service),
    current_user=Depends(get_current_user)
):

    try:

        logger.info(
            f"PUT /appointments/{appointment_id} called."
        )

        response = service.update_appointment(
            appointment_id,
            request
        )

        return response

    except Exception:

        logger.exception(
            f"Update Appointment API failed for Appointment ID : {appointment_id}"
        )

        raise