import sqlite3

from app.schemas.appointment import (
    AppointmentCreateRequest,
    AppointmentUpdateRequest,
)
from app.schemas.search import VisitHistorySearchRequest
from app.utils.logger import logger
from app.utils.query_loader import queries


class AppointmentRepository:

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.cursor = db.cursor()

    def get_patient_history(self, patient_id: int):

        query = queries["get_patient_history"]

        try:

            logger.info(
                f"Fetching complete visit history for Patient ID : {patient_id}"
            )

            self.cursor.execute(query, (patient_id,))

            rows = self.cursor.fetchall()

            logger.info(
                f"Visit history fetched successfully. Records Found : {len(rows)}"
            )

            return [dict(row) for row in rows]

        except Exception:

            logger.exception(
                f"Database error while fetching history for Patient ID : {patient_id}"
            )

            raise

    def search_patient_history(
        self,
        request: VisitHistorySearchRequest
    ):

        logger.info("Executing patient history search query.")

        params = []
        where_conditions = []

        filter_mapping = {
            "patient_id": "p.patient_id",
            "doctor_id": "d.doctor_id",
            "department": "d.department",
            "status": "a.status"
        }

        for field, column in filter_mapping.items():

            value = getattr(request, field)

            if value is not None:
                where_conditions.append(f"{column} = ?")
                params.append(value)

        
        where_conditions.append("a.appointment_date >= ?")
        params.append(request.start_date)

        where_conditions.append("a.appointment_date <= ?")
        params.append(request.end_date)

        query = queries["search_patient_history"].format(
            where_clause=" AND ".join(where_conditions)
        )

        try:

            logger.info(
                f"""
                Searching patient history

                Patient ID : {request.patient_id}
                Doctor ID : {request.doctor_id}
                Department : {request.department}
                Status : {request.status}
                Start Date : {request.start_date}
                End Date : {request.end_date}
                """
            )

            self.cursor.execute(query, tuple(params))

            rows = self.cursor.fetchall()

            logger.info(
                f"Patient history search completed successfully. Records Found : {len(rows)}"
            )

            return [dict(row) for row in rows]

        except Exception:

            logger.exception(
                f"Database error while searching history for Patient ID : {request.patient_id}"
            )

            raise

    def patient_exists(self, patient_id: int):

        query = queries["patient_exists"]

        self.cursor.execute(query, (patient_id,))

        return self.cursor.fetchone() is not None

    def doctor_exists(self, doctor_id: int):

        query = queries["doctor_exists"]

        self.cursor.execute(query, (doctor_id,))

        return self.cursor.fetchone() is not None

    def create_appointment(
        self,
        request: AppointmentCreateRequest
    ):

        query = queries["create_appointment"]

        values = (
            request.patient_id,
            request.doctor_id,
            str(request.appointment_date),
            str(request.appointment_time),
            request.status,
            request.notes,
        )

        try:

            logger.info(
                f"Creating appointment for Patient ID : {request.patient_id}"
            )

            self.cursor.execute(query, values)

            self.db.commit()

            logger.info(
                f"Appointment created successfully. Appointment ID : {self.cursor.lastrowid}"
            )

            return self.cursor.lastrowid

        except Exception:

            logger.exception(
                "Database error while creating appointment."
            )

            self.db.rollback()

            raise

    def appointment_exists(
        self,
        appointment_id: int
    ) -> bool:

        query = queries["appointment_exists"]

        try:

            self.cursor.execute(query, (appointment_id,))

            return self.cursor.fetchone() is not None

        except Exception:

            logger.exception(
                f"Database error while checking Appointment ID : {appointment_id}"
            )

            raise

    def update_appointment(
        self,
        appointment_id: int,
        request: AppointmentUpdateRequest
    ):

        try:

            fields = request.model_dump(exclude_unset=True)

            set_clause = ", ".join(
                f"{key}=?"
                for key in fields
            )

            query = queries["update_appointment"].format(
                set_clause=set_clause,
                where_clause="appointment_id=?"
            )

            values = list(fields.values()) + [appointment_id]

            logger.info(
                f"Updating Appointment ID : {appointment_id}"
            )

            self.cursor.execute(query, values)

            self.db.commit()

            logger.info(
                f"Appointment ID {appointment_id} updated successfully."
            )

        except Exception:

            logger.exception(
                f"Database error while updating Appointment ID : {appointment_id}"
            )

            self.db.rollback()

            raise