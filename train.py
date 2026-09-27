import os
import re
import cv2
import numpy as np


# =====================================================
# SUPABASE
# =====================================================

try:
    from supabase import create_client
except ImportError:
    print("ERROR: supabase package not installed.")
    print("Run: pip install supabase")
    exit()


SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()

SUPABASE_SERVICE_ROLE_KEY = os.getenv(
    "SUPABASE_SERVICE_ROLE_KEY",
    ""
).strip()

SUPABASE_BUCKET = "face-data"


if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:

    print("ERROR: Supabase environment variables are missing.")

    print(
        "SUPABASE_URL:",
        bool(SUPABASE_URL)
    )

    print(
        "SUPABASE_SERVICE_ROLE_KEY:",
        bool(SUPABASE_SERVICE_ROLE_KEY)
    )

    exit()


# =====================================================
# SUPABASE CONNECTION
# =====================================================

try:

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY
    )

    print("Supabase Storage connection ready!")

except Exception as e:

    print("ERROR: Supabase connection failed:")
    print(e)

    exit()


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


os.makedirs(
    DATASET_PATH,
    exist_ok=True
)


os.makedirs(
    TRAINER_PATH,
    exist_ok=True
)


# =====================================================
# CHECK LBPH
# =====================================================

if not hasattr(cv2, "face"):

    print("ERROR: cv2.face is not available.")
    print()
    print("Install:")
    print("pip install opencv-contrib-python")

    exit()


# =====================================================
# DOWNLOAD FACE PHOTOS FROM SUPABASE
# =====================================================

print()
print("==============================================")
print(" DOWNLOADING FACE PHOTOS FROM SUPABASE")
print("==============================================")
print()


try:

    storage = supabase.storage.from_(
        SUPABASE_BUCKET
    )


    files = storage.list("faces")


    if not files:

        print(
            "No files found in Supabase Storage."
        )

        exit()


    downloaded = 0


    for file_info in files:

        filename = file_info.get(
            "name",
            ""
        )


        # -----------------------------------------
        # ONLY IMAGE FILES
        # -----------------------------------------

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):

            continue


        # -----------------------------------------
        # ONLY ONE PHOTO PER STUDENT
        # -----------------------------------------

        match = re.match(
            r"^User\.(\d+)\.1\.(jpg|jpeg|png)$",
            filename,
            re.IGNORECASE
        )


        if not match:

            print(
                "Skipping invalid file:",
                filename
            )

            continue


        student_id = match.group(1)


        storage_path = (
            "faces/" + filename
        )


        try:

            image_bytes = storage.download(
                storage_path
            )


            local_path = os.path.join(
                DATASET_PATH,
                filename
            )


            with open(
                local_path,
                "wb"
            ) as f:

                f.write(
                    image_bytes
                )


            downloaded += 1


            print(
                "Downloaded:",
                filename
            )


        except Exception as e:

            print(
                "ERROR downloading:",
                filename
            )

            print(e)


    print()

    print(
        "Photos downloaded:",
        downloaded
    )


except Exception as e:

    print(
        "ERROR: Could not access Supabase Storage."
    )

    print(e)

    exit()


# =====================================================
# GET LOCAL DATASET
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

    print()
    print(
        "ERROR: No face images found."
    )

    exit()


image_files.sort()


# =====================================================
# HEADER
# =====================================================

print()
print("==============================================")
print("       FACE RECOGNITION TRAINING")
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
# ONE PHOTO PER STUDENT
# =====================================================

student_images = {}


pattern = re.compile(
    r"^User\.(\d+)\.1\.(jpg|jpeg|png)$",
    re.IGNORECASE
)


for filename in image_files:

    match = pattern.match(
        filename
    )


    if not match:

        print(
            "Skipping invalid file:",
            filename
        )

        continue


    student_id = int(
        match.group(1)
    )


    if student_id in student_images:

        print(
            f"Duplicate photo found "
            f"for Student ID {student_id}: "
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
# CHECK STUDENTS
# =====================================================

if not student_images:

    print(
        "ERROR: No valid student photos found."
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
        "Processing Student ID "
        f"{student_id}: {filename}"
    )


    # =================================================
    # READ CROPPED FACE IMAGE
    # =================================================

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


    print(
        f"Original image size: "
        f"{image.shape[1]} x {image.shape[0]}"
    )


    # =================================================
    # HISTOGRAM EQUALIZATION
    # =================================================

    image = cv2.equalizeHist(
        image
    )


    # =================================================
    # RESIZE
    # =================================================

    face_image = cv2.resize(
        image,
        (200, 200)
    )


    # =================================================
    # VALIDATE
    # =================================================

    if face_image.size == 0:

        print(
            "ERROR: Invalid image:",
            filename
        )

        continue


    # =================================================
    # ADD TRAINING DATA
    # =================================================

    faces.append(
        face_image
    )


    ids.append(
        student_id
    )


    print(
        f"Added Student ID {student_id}"
    )

    print(
        "Face detection skipped "
        "(image is already cropped)."
    )

    print()


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
# CREATE LBPH
# =====================================================

recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8
)


# =====================================================
# TRAIN
# =====================================================

print()
print(
    "=============================================="
)

print(
    "Training started..."
)

print(
    "=============================================="
)

print()


recognizer.train(
    faces,
    ids
)


# =====================================================
# SAVE LOCAL TRAINER
# =====================================================

recognizer.write(
    TRAINER_FILE
)


print()

print(
    "Local trainer created:"
)

print(
    TRAINER_FILE
)


# =====================================================
# UPLOAD TRAINER TO SUPABASE
# =====================================================

print()

print(
    "Uploading trainer.yml to Supabase Storage..."
)


try:

    with open(
        TRAINER_FILE,
        "rb"
    ) as f:

        trainer_bytes = f.read()


    storage.upload(
        "trainer/trainer.yml",
        trainer_bytes,
        {
            "content-type":
            "application/octet-stream",

            "upsert":
            "true"
        }
    )


    print()

    print(
        "Trainer uploaded successfully!"
    )

    print(
        "Storage path:"
    )

    print(
        "face-data/trainer/trainer.yml"
    )


except Exception as e:

    print()

    print(
        "ERROR: Trainer upload failed:"
    )

    print(e)


# =====================================================
# FINAL RESULT
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
    sorted(
        ids.tolist()
    )
)


print()

print(
    "Training successful!"
)