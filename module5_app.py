from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog
import cv2
import os

# Load YOLO model
model = YOLO("best.pt")


# -----------------------------------------
# VIDEO DETECTION FUNCTION
# -----------------------------------------
def detect_from_video(video_path):

    video = cv2.VideoCapture(video_path)

    total_frames = 0
    analyzed_frames = 0

    aggressive_frames = 0
    calm_frames = 0

    consecutive_count = 0

    # Analyze every 5th frame
    frame_skip = 5

    while True:

        ret, frame = video.read()

        if not ret:
            break

        total_frames += 1

        # Skip frames for faster processing
        if total_frames % frame_skip != 0:
            continue

        analyzed_frames += 1

        # Run YOLO prediction
        results = model(frame)

        probs = results[0].probs

        # Safety check
        if probs is None:
            continue

        aggressive = float(probs.data[0])
        calm = float(probs.data[1])

        # Prediction logic
        if aggressive > calm:

            label = "Aggressive"
            aggressive_frames += 1
            consecutive_count += 1

        else:

            label = "Calm"
            calm_frames += 1
            consecutive_count = 0

        # Print frame result
        print(f"Frame {total_frames} --> {label}")

        # Display label on video
        cv2.putText(
            frame,
            label,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # Show video window
        cv2.imshow("Video Detection", frame)

        # Alert system
        if consecutive_count >= 5:
            print("⚠ ALERT: Aggressive Behaviour Detected!")

        # Quit button
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    # Final Result
    if analyzed_frames > 0:

        aggression_percentage = (
            aggressive_frames / analyzed_frames
        ) * 100

        calm_percentage = (
            calm_frames / analyzed_frames
        ) * 100

        print("\n------ FINAL RESULT ------")

        print(f"Total Frames      : {total_frames}")
        print(f"Analyzed Frames   : {analyzed_frames}")

        print(f"Aggressive Frames : {aggressive_frames}")
        print(f"Calm Frames       : {calm_frames}")

        print(f"\nAggression Level : {aggression_percentage:.2f}%")
        print(f"Calm Level       : {calm_percentage:.2f}%")

    else:
        print("No frames analyzed.")


# -----------------------------------------
# IMAGE DETECTION FUNCTION
# -----------------------------------------
def detect_from_image(img_path):

    results = model(img_path)

    probs = results[0].probs

    if probs is None:
        print("No prediction found.")
        return

    aggressive = float(probs.data[0])
    calm = float(probs.data[1])

    print("\n📊 Prediction Result:")
    print(f"Aggressive : {aggressive:.2f}")
    print(f"Calm       : {calm:.2f}")

    if calm > aggressive:
        print("✅ Dog is CALM 🐶")
    else:
        print("⚠ Dog is AGGRESSIVE 🚨")


# -----------------------------------------
# MAIN PROGRAM
# -----------------------------------------
if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Image or Video",
        filetypes=[
            ("All Supported Files", "*.jpg *.jpeg *.png *.bmp *.mp4 *.avi *.mov *.mkv"),
            ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
            ("Video Files", "*.mp4 *.avi *.mov *.mkv"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        print("No file selected.")
        exit()

    print(f"Selected file: {file_path}")

    # Check whether file is video
    video = cv2.VideoCapture(file_path)

    if video.isOpened():

        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # If video has frames -> video input
        if frame_count > 1:
            video.release()
            detect_from_video(file_path)

        else:
            video.release()
            detect_from_image(file_path)

    else:
        detect_from_image(file_path)