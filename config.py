import os
from dotenv import load_dotenv

load_dotenv()
JARVIS_SECRET = os.getenv("JARVIS_SECRET_KEY", "")
DB_PATH = os.getenv("DB_PATH", "data/companion.db")