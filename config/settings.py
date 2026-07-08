from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

if port is None:
    raise ValueError("DB_PORT is missing from .env")

DB_PORT = int(port)
