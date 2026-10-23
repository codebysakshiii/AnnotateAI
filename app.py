from flask import Flask, request, jsonify, send_from_directory, render_template
from ultralytics import YOLO
from pathlib import Path
from werkzeug.utils import secure_filename
import uuid
import cv2
import numpy as np

app = Flask(__name__)

# Project folders
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
RESULT_FOLDER = BASE_DIR / "static" / "results"
MODEL_PATH = BASE_DIR / "yolo11n.pt"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

print("Loading YOLO AI model...")
model = YOLO(str(MODEL_PATH))
print("AnnotateAI model loaded successfully!")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


# Upload image and detect objects
@app.route("/api/detect", methods=["POST"])
def detect_image():
    if "image" not in request.files:
        return jsonify({"error": "Please upload an image."}), 400

    file = request.files["image"]

    if not file.filename:
        return jsonify({"error": "No image selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Only JPG, JPEG, PNG and WEBP images are allowed."
        }), 400

    image_id = uuid.uuid4().hex
    extension = file.filename.rsplit(".", 1)[1].lower()
    safe_name = secure_filename(f"{image_id}.{extension}")
    input_path = UPLOAD_FOLDER / safe_name

    file.save(input_path)

    try:
        results = model.predict(
            source=str(input_path),
            save=False,
            conf=0.25,
            verbose=False
        )

        result = results[0]
        detections = []

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())

            coordinates = [
                round(float(value), 2)
                for value in box.xyxy[0].tolist()
            ]

            detections.append({
                "label": result.names[class_id],
                "confidence": round(confidence * 100, 2),
                "box": coordinates
            })

        annotated_image = result.plot()
        output_name = f"{image_id}.jpg"
        output_path = RESULT_FOLDER / output_name

        if not cv2.imwrite(str(output_path), annotated_image):
            raise RuntimeError("Could not save the annotated image.")

        return jsonify({
            "success": True,
            "message": "Image annotation completed!",
            "total_objects": len(detections),
            "detections": detections,
            "annotated_image": f"/results/{output_name}"
        })

    except Exception:
        app.logger.exception("Image detection failed")
        return jsonify({
            "error": "Image detection failed. Please try another image."
        }), 500

    finally:
        input_path.unlink(missing_ok=True)


# Serve annotated result images
@app.route("/results/<path:filename>")
def get_result(filename):
    return send_from_directory(RESULT_FOLDER, filename)


# Live camera frame detection
@app.route("/api/live-detect", methods=["POST"])
def live_detect():
    if "image" not in request.files:
        return jsonify({"error": "Camera frame missing."}), 400

    file = request.files["image"]
    image_bytes = file.read()

    if not image_bytes:
        return jsonify({"error": "Empty camera frame."}), 400

    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Invalid camera frame."}), 400

    try:
        results = model.predict(
            source=frame,
            conf=0.35,
            imgsz=416,
            verbose=False
        )

        result = results[0]
        detections = []

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())

            x1, y1, x2, y2 = [
                round(float(value), 2)
                for value in box.xyxy[0].tolist()
            ]

            detections.append({
                "label": result.names[class_id],
                "confidence": round(confidence * 100, 2),
                "box": [x1, y1, x2, y2]
            })

        height, width = frame.shape[:2]

        return jsonify({
            "success": True,
            "width": width,
            "height": height,
            "total_objects": len(detections),
            "detections": detections
        })

    except Exception:
        app.logger.exception("Live detection failed")
        return jsonify({
            "error": "Live detection failed."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)