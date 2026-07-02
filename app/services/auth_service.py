from app.auth.jwt_handler import create_access_token
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import LoginRequest
from app.utils.exceptions import InvalidCredentialsException
from app.utils.logger import logger
from app.auth.password import verify_password


class AuthService:

    def __init__(
        self,
        repository: AuthRepository
    ):
        self.repository = repository

    def login(
        self,
        request: LoginRequest
    ):

        logger.info(
            f"Login attempt for username : {request.username}"
        )

        user = self.repository.get_user_by_username(
            request.username
        )

        if user is None:

            logger.warning(
                f"User '{request.username}' not found."
            )

            raise InvalidCredentialsException()

        if not verify_password(
                request.password,
                user["password"]
            ):

            logger.warning(
                f"Incorrect password for user '{request.username}'."
            )

            raise InvalidCredentialsException()

        token = create_access_token(
            {
                "sub": user["username"],
                "role": user["role"]
            }
        )

        logger.info(
            f"JWT generated successfully for '{request.username}'."
        )

        return {
            "access_token": token,
            "token_type": "Bearer"
        }