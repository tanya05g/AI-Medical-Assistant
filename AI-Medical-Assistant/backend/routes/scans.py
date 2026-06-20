from datetime import datetime, timedelta
from pathlib import Path
import shutil
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database.db import get_db
from models.entities import Scan, User
from models.schemas import ScanOut
from services.prediction_service import UPLOAD_DIR, analyze_xray
from services.report_service import create_csv_history, create_pdf_report
from services.security import get_current_user

router = APIRouter(prefix="/api/scans", tags=["Scans"])
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


@router.post("/analyze", response_model=ScanOut)
def analyze_scan(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only JPG, JPEG, and PNG images are accepted")

    safe_name = f"user_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}{extension}"
    image_path = UPLOAD_DIR / safe_name
    with image_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_xray(image_path)
    scan = Scan(
        user_id=current_user.id,
        image_path=str(image_path),
        heatmap_path=result["heatmap_path"],
        prediction=result["prediction"],
        confidence=result["confidence"],
        risk_level=result["risk_level"],
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan


@router.get("/history", response_model=list[ScanOut])
def history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Scan).filter(Scan.user_id == current_user.id).order_by(Scan.created_at.desc()).all()


@router.get("/analytics")
def analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scans = db.query(Scan).filter(Scan.user_id == current_user.id).all()
    distribution = {"Normal": 0, "Pneumonia": 0}
    weekly = []
    today = datetime.utcnow().date()
    for index in range(6, -1, -1):
        day = today - timedelta(days=index)
        count = sum(1 for scan in scans if scan.created_at.date() == day)
        weekly.append({"date": day.isoformat(), "count": count})
    for scan in scans:
        distribution[scan.prediction] = distribution.get(scan.prediction, 0) + 1
    return {
        "total": len(scans),
        "normal": distribution.get("Normal", 0),
        "pneumonia": distribution.get("Pneumonia", 0),
        "distribution": distribution,
        "weekly": weekly,
        "average_confidence": round(sum(scan.confidence for scan in scans) / len(scans), 2) if scans else 0,
    }


@router.get("/{scan_id}/image")
def scan_image(scan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return FileResponse(scan.image_path)


@router.get("/{scan_id}/heatmap")
def scan_heatmap(scan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return FileResponse(scan.heatmap_path)


@router.get("/{scan_id}/report")
def report(scan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return FileResponse(create_pdf_report(scan, current_user), filename=f"scan_{scan.id}_report.pdf")


@router.get("/exports/history.csv")
def csv_export(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scans = db.query(Scan).filter(Scan.user_id == current_user.id).order_by(Scan.created_at.desc()).all()
    return FileResponse(create_csv_history(scans, current_user.id), filename="scan_history.csv")
