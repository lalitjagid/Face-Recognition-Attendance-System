import os
import cv2
import numpy as np


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_FOLDER = os.path.join(
    BASE_DIR,
    "dataset"
)


# ==========================================
# CREATE DATASET FOLDER
# ==========================================

os.makedirs(
    DATASET_FOLDER,
    exist_ok=True
)


# ==========================================
# HAAR CASCADE
# ==========================================

CASCADE_PATH = os.path.join(
    cv2.data.haarcascades,
    "haarcascade_frontalface_default.xml"
)

FACE_DETECTOR = cv2.CascadeClassifier(
    CASCADE_PATH
)


if FACE_DETECTOR.empty():

    raise RuntimeError(
        "Haar Cascade could not be loaded."
    )


# ==========================================
# SAVE ONE FACE PHOTO
# ==========================================

def save_face_image(student_id, image_bytes):

    student_id = str(
        student_id
    ).strip()


    if not student_id:

        return (
            False,
            "Student ID is required."
        )


    # ======================================
    # ONE PHOTO ONLY
    # ======================================

    filename = (
        f"User.{student_id}.1.jpg"
    )

    filepath = os.path.join(
        DATASET_FOLDER,
        filename
    )


    # ======================================
    # DUPLICATE PHOTO CHECK
    # ======================================

    if os.path.exists(filepath):

        return (
            False,
            "Face photo already exists "
            "for this Student ID."
        )


    # ======================================
    # CONVERT IMAGE BYTES
    # ======================================

    try:

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

    except Exception as error:

        print(
            "Image decode error:",
            error
        )

        return (
            False,
            "Invalid image data."
        )


    if image is None:

        return (
            False,
            "Could not read image."
        )


    # ======================================
    # CHECK IMAGE SIZE
    # ======================================

    height, width = image.shape[:2]

    print(
        f"Camera Image Size: {width} x {height}"
    )


    if width < 100 or height < 100:

        return (
            False,
            "Camera image is too small."
        )


    # ======================================
    # GRAYSCALE
    # ======================================

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # ======================================
    # IMPROVE CONTRAST
    # ======================================

    gray_equalized = cv2.equalizeHist(
        gray
    )


    # ======================================
    # FACE DETECTION
    # ======================================

    faces = FACE_DETECTOR.detectMultiScale(
        gray_equalized,
        scaleFactor=1.05,
        minNeighbors=4,
        minSize=(60, 60)
    )


    # ======================================
    # SECOND DETECTION ATTEMPT
    # ======================================

    if len(faces) == 0:

        faces = FACE_DETECTOR.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(50, 50)
        )


    # ======================================
    # NO FACE
    # ======================================

    if len(faces) == 0:

        print(
            "No face detected in camera image."
        )

        return (
            False,
            "No face detected. "
            "Please look directly at the camera "
            "and make sure your face is clearly visible."
        )


    # ======================================
    # MULTIPLE FACES
    # ======================================

    if len(faces) > 1:

        print(
            f"Multiple faces detected: {len(faces)}"
        )

        return (
            False,
            "More than one face detected. "
            "Please keep only one person "
            "in front of the camera."
        )


    # ======================================
    # GET SINGLE FACE
    # ======================================

    x, y, w, h = faces[0]

    print(
        f"Face detected: x={x}, y={y}, "
        f"width={w}, height={h}"
    )


    # ======================================
    # ADD SMALL PADDING
    # ======================================

    padding = 20

    x1 = max(
        0,
        x - padding
    )

    y1 = max(
        0,
        y - padding
    )

    x2 = min(
        gray.shape[1],
        x + w + padding
    )

    y2 = min(
        gray.shape[0],
        y + h + padding
    )


    # ======================================
    # CROP FACE
    # ======================================

    face_image = gray[
        y1:y2,
        x1:x2
    ]


    # ======================================
    # RESIZE FACE
    # ======================================

    face_image = cv2.resize(
        face_image,
        (200, 200)
    )


    # ======================================
    # IMPROVE FACE IMAGE
    # ======================================

    face_image = cv2.equalizeHist(
        face_image
    )


    # ======================================
    # SAVE EXACTLY ONE PHOTO
    # ======================================

    success = cv2.imwrite(
        filepath,
        face_image
    )


    if not success:

        return (
            False,
            "Could not save face photo."
        )


    # ======================================
    # SUCCESS
    # ======================================

    print(
        f"Face photo saved successfully: "
        f"{filepath}"
    )

    return (
        True,
        filename
    )