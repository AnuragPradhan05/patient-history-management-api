import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SCHEMA_FILE = os.path.join(BASE_DIR, "01_schema.sql")
SEED_FILE = os.path.join(BASE_DIR, "02_seed_data.sql")
DATABASE_NAME = os.path.join(BASE_DIR, "patient_visit_history.db")



def get_db():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
    finally:
        connection.close()


def initialize_database():
    
    if os.path.exists(DATABASE_NAME):
        print("Database already exists.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    with open(SCHEMA_FILE, "r") as file:
        cursor.executescript(file.read())

    with open(SEED_FILE, "r") as file:
        cursor.executescript(file.read())

    connection.commit()
    connection.close()

    print("Database initialized successfully.")