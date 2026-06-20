# Project Report

## Title

AI Medical Assistant - Pneumonia Detection from Chest X-Rays

## Objective

Build a full-stack web application that lets users upload chest X-ray images and receive AI-assisted pneumonia predictions, confidence scores, Grad-CAM visual explanations, analytics, and downloadable reports.

## Methodology

The backend preprocesses images with OpenCV by loading, converting BGR to RGB, resizing to 224 x 224 pixels, and batching for TensorFlow inference. The CNN performs binary classification with sigmoid output. A prediction score greater than or equal to 0.5 is interpreted as Pneumonia; otherwise the image is classified as Normal.

Grad-CAM uses the final convolutional layer to compute a class activation heatmap. The heatmap is resized and blended with the original X-ray for explainability.

## Evaluation

`model/train_model.py` trains the CNN and writes:

- `model/metrics/evaluation.txt`
- `model/metrics/confusion_matrix.png`
- `model/metrics/accuracy_curve.png`

`model/evaluate_model.py` can also calculate accuracy, classification report, and confusion matrix for a separate test directory.

## Security

Users authenticate with hashed passwords and JWT bearer tokens. Scan history is scoped to the current user. Admin routes require the admin role.

## Limitations

The model must be trained on a clinically appropriate, licensed dataset before real-world use. This software is decision support only and is not a substitute for physician diagnosis.
