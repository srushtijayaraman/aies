"""Neural-network face detection using OpenCV YuNet (ONNX model required).
Install: python -m pip install opencv-python
Download face_detection_yunet_2023mar.onnx from the OpenCV Zoo model folder
and put it beside this script. Input image defaults to face.jpg.
"""
import sys
from pathlib import Path
import cv2

image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("face.jpg")
model_path = Path("face_detection_yunet_2023mar.onnx")
image = cv2.imread(str(image_path))
if image is None:
    raise SystemExit(f"Cannot read image: {image_path}")
if not model_path.exists():
    raise SystemExit("Missing face_detection_yunet_2023mar.onnx. See README for official download link.")
h, w = image.shape[:2]
detector = cv2.FaceDetectorYN.create(str(model_path), "", (w, h), 0.9, 0.3, 5000)
_, faces = detector.detect(image)
count = 0 if faces is None else len(faces)
if faces is not None:
    for face in faces:
        x, y, fw, fh = face[:4].astype(int)
        cv2.rectangle(image, (x, y), (x+fw, y+fh), (0, 255, 0), 2)
print("Faces detected:", count)
out_path = image_path.with_name(image_path.stem + "_yunet_detected.jpg")
cv2.imwrite(str(out_path), image)
print("Saved result:", out_path)
cv2.imshow("YuNet DNN Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
