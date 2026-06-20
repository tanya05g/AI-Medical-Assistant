from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report, confusion_matrix
from inference import IMG_SIZE, MODEL_PATH, build_model


def dataset_from_directory(path: Path, shuffle: bool) -> tf.data.Dataset:
    return tf.keras.utils.image_dataset_from_directory(
        path,
        labels="inferred",
        label_mode="binary",
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=32,
        shuffle=shuffle,
    ).prefetch(tf.data.AUTOTUNE)


def train(data_dir: Path, epochs: int) -> None:
    train_ds = dataset_from_directory(data_dir / "train", True)
    val_ds = dataset_from_directory(data_dir / "val", False)
    test_ds = dataset_from_directory(data_dir / "test", False)

    model = build_model()
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(MODEL_PATH, save_best_only=True, monitor="val_accuracy", mode="max"),
        tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
    ]
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks)
    model.save(MODEL_PATH)

    y_true, y_prob = [], []
    for images, labels in test_ds:
        y_true.extend(labels.numpy().ravel().astype(int))
        y_prob.extend(model.predict(images, verbose=0).ravel())
    y_pred = (np.array(y_prob) >= 0.5).astype(int)

    metrics_dir = Path(__file__).resolve().parent / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=["Normal", "Pneumonia"])
    (metrics_dir / "evaluation.txt").write_text(f"Accuracy: {accuracy:.4f}\n\n{report}", encoding="utf-8")

    matrix = confusion_matrix(y_true, y_pred)
    display = ConfusionMatrixDisplay(matrix, display_labels=["Normal", "Pneumonia"])
    display.plot(cmap="Blues")
    plt.title("Pneumonia CNN Confusion Matrix")
    plt.tight_layout()
    plt.savefig(metrics_dir / "confusion_matrix.png", dpi=160)

    plt.figure()
    plt.plot(history.history["accuracy"], label="train_accuracy")
    plt.plot(history.history["val_accuracy"], label="val_accuracy")
    plt.legend()
    plt.title("Model Accuracy")
    plt.tight_layout()
    plt.savefig(metrics_dir / "accuracy_curve.png", dpi=160)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the pneumonia detection CNN.")
    parser.add_argument("--data-dir", required=True, help="Directory with train/val/test class folders")
    parser.add_argument("--epochs", type=int, default=15)
    args = parser.parse_args()
    train(Path(args.data_dir), args.epochs)
