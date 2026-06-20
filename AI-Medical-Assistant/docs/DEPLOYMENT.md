# Deployment Guide

## Backend

Use a production ASGI server behind a reverse proxy.

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

For production, set a strong JWT secret in `services/security.py` or load it from environment variables.

## Frontend

```bash
cd frontend
npm install
npm run build
```

Serve `frontend/dist` with Nginx, Caddy, or a static hosting service. Set `VITE_API_URL` during build when the backend is not on `http://127.0.0.1:8000`.

## Model

Train with a chest X-ray dataset arranged as:

```text
dataset/
  train/
    Normal/
    Pneumonia/
  val/
    Normal/
    Pneumonia/
  test/
    Normal/
    Pneumonia/
```

Then run:

```bash
cd model
python train_model.py --data-dir C:\path\to\dataset --epochs 15
```

The trained model is saved as `model/pneumonia_model.h5`.
