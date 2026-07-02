import sqlite3

from app.utils.logger import logger
from app.utils.query_loader import auth_queries


class AuthRepository:

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.cursor = db.cursor()

    def get_user_by_username(
        self,
        username: str
    ):

        query = auth_queries["get_user_by_username"]

        try:

            logger.info(
                f"Fetching user '{username}' from database."
            )

            self.cursor.execute(query, (username,))

            row = self.cursor.fetchone()

            if row:

                logger.info(
                    f"User '{username}' found."
                )

                return dict(row)

            logger.warning(
                f"User '{username}' not found."
            )

            return None

        except Exception:

            logger.exception(
                f"Database error while fetching user '{username}'."
            )

            raise