import os
import re
import cv2
import numpy as np


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset"
)

TRAINER_PATH = os.path.join(
    BASE_DIR,
    "trainer"
)

TRAINER_FILE = os.path.join(
    TRAINER_PATH,
    "trainer.yml"
)


# =====================================================
# CREATE TRAINER FOLDER
# =====================================================

os.makedirs(
    TRAINER_PATH,
    exist_ok=True
)


# =====================================================
# CHECK DATASET
# =====================================================

if not os.path.exists(DATASET_PATH):

    print("ERROR: Dataset folder not found.")

    exit()


# =====================================================
# LOAD HAAR CASCADE
# =====================================================

CASCADE_PATH = os.path.join(
    cv2.data.haarcascades,
    "haarcascade_frontalface_default.xml"
)

detector = cv2.CascadeClassifier(
    CASCADE_PATH
)


if detector.empty():

    print(
        "ERROR: Haar Cascade could not be loaded."
    )

    exit()


# =====================================================
# CHECK LBPH
# =====================================================

if not hasattr(
    cv2,
    "face"
):

    print(
        "ERROR: cv2.face is not available."
    )

    print(
        "Install opencv-contrib-python:"
    )

    print(
        "pip install opencv-contrib-python"
    )

    exit()


# =====================================================
# GET DATASET FILES
# =====================================================

image_files = []

for filename in os.listdir(
    DATASET_PATH
):

    if filename.lower().endswith(
        (".jpg", ".jpeg", ".png")
    ):

        image_files.append(
            filename
        )


if not image_files:

    print(
        "ERROR: No images found in dataset."
    )

    exit()


image_files.sort()


print()
print("==============================================")
print("        FACE RECOGNITION TRAINING")
print("==============================================")
print()

print(
    "Dataset:",
    DATASET_PATH
)

print(
    "Trainer:",
    TRAINER_FILE
)

print()


# =====================================================
# STORE ONE PHOTO PER STUDENT
# =====================================================

student_images = {}


# Expected filename:

# User.1.1.jpg
# User.2.1.jpg
# User.10.1.jpg
# User.101.1.jpg


pattern = re.compile(
    r"^User\.(\d+)\.1\.(jpg|jpeg|png)$",
    re.IGNORECASE
)


# =====================================================
# READ DATASET
# =====================================================

for filename in image_files:

    match = pattern.match(
        filename
    )


    # -----------------------------------------------
    # INVALID FILE NAME
    # -----------------------------------------------

    if not match:

        print(
            "Skipping invalid file:",
            filename
        )

        continue


    # -----------------------------------------------
    # GET STUDENT ID
    # -----------------------------------------------

    student_id = int(
        match.group(1)
    )


    # -----------------------------------------------
    # ONE PHOTO PER STUDENT
    # -----------------------------------------------

    if student_id in student_images:

        print(
            f"Duplicate photo found for "
            f"Student ID {student_id}: "
            f"{filename}"
        )

        print(
            "Skipping duplicate."
        )

        continue


    student_images[
        student_id
    ] = filename


# =====================================================
# CHECK VALID STUDENTS
# =====================================================

if not student_images:

    print()
    print(
        "ERROR: No valid student photos found."
    )

    print()
    print(
        "Expected format:"
    )

    print(
        "User.1.1.jpg"
    )

    print(
        "User.2.1.jpg"
    )

    print(
        "User.10.1.jpg"
    )

    exit()


print(
    "Valid students:",
    len(student_images)
)

print()


# =====================================================
# PREPARE TRAINING DATA
# =====================================================

faces = []
ids = []


for student_id in sorted(
    student_images.keys()
):

    filename = student_images[
        student_id
    ]

    image_path = os.path.join(
        DATASET_PATH,
        filename
    )


    print(
        f"Processing Student ID "
        f"{student_id}: {filename}"
    )


    # -----------------------------------------------
    # READ IMAGE
    # -----------------------------------------------

    image = cv2.imread(
        image_path,
        cv2.IMREAD_GRAYSCALE
    )


    if image is None:

        print(
            "ERROR: Could not read:",
            filename
        )

        continue


    # -----------------------------------------------
    # NORMALIZE IMAGE
    # -----------------------------------------------

    image = cv2.equalizeHist(
        image
    )


    # -----------------------------------------------
    # DETECT FACE
    # -----------------------------------------------

    detected_faces = detector.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )


    # -----------------------------------------------
    # IF FACE DETECTION FAILS
    # -----------------------------------------------

    if len(detected_faces) == 0:

        print(
            "WARNING: No face detected in:",
            filename
        )

        # Since capture.py already saves
        # cropped face images, use the image itself.

        face_image = image

    else:

        # -------------------------------------------
        # USE LARGEST FACE
        # -------------------------------------------

        largest_face = max(
            detected_faces,
            key=lambda rect:
                rect[2] * rect[3]
        )


        x, y, w, h = largest_face

        face_image = image[
            y:y + h,
            x:x + w
        ]


    # -----------------------------------------------
    # VALIDATE FACE IMAGE
    # -----------------------------------------------

    if face_image.size == 0:

        print(
            "WARNING: Invalid face image:",
            filename
        )

        continue


    # -----------------------------------------------
    # RESIZE
    # -----------------------------------------------

    face_image = cv2.resize(
        face_image,
        (200, 200)
    )


    faces.append(
        face_image
    )

    ids.append(
        student_id
    )


    print(
        f"Added Student ID {student_id}"
    )


# =====================================================
# CHECK TRAINING DATA
# =====================================================

if len(faces) == 0:

    print()
    print(
        "ERROR: No valid training images."
    )

    exit()


# =====================================================
# CONVERT IDS
# =====================================================

ids = np.array(
    ids,
    dtype=np.int32
)


# =====================================================
# CREATE LBPH RECOGNIZER
# =====================================================

recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8
)


# =====================================================
# TRAIN MODEL
# =====================================================

print()
print(
    "Training started..."
)

recognizer.train(
    faces,
    ids
)


# =====================================================
# SAVE MODEL
# =====================================================

recognizer.write(
    TRAINER_FILE
)


# =====================================================
# SUCCESS
# =====================================================

print()
print("==============================================")
print("          TRAINING COMPLETED")
print("==============================================")
print()

print(
    "Students trained:",
    len(faces)
)

print(
    "Student IDs:",
    sorted(ids.tolist())
)

print(
    "Trainer file:",
    TRAINER_FILE
)

print()
print(
    "Training successful!"
)