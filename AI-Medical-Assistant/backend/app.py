from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.db import Base, engine
from routes import admin, auth, scans

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Medical Assistant - Pneumonia Detection API",
    description="Upload chest X-rays, run CNN inference, generate Grad-CAM explanations, and download reports.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
(BASE_DIR / "uploads").mkdir(exist_ok=True)
(BASE_DIR / "reports").mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=BASE_DIR / "uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(scans.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AI Medical Assistant"}
