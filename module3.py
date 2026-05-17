from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLO model
model = YOLO("yolov8n.pt")

# Load image
img_path = r"C:\Users\admin\Desktop\animal_project\dog.jpg"
img = cv2.imread(img_path)

# Run detection
results = model(img_path)

for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]

        if label in ["dog", "cat", "cow", "horse"]:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            animal = img[y1:y2, x1:x2]

            # Convert to grayscale
            gray = cv2.cvtColor(animal, cv2.COLOR_BGR2GRAY)

            # Edge detection
            edges = cv2.Canny(gray, 50, 150)

            # Contour extraction
            contours, _ = cv2.findContours(
                edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                perimeter = cv2.arcLength(largest_contour, True)

                print("---- Animal Feature Data ----")
                print("Animal:", label)
                print("Body Area:", int(area))
                print("Body Perimeter:", int(perimeter))

                # Draw contour
                cv2.drawContours(animal, [largest_contour], -1, (0, 255, 0), 2)

            cv2.imshow("Extracted Animal Features", animal)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
