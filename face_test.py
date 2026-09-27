import cv2
import os

print("Face Detection Test Started")

# OpenCV ke built-in Haar Cascade ka path
cascade_path = os.path.join(
    cv2.data.haarcascades,
    "haarcascade_frontalface_default.xml"
)

# Haar Cascade load karo
face_detector = cv2.CascadeClassifier(cascade_path)

if face_detector.empty():
    print("ERROR: Face detector could not be loaded!")
    exit()

print("Face detector loaded successfully!")

# Dataset folder
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Open camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera not opening")
    exit()

print("Camera Opened Successfully!")
print("Look at the camera.")
print("Press Q to exit.")

count = 0

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Detection Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

print("Face Detection Test Finished")