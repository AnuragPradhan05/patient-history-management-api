from datetime import date

from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment import AppointmentCreateRequest
from app.schemas.search import VisitHistorySearchRequest
from app.utils.exceptions import InvalidAppointmentDateException, InvalidDateRangeException, InvalidStatusException, DoctorNotFoundException, InvalidStatusExceptionForCreate, PatientNotFoundException
from app.utils.logger import logger

from app.schemas.appointment import AppointmentUpdateRequest
from app.utils.exceptions import (
    AppointmentNotFoundException,
    DiagnosisRequiredException,
)


class AppointmentService:

    def __init__(self, repository: AppointmentRepository):
        self.repository = repository

    def search_patient_history(self, request: VisitHistorySearchRequest):

        logger.info(
            f"""
            Patient History Search Request
            Patient ID : {request.patient_id}
            Doctor ID : {request.doctor_id}
            Department : {request.department}
            Status : {request.status}
            Start Date : {request.start_date}
            End Date : {request.end_date}
            """
        )

        if (
            request.start_date
            and request.end_date
            and request.start_date > request.end_date
        ):
            logger.warning(
                f"Invalid date range for Patient ID : {request.patient_id}"
            )
            raise InvalidDateRangeException()
        
        allowed_status = {
            "scheduled",
            "confirmed",
            "completed",
            "cancelled"
        }

        if (
            request.status
            and request.status.lower() not in allowed_status
        ):
            logger.warning(
                f"Invalid status received: {request.status}"
            )
            raise InvalidStatusException(request.status)

        logger.info("Validation successful.")

        result = self.repository.search_patient_history(request)

        logger.info(
            f"Repository returned {len(result)} records."
        )

        if not result:
            logger.warning(
                f"No visit history found for Patient ID : {request.patient_id}"
            )

        logger.info("Patient history search completed successfully.")

        return result
    
    def create_appointment(self, request: AppointmentCreateRequest):

        logger.info(
            f"""
            Appointment Booking Request

            Patient ID : {request.patient_id}
            Doctor ID : {request.doctor_id}
            Appointment Date : {request.appointment_date}
            Appointment Time : {request.appointment_time}
            Status : {request.status}
            """
        )

        # Patient Validation
        if not self.repository.patient_exists(request.patient_id):
            logger.warning(
                f"Patient {request.patient_id} does not exist."
            )
            raise PatientNotFoundException(request.patient_id)

        
        # Doctor Validation
        if not self.repository.doctor_exists(request.doctor_id):
            logger.warning(
                f"Doctor {request.doctor_id} does not exist."
            )
            raise DoctorNotFoundException(request.doctor_id)
        
        
        #status Validation
        allowed_status = {
            "scheduled",
            "confirmed",
        }

        if request.status.lower() not in allowed_status:
            logger.warning(
                f"Invalid status : {request.status}"
            )
            raise InvalidStatusExceptionForCreate(request.status)
        
        
        # Date Validation
        if request.appointment_date < date.today():
            raise InvalidAppointmentDateException()

        appointment_id = self.repository.create_appointment(request)

        logger.info(
            f"Appointment booked successfully. Appointment ID : {appointment_id}"
        )

        return {
            "message": "Appointment booked successfully.",
            "appointment_id": appointment_id
        }
        
        
    def update_appointment(
        self,
        appointment_id: int,
        request: AppointmentUpdateRequest
    ):

        logger.info(
            f"""
            Appointment Update Request

            Appointment ID : {appointment_id}
            Status : {request.status}
            Diagnosis : {request.diagnosis}
            Notes : {request.notes}
            """
        )

        # Check Appointment Exists
        if not self.repository.appointment_exists(appointment_id):
            logger.warning(
                f"Appointment {appointment_id} does not exist."
            )
            raise AppointmentNotFoundException(appointment_id)

        # Validate Status
        allowed_status = {
            "scheduled",
            "confirmed",
            "completed",
            "cancelled"
        }
        if request.status.lower() not in allowed_status:
            logger.warning(
                f"Invalid status : {request.status}"
            )
            raise InvalidStatusException(request.status)

        # Diagnosis Required
        if (
            request.status.lower() == "completed"
            and not request.diagnosis
        ):
            logger.warning(
                "Diagnosis missing for completed appointment."
            )
            raise DiagnosisRequiredException()

        self.repository.update_appointment(
            appointment_id,
            request
        )

        logger.info(
            f"Appointment {appointment_id} updated successfully."
        )

        return {
            "message": "Appointment updated successfully.",
            "appointment_id": appointment_id
        }