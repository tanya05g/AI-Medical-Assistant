from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from database.db import get_db
from models.entities import Scan, User
from models.schemas import ScanOut, UserOut
from services.security import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserOut])
def users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.get("/scans", response_model=list[ScanOut])
def scans(
    search: str = Query("", description="Search prediction, risk, user email, or user name"),
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Scan).join(User)
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Scan.prediction.ilike(pattern), Scan.risk_level.ilike(pattern), User.email.ilike(pattern), User.full_name.ilike(pattern)))
    return query.order_by(Scan.created_at.desc()).all()


@router.delete("/scans/{scan_id}")
def delete_scan(scan_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    for path in [scan.image_path, scan.heatmap_path]:
        file_path = Path(path)
        if file_path.exists():
            file_path.unlink()
    db.delete(scan)
    db.commit()
    return {"message": "Scan deleted"}
