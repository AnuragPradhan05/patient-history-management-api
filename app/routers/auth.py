import sqlite3

from fastapi import APIRouter, Depends

from app.database.database import get_db
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_auth_repository(
    db: sqlite3.Connection = Depends(get_db)
):
    return AuthRepository(db)


def get_auth_service(
    repository: AuthRepository = Depends(get_auth_repository)
):
    return AuthService(repository)


@router.post("/login")
def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    return service.login(request)