import cv2
import os
import numpy as np
from PIL import Image

import database



# =========================
# PATH
# =========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


TRAINER_FILE = os.path.join(
    BASE_DIR,
    "trainer",
    "trainer.yml"
)



# =========================
# LOAD MODEL
# =========================

def load_model():


    if not os.path.exists(TRAINER_FILE):

        print(
            "Trainer file not found"
        )

        return None, None



    recognizer = cv2.face.LBPHFaceRecognizer_create()


    recognizer.read(
        TRAINER_FILE
    )


    detector = cv2.CascadeClassifier(

        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"

    )


    return recognizer, detector




# =========================
# RECOGNIZE UPLOADED IMAGE
# =========================

def recognize_uploaded_face(image_path):


    recognizer, detector = load_model()



    if recognizer is None:


        return {

            "recognized":False,

            "message":"Trainer not found. Train model first."

        }



    img = Image.open(
        image_path
    ).convert(
        "L"
    )



    img_numpy = np.array(
        img,
        "uint8"
    )



    faces = detector.detectMultiScale(

        img_numpy,

        scaleFactor=1.2,

        minNeighbors=5

    )



    if len(faces)==0:


        return {

            "recognized":False,

            "message":"No face detected"

        }





    for (x,y,w,h) in faces:


        student_id, confidence = recognizer.predict(

            img_numpy[y:y+h, x:x+w]

        )



        print(
            "Detected ID:",
            student_id,
            "Confidence:",
            confidence
        )



        # confidence low means better match

        if confidence < 70:



            student = database.get_student(

                student_id

            )



            if student:



                database.save_attendance(

                    student[1],

                    student[2]

                )



                return {


                    "recognized":True,


                    "student_id":student[1],


                    "name":student[2],


                    "roll_no":student[3],


                    "course":student[4],


                    "message":"Attendance Marked Successfully"

                }





    return {


        "recognized":False,


        "message":"Unknown Face"

    }