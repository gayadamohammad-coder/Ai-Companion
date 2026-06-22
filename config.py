import os
from dotenv import load_dotenv

load_dotenv()
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-key")
JARVIS_USERNAME = os.getenv("JARVIS_USERNAME", "admin")
JARVIS_PASSWORD = os.getenv("JARVIS_PASSWORD", "")
JARVIS_SECRET = os.getenv("JARVIS_SECRET_KEY", "")
DB_PATH = os.getenv("DB_PATH", "data/companion.db")