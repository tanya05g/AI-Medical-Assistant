from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import FRONTEND_ORIGINS, REPORT_DIR, UPLOAD_DIR
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
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(auth.router)
app.include_router(scans.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AI Medical Assistant"}
