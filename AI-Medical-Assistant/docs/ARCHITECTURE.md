# Architecture

```mermaid
flowchart LR
  User["User Browser"] --> React["React + Tailwind Frontend"]
  React --> API["FastAPI Backend"]
  API --> Auth["JWT Authentication"]
  API --> SQLite["SQLite Database"]
  API --> Uploads["Uploaded X-ray Storage"]
  API --> ML["TensorFlow/Keras CNN"]
  ML --> OpenCV["OpenCV Preprocessing"]
  ML --> GradCAM["Grad-CAM Heatmap"]
  API --> Reports["PDF and CSV Report Services"]
  Reports --> React
  GradCAM --> React
```

## Request Flow

1. User authenticates and receives a JWT.
2. User uploads a JPG, JPEG, or PNG chest X-ray from the protected dashboard.
3. FastAPI stores the image, preprocesses it with OpenCV, and sends it to the TensorFlow model.
4. The model returns a normal or pneumonia prediction and confidence score.
5. Grad-CAM creates a heatmap overlay from the final convolutional layer.
6. The scan row is stored in SQLite.
7. React displays result cards, original image, heatmap, analytics, history, and report links.
