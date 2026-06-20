# AI Medical Assistant - Pneumonia Detection from Chest X-Rays

A full-stack healthcare AI application for uploading chest X-rays, predicting Normal vs Pneumonia, generating Grad-CAM heatmaps, storing scan history, visualizing analytics, and exporting PDF/CSV reports.

## Tech Stack

- AI/ML: Python, TensorFlow/Keras, OpenCV, NumPy, Pandas, Matplotlib
- Backend: FastAPI, SQLite, SQLAlchemy, JWT authentication
- Frontend: React, Tailwind CSS, Chart.js

## Project Structure

```text
AI-Medical-Assistant/
  backend/
    app.py
    routes/
    database/
    models/
    services/
    uploads/
    reports/
    requirements.txt
  frontend/
    src/
    public/
    package.json
    tailwind.config.js
  model/
    pneumonia_model.h5
    inference.py
    train_model.py
    evaluate_model.py
  docs/
  screenshots/
  README.md
```

`pneumonia_model.h5` is created automatically the first time inference runs if you have not trained yet. Train the model with your dataset before clinical evaluation.

## Installation

### Backend

```bash
cd AI-Medical-Assistant/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

API docs open at `http://127.0.0.1:8000/docs`.

### Frontend

```bash
cd AI-Medical-Assistant/frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Usage

1. Register a user. The first registered account becomes admin.
2. Open the dashboard.
3. Upload a JPG, JPEG, or PNG chest X-ray.
4. Review prediction, confidence, risk level, timestamp, original image, and Grad-CAM overlay.
5. Download the PDF report or CSV history.
6. Admin users can view users, search scans, and delete scan records.

## Training

Organize a dataset as:

```text
dataset/
  train/Normal
  train/Pneumonia
  val/Normal
  val/Pneumonia
  test/Normal
  test/Pneumonia
```

Run:

```bash
cd AI-Medical-Assistant/model
python train_model.py --data-dir C:\path\to\dataset --epochs 15
```

Metrics and plots are written to `model/metrics`.

## Documentation

- API: `docs/API.md`
- Architecture: `docs/ARCHITECTURE.md`
- Database schema: `docs/DATABASE_SCHEMA.md`
- Deployment: `docs/DEPLOYMENT.md`
- Project report: `docs/PROJECT_REPORT.md`

## Medical Disclaimer

This project is an educational AI decision-support application. It is not a medical device and must not be used as the sole basis for diagnosis or treatment.
