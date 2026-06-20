# Deployment Guide

## Recommended Hosting

- Backend: Render web service
- Frontend: Vercel static React app
- Source: GitHub repository `tanya05g/AI-Medical-Assistant`

This project uses SQLite and uploaded image files, so the backend should run on a service with persistent storage. The included `render.yaml` config uses a persistent disk mounted at `/var/data`.

## Backend on Render

1. Push the latest code to GitHub.
2. Open Render and create a new Blueprint from the repository.
3. Select `AI-Medical-Assistant/render.yaml`.
4. Set `FRONTEND_ORIGINS` after the Vercel frontend URL is available.

Manual Render settings, if you do not use the blueprint:

```bash
Root Directory: AI-Medical-Assistant/backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
```

Environment variables:

```text
PYTHON_VERSION=3.11.9
SECRET_KEY=<generate a long random value>
STORAGE_DIR=/var/data
DATABASE_URL=sqlite:////var/data/medical_assistant.db
FRONTEND_ORIGINS=https://your-vercel-app.vercel.app
```

## Frontend on Vercel

1. Import the GitHub repository into Vercel.
2. Set the root directory to `AI-Medical-Assistant/frontend`.
3. Use these build settings:

```text
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

4. Add this environment variable:

```text
VITE_API_URL=https://your-render-backend.onrender.com
```

5. Deploy.
6. Copy the Vercel URL and update Render's `FRONTEND_ORIGINS` with that URL.

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
