from flask import Flask, render_template, request
from ultralytics import YOLO
import cv2
import os

# Initialize Flask App
app = Flask(__name__)

# Upload Folder Configuration
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Trained YOLO Model
model = YOLO("best.pt")


# ----------------------------------------
# Function for Video Detection
# ----------------------------------------
def detect_video(path):

    cap = cv2.VideoCapture(path)

    aggressive_count = 0
    calm_count = 0
    total_frames = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # YOLO Prediction
        results = model(frame)

        # Check if probabilities exist
        if results[0].probs is None:
            continue

        # Convert probabilities to list
        probs = results[0].probs.data.tolist()

        # Class Probabilities
        aggressive = probs[0]
        calm = probs[1]

        # Count Behaviour
        if aggressive > calm:
            aggressive_count += 1
        else:
            calm_count += 1

        total_frames += 1

    cap.release()

    # Avoid division by zero
    if total_frames == 0:
        return 0, 0

    aggressive_percent = (aggressive_count / total_frames) * 100
    calm_percent = (calm_count / total_frames) * 100

    return aggressive_percent, calm_percent


# ----------------------------------------
# Home Page
# ----------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------------------
# Prediction Route
# ----------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    # Get Uploaded File
    file = request.files["file"]

    # Save File
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Perform Detection
    aggressive_percent, calm_percent = detect_video(file_path)

    # Risk Analysis
    if aggressive_percent > 60:
        risk = "High Risk Behaviour Detected"
    elif aggressive_percent > 30:
        risk = "Moderate Risk Behaviour"
    else:
        risk = "Normal Behaviour"

    # Return Result
    return render_template(
        "result.html",
        aggressive=round(aggressive_percent, 2),
        calm=round(calm_percent, 2),
        risk=risk
    )


# ----------------------------------------
# Run Flask App
# ----------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)