import tensorflow as tf # type: ignore
import numpy as np
from PIL import Image

# Load model once
model = tf.keras.models.load_model("model.h5")

# Class names (VERY IMPORTANT: SAME ORDER AS TRAINING)
classes = [
    "Potato_Early_blight",
    "Potato_Late_blight",
    "Potato_healthy"
]

def predict_disease(image_path):
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)
    confidence = float(np.max(preds))
    predicted_class = classes[np.argmax(preds)]

    print("CONFIDENCE:", confidence)
    print("PREDICTED:", predicted_class)

    if confidence < 0.8:
        return "Unknown", confidence 

    # Clean name for display
    return predicted_class.replace("_", " ").title(), confidence 