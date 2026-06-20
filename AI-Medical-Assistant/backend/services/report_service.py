from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def create_pdf_report(scan, user) -> Path:
    path = REPORT_DIR / f"scan_{scan.id}_report.pdf"
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    y = height - inch

    c.setFont("Helvetica-Bold", 18)
    c.drawString(inch, y, "AI Medical Assistant - Pneumonia Report")
    y -= 0.45 * inch
    c.setFont("Helvetica", 11)
    c.drawString(inch, y, f"Patient/User: {user.full_name} ({user.email})")
    y -= 0.28 * inch
    c.drawString(inch, y, f"Scan ID: {scan.id}")
    y -= 0.28 * inch
    c.drawString(inch, y, f"Timestamp: {scan.created_at}")
    y -= 0.28 * inch
    c.drawString(inch, y, f"Prediction: {scan.prediction}")
    y -= 0.28 * inch
    c.drawString(inch, y, f"Confidence: {scan.confidence:.2f}%")
    y -= 0.28 * inch
    c.drawString(inch, y, f"Risk level: {scan.risk_level}")
    y -= 0.45 * inch
    c.drawString(inch, y, "This report is an AI decision-support output and is not a clinical diagnosis.")
    y -= 0.45 * inch

    if Path(scan.image_path).exists():
        c.drawImage(scan.image_path, inch, y - 2.2 * inch, width=2.2 * inch, height=2.2 * inch)
    if Path(scan.heatmap_path).exists():
        c.drawImage(scan.heatmap_path, 3.7 * inch, y - 2.2 * inch, width=2.2 * inch, height=2.2 * inch)
    c.save()
    return path


def create_csv_history(scans, user_id: int) -> Path:
    path = REPORT_DIR / f"user_{user_id}_history.csv"
    rows = [
        {
            "scan_id": scan.id,
            "prediction": scan.prediction,
            "confidence": scan.confidence,
            "risk_level": scan.risk_level,
            "created_at": scan.created_at,
        }
        for scan in scans
    ]
    pd.DataFrame(rows).to_csv(path, index=False)
    return path
