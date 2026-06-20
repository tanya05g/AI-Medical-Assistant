from pathlib import Path
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

IMG_SIZE = 224
MODEL_PATH = Path(__file__).resolve().parent / "pneumonia_model.h5"


def build_model() -> tf.keras.Model:
    inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = layers.Rescaling(1.0 / 255)(inputs)
    x = layers.Conv2D(32, 3, activation="relu", padding="same", name="conv_block_1")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, 3, activation="relu", padding="same", name="conv_block_2")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(128, 3, activation="relu", padding="same", name="last_conv")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.35)(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)
    model = models.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


def ensure_model() -> tf.keras.Model:
    if MODEL_PATH.exists():
        return tf.keras.models.load_model(MODEL_PATH)
    model = build_model()
    model.save(MODEL_PATH)
    return model


def preprocess_image(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Unable to read image file")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    return np.expand_dims(image.astype("float32"), axis=0)


def predict_image(model: tf.keras.Model, image_array: np.ndarray) -> tuple[str, float, float]:
    probability = float(model.predict(image_array, verbose=0)[0][0])
    label = "Pneumonia" if probability >= 0.5 else "Normal"
    confidence = probability * 100 if label == "Pneumonia" else (1 - probability) * 100
    return label, confidence, probability


def generate_gradcam(model: tf.keras.Model, image_array: np.ndarray, layer_name: str = "last_conv") -> np.ndarray:
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(layer_name).output, model.output],
    )
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image_array)
        loss = predictions[:, 0]
    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = np.maximum(heatmap, 0)
    max_value = np.max(heatmap)
    if max_value > 0:
        heatmap /= max_value
    return cv2.resize(np.array(heatmap), (IMG_SIZE, IMG_SIZE))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run pneumonia inference on a chest X-ray image.")
    parser.add_argument("image", help="Path to a JPG, JPEG, or PNG image")
    args = parser.parse_args()
    cnn = ensure_model()
    image = preprocess_image(args.image)
    pred, conf, prob = predict_image(cnn, image)
    print({"prediction": pred, "confidence": round(conf, 2), "pneumonia_probability": round(prob, 4)})
