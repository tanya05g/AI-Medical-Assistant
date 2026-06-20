from pathlib import Path
import argparse
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from inference import IMG_SIZE, ensure_model


def evaluate(test_dir: Path) -> None:
    dataset = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        labels="inferred",
        label_mode="binary",
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=32,
        shuffle=False,
    )
    model = ensure_model()
    y_true, y_prob = [], []
    for images, labels in dataset:
        y_true.extend(labels.numpy().ravel().astype(int))
        y_prob.extend(model.predict(images, verbose=0).ravel())
    y_pred = (np.array(y_prob) >= 0.5).astype(int)
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print(classification_report(y_true, y_pred, target_names=["Normal", "Pneumonia"]))
    print("Confusion matrix:")
    print(confusion_matrix(y_true, y_pred))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate pneumonia model accuracy and confusion matrix.")
    parser.add_argument("--test-dir", required=True, help="Test directory with Normal and Pneumonia folders")
    args = parser.parse_args()
    evaluate(Path(args.test_dir))
