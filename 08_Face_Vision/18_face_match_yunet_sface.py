"""Compare whether two images likely contain the same face using YuNet + SFace.
Requires the two ONNX model files from OpenCV Zoo and opencv-python.
This is biometric matching; use only images you have permission to process.
"""
from pathlib import Path
import cv2

DETECTOR_MODEL = Path("face_detection_yunet_2023mar.onnx")
RECOGNIZER_MODEL = Path("face_recognition_sface_2021dec.onnx")
IMAGE_1, IMAGE_2 = Path("face1.jpg"), Path("face2.jpg")
THRESHOLD_COSINE = 0.363  # OpenCV Zoo SFace example's reference threshold

def detect_largest_face(image, detector):
    h, w = image.shape[:2]
    detector.setInputSize((w, h))
    _, faces = detector.detect(image)
    if faces is None or len(faces) == 0:
        raise ValueError("No face detected in an input image.")
    return max(faces, key=lambda f: f[2] * f[3])

for file in (DETECTOR_MODEL, RECOGNIZER_MODEL, IMAGE_1, IMAGE_2):
    if not file.exists():
        raise SystemExit(f"Missing {file}. See README for model links and image setup.")
img1, img2 = cv2.imread(str(IMAGE_1)), cv2.imread(str(IMAGE_2))
if img1 is None or img2 is None:
    raise SystemExit("Could not read face1.jpg or face2.jpg.")
detector = cv2.FaceDetectorYN.create(str(DETECTOR_MODEL), "", (320, 320), 0.9, 0.3, 5000)
recognizer = cv2.FaceRecognizerSF.create(str(RECOGNIZER_MODEL), "")
face1 = detect_largest_face(img1, detector)
face2 = detect_largest_face(img2, detector)
aligned1 = recognizer.alignCrop(img1, face1)
aligned2 = recognizer.alignCrop(img2, face2)
feature1 = recognizer.feature(aligned1)
feature2 = recognizer.feature(aligned2)
score = recognizer.match(feature1, feature2, 0)  # 0 = cosine similarity in OpenCV SFace
print(f"Cosine similarity: {score:.4f}")
print("Likely same person" if score >= THRESHOLD_COSINE else "Likely different people")
print("This is an automated similarity estimate, not proof of identity.")
