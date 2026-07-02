import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPOINTMENT_QUERY_FILE = os.path.join(
    BASE_DIR,
    "queries",
    "appointment.yaml"
)

AUTH_QUERY_FILE = os.path.join(
    BASE_DIR,
    "queries",
    "auth.yaml"
)

with open(APPOINTMENT_QUERY_FILE, "r") as file:
    queries = yaml.safe_load(file)

with open(AUTH_QUERY_FILE, "r") as file:
    auth_queries = yaml.safe_load(file)