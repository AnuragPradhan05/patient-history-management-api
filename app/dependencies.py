import sqlite3

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt_handler import verify_access_token
from app.database.database import get_db
from app.repositories.appointment_repository import AppointmentRepository
from app.services.appointment_service import AppointmentService
from app.utils.exceptions import InvalidCredentialsException, UnauthorizedAccessException


security = HTTPBearer()


def get_repository(
    db: sqlite3.Connection = Depends(get_db)
):
    return AppointmentRepository(db)


def get_service(
    repository: AppointmentRepository = Depends(get_repository)
):
    return AppointmentService(repository)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise InvalidCredentialsException()

    if payload["role"] != "ADMIN":
        raise UnauthorizedAccessException()

    return payload