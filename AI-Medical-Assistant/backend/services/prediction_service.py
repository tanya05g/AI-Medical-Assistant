from pathlib import Path
import sys
import cv2
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT_DIR / "model"
sys.path.append(str(MODEL_DIR))

from inference import ensure_model, preprocess_image, predict_image, generate_gradcam  # noqa: E402

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
HEATMAP_DIR = UPLOAD_DIR / "heatmaps"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
HEATMAP_DIR.mkdir(parents=True, exist_ok=True)


def risk_level(label: str, confidence: float) -> str:
    if label == "Normal":
        return "Low"
    if confidence >= 85:
        return "High"
    if confidence >= 65:
        return "Moderate"
    return "Low"


def analyze_xray(image_path: Path) -> dict:
    model = ensure_model()
    image_array = preprocess_image(str(image_path))
    label, confidence, probability = predict_image(model, image_array)
    heatmap = generate_gradcam(model, image_array)

    original = cv2.imread(str(image_path))
    original = cv2.resize(original, (224, 224))
    heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(original, 0.55, heatmap_color, 0.45, 0)

    heatmap_path = HEATMAP_DIR / f"{image_path.stem}_gradcam.png"
    cv2.imwrite(str(heatmap_path), overlay)

    return {
        "prediction": label,
        "confidence": round(float(confidence), 2),
        "probability": float(probability),
        "risk_level": risk_level(label, confidence),
        "heatmap_path": str(heatmap_path),
    }
