"""Face detection using OpenCV's pre-trained Haar cascade.
Install: python -m pip install opencv-python
Put face.jpg next to this script, or pass an image path as an argument.
"""
import sys
from pathlib import Path
import cv2

image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("face.jpg")
image = cv2.imread(str(image_path))
if image is None:
    raise SystemExit(f"Cannot read image: {image_path}. Check the path.")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
model_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(model_path)
if cascade.empty():
    raise SystemExit("Could not load OpenCV Haar cascade.")
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
print("Faces detected:", len(faces))
out_path = image_path.with_name(image_path.stem + "_haar_detected.jpg")
cv2.imwrite(str(out_path), image)
print("Saved result:", out_path)
cv2.imshow("Haar Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
