import cv2

# Read the image
img = cv2.imread("dog.jpg")

# Resize the image
img_resized = cv2.resize(img, (400, 400))

# Convert to grayscale
img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

# Show results
cv2.imshow("Original Image", img)
cv2.imshow("Resized Image", img_resized)
cv2.imshow("Grayscale Image", img_gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
