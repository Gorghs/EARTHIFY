"""
Flask application for waste classification using ONNX model.
"""
from flask import Flask, request, render_template, jsonify, url_for
from werkzeug.utils import secure_filename
import os
import json
import logging
from datetime import datetime
import numpy as np
from PIL import Image

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def load_model(model_path):
    try:
        import onnxruntime as rt

        session = rt.InferenceSession(model_path)
        logging.info("ONNX model loaded successfully")
        return session
    except ModuleNotFoundError as error:
        logging.error(f"ONNX Runtime dependency missing: {error}")
        return None
    except Exception as error:
        logging.error(f"Error loading model: {error}")
        return None


model = load_model(os.path.join("..", "weights", "best.onnx"))

waste_types = {
    0: "battery",
    1: "biological",
    2: "brown-glass",
    3: "cardboard",
    4: "clothes",
    5: "green-glass",
    6: "metal",
    7: "paper",
    8: "plastic",
    9: "shoes",
    10: "trash",
    11: "white-glass",
}

category_map = {
    "battery": "Hazardous",
    "biological": "Organic",
    "brown-glass": "Recyclable",
    "cardboard": "Recyclable",
    "clothes": "Special",
    "green-glass": "Recyclable",
    "metal": "Recyclable",
    "paper": "Recyclable",
    "plastic": "Recyclable",
    "shoes": "Non-Recyclable",
    "trash": "Non-Recyclable",
    "white-glass": "Recyclable",
}

icon_map = {
    "Hazardous": "⚠️",
    "Organic": "🌿",
    "Recyclable": "♻️",
    "Non-Recyclable": "🗑️",
    "Special": "👕",
    "Unknown": "❓",
}


def get_waste_info():
    try:
        with open("waste_info.json", "r", encoding="utf-8") as info_file:
            return json.load(info_file)
    except Exception as error:
        logging.error(f"Error loading waste_info.json: {error}")
        return {}


waste_info = get_waste_info()


def classify_image(image_path):
    if model is None:
        raise RuntimeError("Model is not available")

    image = Image.open(image_path).convert("RGB")
    # Resize to 640x640 for YOLO model
    image = image.resize((640, 640))
    # Convert to numpy array and normalize (0-1 range)
    image = np.array(image, dtype=np.float32) / 255.0
    # Convert from (H, W, C) to (C, H, W) for YOLO
    image = np.transpose(image, (2, 0, 1))
    # Add batch dimension: (1, C, H, W)
    image = np.expand_dims(image, axis=0)

    # Get input name from the model
    input_name = model.get_inputs()[0].name
    
    # Run YOLO inference
    outputs = model.run(None, {input_name: image})
    # YOLO output is [1, 26, 8400] where:
    # - 4 bbox coordinates
    # - 1 objectness score
    # - 21 class scores (COCO classes)
    output = outputs[0][0]  # Shape: [26, 8400]
    
    # Extract objectness and class scores for our 12 waste classes (indices 5-16)
    obj_scores = output[4, :]  # Objectness scores
    class_scores = output[5:17, :]  # First 12 class scores
    
    # Find best detection by combining objectness with class confidence
    combined_scores = obj_scores * class_scores
    max_idx = np.unravel_index(np.argmax(combined_scores), combined_scores.shape)
    class_idx = int(max_idx[0])
    confidence = float(combined_scores[max_idx])
    
    label = waste_types.get(class_idx, "unknown")
    
    return label, confidence


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/classify", methods=["POST"])
def api_classify():
    if model is None:
        return jsonify({"error": "Model failed to load"}), 500

    image_file = request.files.get("image")
    if image_file is None or image_file.filename == "":
        return jsonify({"error": "No image uploaded"}), 400

    filename = secure_filename(image_file.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    saved_filename = f"{timestamp}_{filename}"
    saved_path = os.path.join(app.config["UPLOAD_FOLDER"], saved_filename)
    image_file.save(saved_path)

    try:
        label, confidence = classify_image(saved_path)
        category = category_map.get(label, "Unknown")
        details = waste_info.get(label, {})
        tip = details.get("tips", "Sort correctly and follow your local recycling rules.")
        if isinstance(tip, list):
            tip = tip[0] if tip else "Sort correctly and follow your local recycling rules."

        return jsonify(
            {
                "label": label,
                "category": category,
                "icon": icon_map.get(category, "❓"),
                "confidence": round(confidence * 100, 2),
                "tip": tip,
                "imageUrl": url_for("static", filename=f"uploads/{saved_filename}"),
            }
        )
    except Exception as error:
        logging.error(f"Classification error: {error}")
        return jsonify({"error": "Failed to classify image"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)








