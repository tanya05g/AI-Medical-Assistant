import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-for-production")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'database' / 'medical_assistant.db'}")

storage_root = Path(os.getenv("STORAGE_DIR", BASE_DIR)).resolve()
UPLOAD_DIR = storage_root / "uploads"
REPORT_DIR = storage_root / "reports"

raw_origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
FRONTEND_ORIGINS = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
