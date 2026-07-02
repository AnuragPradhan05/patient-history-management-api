import sqlite3
import time
from fastapi import FastAPI, Request
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.database.database import get_db, initialize_database
from app.routers.appointment import router as appointment_router
from app.utils.exceptions import (
    InvalidStatusExceptionForCreate,
    PatientNotFoundException,
    DoctorNotFoundException,
    InvalidAppointmentDateException,
    InvalidDateRangeException,
    InvalidStatusException,
    AppointmentNotFoundException,
    DiagnosisRequiredException,
    InvalidCredentialsException,
    UnauthorizedAccessException
)
from app.utils.logger import logger
from app.routers.auth import router as auth_router

app = FastAPI(
    title="Patient Visit History API"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    logger.info(
        f"Incoming Request -> {request.method} {request.url.path}"
    )

    response = await call_next(request)

    execution_time = round(time.time() - start_time, 4)

    logger.info(
        f"Completed Request -> {request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Execution Time: {execution_time} sec"
    )

    return response

@app.on_event("startup")
def startup():

    initialize_database()
    
    
    
    
@app.exception_handler(UnauthorizedAccessException)
async def unauthorized_access_exception_handler(
    request: Request,
    exc: UnauthorizedAccessException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=403,
        content={
            "success": False,
            "message": exc.message
        }
    )

@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_exception_handler(
    request: Request,
    exc: InvalidCredentialsException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": exc.message
        }
    )
    

@app.exception_handler(PatientNotFoundException)
async def patient_not_found_exception_handler(
    request: Request,
    exc: PatientNotFoundException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message
        }
    )


@app.exception_handler(InvalidDateRangeException)
async def invalid_date_range_exception_handler(
    request: Request,
    exc: InvalidDateRangeException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )

@app.exception_handler(InvalidStatusExceptionForCreate)
async def invalid_status_exception_handler(
    request: Request,
    exc: InvalidStatusExceptionForCreate
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )
@app.exception_handler(InvalidStatusException)
async def invalid_status_exception_handler(
    request: Request,
    exc: InvalidStatusException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )
    
    
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception("Unhandled exception occurred.")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )
    
@app.exception_handler(DoctorNotFoundException)
async def doctor_not_found_exception_handler(
    request: Request,
    exc: DoctorNotFoundException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message
        }
    )

@app.exception_handler(InvalidAppointmentDateException)
async def invalid_appointment_date_exception_handler(
    request: Request,
    exc: InvalidAppointmentDateException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )
    
@app.exception_handler(AppointmentNotFoundException)
async def appointment_not_found_handler(
    request: Request,
    exc: AppointmentNotFoundException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message
        }
    )
    
    
@app.exception_handler(DiagnosisRequiredException)
async def diagnosis_required_handler(
    request: Request,
    exc: DiagnosisRequiredException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )
    
    

app.include_router(appointment_router)
app.include_router(auth_router)

@app.get("/")
def home():

    logger.info("Home endpoint accessed.")

    return {
        "success": True,
        "message": "Patient Visit History API is Running"
    }


@app.get("/test")
def test(db: sqlite3.Connection = Depends(get_db)):

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM appointments")

    return {
        "total_appointments": cursor.fetchone()[0]
    }