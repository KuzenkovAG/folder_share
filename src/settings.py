import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


PORT = int(os.getenv("PORT"))
USERNAME = os.getenv("SERVER_USERNAME")
PASSWORD = os.getenv("SERVER_PASSWORD")

# путь к расшареной папке
SHARED_PATH = os.getenv("SHARED_PATH", ".")

BASE_PATH = os.getenv("BASE_PATH", "/internal/server_logs")

JWT_SECRET = os.getenv("JWT_SECRET")