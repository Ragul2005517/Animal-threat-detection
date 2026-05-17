from ultralytics import YOLO
import cv2

# Load the pretrained YOLOv8 model
model = YOLO("yolov8n.pt")  # small model, fast

# Load image
img_path = r"C:\Users\admin\Desktop\animal_project\dog.jpg"
img = cv2.imread(img_path)

# Detect objects
results = model(img_path)

# Show results
results[0].show()
