class PatientNotFoundException(Exception):
    def __init__(self, patient_id: int):
        self.patient_id = patient_id
        self.message = f"Patient with ID {patient_id} not found."
        super().__init__(self.message)


class InvalidDateRangeException(Exception):
    def __init__(self):
        self.message = "Start date cannot be greater than end date."
        super().__init__(self.message)
        
        
class InvalidStatusException(Exception):
    def __init__(self, status: str):
        self.message = (
            f"Invalid status '{status}'. "
            f"Allowed values are: scheduled, confirmed, completed, cancelled."
        )
        super().__init__(self.message)
        
class InvalidStatusExceptionForCreate(Exception):
    def __init__(self, status: str):
        self.message = (
            f"Invalid status '{status}'. "
            f"Allowed values are: scheduled, confirmed."
        )
        super().__init__(self.message)
        
        
class DoctorNotFoundException(Exception):
    def __init__(self, doctor_id: int):
        self.message = f"Doctor with ID {doctor_id} not found."
        super().__init__(self.message)
        
        
class InvalidAppointmentDateException(Exception):
    def __init__(self):
        self.message = "Appointment date cannot be in the past."
        super().__init__(self.message)
        
        
class AppointmentNotFoundException(Exception):
    def __init__(self, appointment_id: int):
        self.message = f"Appointment with ID {appointment_id} not found."
        super().__init__(self.message)


class DiagnosisRequiredException(Exception):
    def __init__(self):
        self.message = "Diagnosis is required when appointment status is completed."
        super().__init__(self.message)
        
        
class InvalidCredentialsException(Exception):

    def __init__(self):

        self.message = "Invalid username or password."

        super().__init__(self.message)
        
        
class UnauthorizedAccessException(Exception):

    def __init__(self):
        self.message = "Only Admin can access this resource."
        super().__init__(self.message)