from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    Response
)

import os
import csv
import io
import sqlite3
from datetime import datetime

import cv2
import numpy as np

import database
from face_capture import save_face_image


# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "face_attendance_secret_key_change_this"
)


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_FOLDER = os.path.join(
    BASE_DIR,
    "dataset"
)

TRAINER_FOLDER = os.path.join(
    BASE_DIR,
    "trainer"
)

TRAINER_FILE = os.path.join(
    TRAINER_FOLDER,
    "trainer.yml"
)

CASCADE_PATH = os.path.join(
    cv2.data.haarcascades,
    "haarcascade_frontalface_default.xml"
)


# =====================================================
# CREATE REQUIRED FOLDERS
# =====================================================

os.makedirs(
    DATASET_FOLDER,
    exist_ok=True
)

os.makedirs(
    TRAINER_FOLDER,
    exist_ok=True
)


# =====================================================
# CREATE DATABASE
# =====================================================

database.create_database()


# =====================================================
# LOGIN CHECK
# =====================================================

def admin_required():

    return session.get(
        "admin_logged_in",
        False
    )


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================
# LOGIN
# =====================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()


        # ---------------------------------------------
        # DEFAULT ADMIN LOGIN
        # ---------------------------------------------

        if (
            username == "admin"
            and password == "admin123"
        ):

            session[
                "admin_logged_in"
            ] = True

            return redirect(
                url_for("dashboard")
            )


        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )


    return render_template(
        "login.html"
    )


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    if not admin_required():

        return redirect(
            url_for("login")
        )


    total_students = (
        database.get_total_students()
    )


    present_today = (
        database.get_present_today()
    )


    total_attendance = (
        database.get_total_attendance()
    )


    attendance_percentage = (
        database.get_attendance_percentage()
    )


    today = datetime.now().strftime(
        "%d-%m-%Y"
    )


    return render_template(
        "dashboard.html",

        total_students=total_students,

        present_today=present_today,

        total_attendance=total_attendance,

        attendance_percentage=
            attendance_percentage,

        today=today
    )


# =====================================================
# REGISTER STUDENT
# =====================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if not admin_required():

        return redirect(
            url_for("login")
        )


    if request.method == "POST":

        student_id = request.form.get(
            "student_id",
            ""
        ).strip()

        name = request.form.get(
            "name",
            ""
        ).strip()

        roll_no = request.form.get(
            "roll_no",
            ""
        ).strip()

        course = request.form.get(
            "course",
            ""
        ).strip()


        # ---------------------------------------------
        # VALIDATION
        # ---------------------------------------------

        if not student_id:

            return render_template(
                "register.html",
                error="Please enter Student ID."
            )


        if not name:

            return render_template(
                "register.html",
                error="Please enter Student Name."
            )


        if not roll_no:

            return render_template(
                "register.html",
                error="Please enter Roll Number."
            )


        if not course:

            return render_template(
                "register.html",
                error="Please select Course."
            )


        # ---------------------------------------------
        # CHECK DUPLICATE STUDENT ID
        # ---------------------------------------------

        existing = database.get_student(
            student_id
        )


        if existing:

            return render_template(
                "register.html",
                error=(
                    f"Student ID {student_id} "
                    "already exists."
                )
            )


        # ---------------------------------------------
        # ADD STUDENT
        # ---------------------------------------------

        try:

            success = database.add_student(
                student_id,
                name,
                roll_no,
                course,
                ""
            )


            if not success:

                return render_template(
                    "register.html",
                    error=(
                        f"Student ID {student_id} "
                        "already exists."
                    )
                )


            # -----------------------------------------
            # REGISTRATION SUCCESS
            # -----------------------------------------

            return render_template(
                "success.html",

                student_id=student_id,

                name=name
            )


        except Exception as e:

            print(
                "Registration Error:",
                e
            )

            return render_template(
                "register.html",
                error=(
                    "Student registration failed."
                )
            )


    return render_template(
        "register.html"
    )


# =====================================================
# STUDENT LIST
# =====================================================

@app.route("/students")
def students():

    if not admin_required():

        return redirect(
            url_for("login")
        )


    students_data = (
        database.get_all_students()
    )


    students_with_percentage = []


    for student in students_data:

        student_id = student[0]


        percentage = (
            database
            .get_student_attendance_percentage(
                student_id
            )
        )


        students_with_percentage.append(
            (
                student[0],
                student[1],
                student[2],
                student[3],
                percentage
            )
        )


    return render_template(
        "students.html",
        students=students_with_percentage
    )


# =====================================================
# STUDENT PROFILE
# =====================================================

@app.route(
    "/student/<student_id>"
)
def student_profile(student_id):

    if not admin_required():

        return redirect(
            url_for("login")
        )


    student = database.get_student(
        student_id
    )


    if not student:

        return redirect(
            url_for("students")
        )


    attendance = (
        database.get_student_attendance(
            student_id
        )
    )


    percentage = (
        database
        .get_student_attendance_percentage(
            student_id
        )
    )


    return render_template(
        "student_profile.html",

        student=student,

        attendance=attendance,

        percentage=percentage
    )


# =====================================================
# EDIT STUDENT
# =====================================================

@app.route(
    "/edit-student/<student_id>",
    methods=["GET", "POST"]
)
def edit_student(student_id):

    if not admin_required():

        return redirect(
            url_for("login")
        )


    student = database.get_student(
        student_id
    )


    if not student:

        return redirect(
            url_for("students")
        )


    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        roll_no = request.form.get(
            "roll_no",
            ""
        ).strip()

        course = request.form.get(
            "course",
            ""
        ).strip()


        if (
            not name
            or not roll_no
            or not course
        ):

            return render_template(
                "edit_student.html",

                student=student,

                error=(
                    "All fields are required."
                )
            )


        database.update_student(
            student_id,
            name,
            roll_no,
            course
        )


        return redirect(
            url_for(
                "student_profile",
                student_id=student_id
            )
        )


    return render_template(
        "edit_student.html",
        student=student
    )


# =====================================================
# DELETE STUDENT
# =====================================================

@app.route(
    "/delete-student/<student_id>",
    methods=["POST"]
)
def delete_student(student_id):

    if not admin_required():

        return redirect(
            url_for("login")
        )


    # ---------------------------------------------
    # DELETE DATABASE DATA
    # ---------------------------------------------

    database.delete_student(
        student_id
    )


    # ---------------------------------------------
    # DELETE ONE FACE PHOTO
    # ---------------------------------------------

    filename = (
        f"User.{student_id}.1.jpg"
    )


    filepath = os.path.join(
        DATASET_FOLDER,
        filename
    )


    if os.path.exists(filepath):

        try:

            os.remove(
                filepath
            )

        except Exception as e:

            print(
                "Face photo delete error:",
                e
            )


    # ---------------------------------------------
    # OLD EXTRA PHOTOS IF ANY
    # ---------------------------------------------

    if os.path.exists(
        DATASET_FOLDER
    ):

        prefix = (
            f"User.{student_id}."
        )


        for filename in os.listdir(
            DATASET_FOLDER
        ):

            if filename.startswith(
                prefix
            ):

                filepath = os.path.join(
                    DATASET_FOLDER,
                    filename
                )


                try:

                    os.remove(
                        filepath
                    )

                except Exception as e:

                    print(
                        "Extra photo delete error:",
                        e
                    )


    return redirect(
        url_for("students")
    )


# =====================================================
# FACE CAPTURE PAGE
# =====================================================

@app.route(
    "/capture/<student_id>"
)
def capture(student_id):

    if not admin_required():

        return redirect(
            url_for("login")
        )


    student = database.get_student(
        student_id
    )


    if not student:

        return redirect(
            url_for("register")
        )


    return render_template(
        "camera.html",

        student_id=student_id
    )


# =====================================================
# SAVE FACE PHOTO
# ONLY ONE PHOTO
# =====================================================

@app.route(
    "/save-face",
    methods=["POST"]
)
def save_face():

    if not admin_required():

        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401


    student_id = request.form.get(
        "student_id",
        ""
    ).strip()


    image = request.files.get(
        "image"
    )


    # ---------------------------------------------
    # VALIDATION
    # ---------------------------------------------

    if not student_id:

        return jsonify({
            "success": False,
            "message": "Student ID is required."
        }), 400


    if image is None:

        return jsonify({
            "success": False,
            "message": "Image not received."
        }), 400


    # ---------------------------------------------
    # CHECK STUDENT
    # ---------------------------------------------

    student = database.get_student(
        student_id
    )


    if not student:

        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404


    # ---------------------------------------------
    # ONE PHOTO ONLY
    # ---------------------------------------------

    existing_photo = os.path.join(
        DATASET_FOLDER,
        f"User.{student_id}.1.jpg"
    )


    if os.path.exists(
        existing_photo
    ):

        return jsonify({
            "success": False,
            "message": (
                "Face photo already exists "
                "for this Student ID."
            )
        })


    # ---------------------------------------------
    # READ IMAGE
    # ---------------------------------------------

    try:

        image_bytes = image.read()


        success, message = (
            save_face_image(
                student_id,
                image_bytes
            )
        )


        if not success:

            return jsonify({
                "success": False,
                "message": message
            })


        return jsonify({

            "success": True,

            "message": (
                "Face photo captured "
                "successfully."
            ),

            "filename": message

        })


    except Exception as e:

        print(
            "Face Save Error:",
            e
        )


        return jsonify({
            "success": False,
            "message": "Face photo could not be saved."
        }), 500


# =====================================================
# ATTENDANCE CAMERA PAGE
# =====================================================

@app.route(
    "/attendance"
)
def attendance():

    if not admin_required():

        return redirect(
            url_for("login")
        )


    return render_template(
        "attendance_camera.html"
    )


# =====================================================
# FACE RECOGNITION
# =====================================================

@app.route(
    "/recognize-face",
    methods=["POST"]
)
def recognize_face():

    if not admin_required():

        return jsonify({
            "success": False,
            "recognized": False,
            "message": "Unauthorized"
        }), 401


    try:

        # -----------------------------------------
        # CHECK TRAINER
        # -----------------------------------------

        if not os.path.exists(
            TRAINER_FILE
        ):

            return jsonify({

                "success": False,

                "recognized": False,

                "message": (
                    "Trainer file not found. "
                    "Please run train.py first."
                )
            })


        # -----------------------------------------
        # CHECK IMAGE
        # -----------------------------------------

        image_file = request.files.get(
            "image"
        )


        if image_file is None:

            return jsonify({

                "success": False,

                "recognized": False,

                "message": "Image not received."
            }), 400


        image_bytes = image_file.read()


        if not image_bytes:

            return jsonify({

                "success": False,

                "recognized": False,

                "message": "Empty image."
            }), 400


        # -----------------------------------------
        # DECODE IMAGE
        # -----------------------------------------

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )


        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )


        if frame is None:

            return jsonify({

                "success": False,

                "recognized": False,

                "message": "Invalid image."
            }), 400


        # -----------------------------------------
        # GRAYSCALE
        # -----------------------------------------

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )


        gray = cv2.equalizeHist(
            gray
        )


        # -----------------------------------------
        # LOAD FACE DETECTOR
        # -----------------------------------------

        detector = cv2.CascadeClassifier(
            CASCADE_PATH
        )


        if detector.empty():

            return jsonify({

                "success": False,

                "recognized": False,

                "message": (
                    "Haar Cascade could not "
                    "be loaded."
                )
            }), 500


        # -----------------------------------------
        # DETECT FACE
        # -----------------------------------------

        faces = detector.detectMultiScale(
            gray,

            scaleFactor=1.1,

            minNeighbors=5,

            minSize=(80, 80)
        )


        if len(faces) == 0:

            return jsonify({

                "success": False,

                "recognized": False,

                "message": "No face detected."
            })


        # -----------------------------------------
        # ONLY ONE FACE
        # -----------------------------------------

        if len(faces) > 1:

            return jsonify({

                "success": False,

                "recognized": False,

                "message": (
                    "More than one face detected. "
                    "Please keep only one person "
                    "in front of the camera."
                )
            })


        # -----------------------------------------
        # OPENCV CONTRIB CHECK
        # -----------------------------------------

        if not hasattr(
            cv2,
            "face"
        ):

            return jsonify({

                "success": False,

                "recognized": False,

                "message": (
                    "opencv-contrib-python "
                    "is required."
                )
            }), 500


        # -----------------------------------------
        # CREATE RECOGNIZER
        # -----------------------------------------

        recognizer = (
            cv2.face
            .LBPHFaceRecognizer_create()
        )


        # -----------------------------------------
        # LOAD TRAINER
        # -----------------------------------------

        recognizer.read(
            TRAINER_FILE
        )


        # -----------------------------------------
        # GET FACE
        # -----------------------------------------

        x, y, w, h = faces[0]


        face_image = gray[
            y:y + h,
            x:x + w
        ]


        face_image = cv2.resize(
            face_image,
            (200, 200)
        )


        face_image = cv2.equalizeHist(
            face_image
        )


        # -----------------------------------------
        # PREDICT
        # -----------------------------------------

        student_id, confidence = (
            recognizer.predict(
                face_image
            )
        )


        print(
            "Detected ID:",
            student_id
        )

        print(
            "Confidence:",
            confidence
        )


        # -----------------------------------------
        # CONFIDENCE CHECK
        # -----------------------------------------

        # LBPH:
        # lower confidence = better match

        MAX_CONFIDENCE = 75


        if confidence > MAX_CONFIDENCE:

            return jsonify({

                "success": False,

                "recognized": False,

                "message": (
                    "Face not recognized."
                )
            })


        # -----------------------------------------
        # GET STUDENT FROM DATABASE
        # -----------------------------------------

        student = database.get_student(
            str(student_id)
        )


        if not student:

            return jsonify({

                "success": False,

                "recognized": False,

                "message": (
                    "Recognized face does not "
                    "belong to a registered student."
                )
            })


        # student:
        # 0 = student_id
        # 1 = name
        # 2 = roll_no
        # 3 = course


        # -----------------------------------------
        # SAVE ATTENDANCE
        # -----------------------------------------

        attendance_saved = (
            database.save_attendance(
                student[0],
                student[1]
            )
        )


        if attendance_saved:

            message = (
                "Attendance marked successfully."
            )

        else:

            message = (
                "Attendance already marked "
                "for today."
            )


        # -----------------------------------------
        # RESPONSE
        # -----------------------------------------

        return jsonify({

            "success": True,

            "recognized": True,

            "student_id": student[0],

            "name": student[1],

            "roll_no": student[2],

            "course": student[3],

            "confidence": round(
                float(confidence),
                2
            ),

            "attendance_saved":
                attendance_saved,

            "message": message
        })


    except Exception as e:

        print(
            "Recognition Error:",
            e
        )


        return jsonify({

            "success": False,

            "recognized": False,

            "message": (
                "Face recognition error."
            )
        }), 500


# =====================================================
# VIEW ATTENDANCE
# =====================================================

@app.route(
    "/view-attendance"
)
def view_attendance():

    if not admin_required():

        return redirect(
            url_for("login")
        )


    attendance_data = (
        database.get_all_attendance()
    )


    return render_template(
        "attendance.html",

        attendance=attendance_data
    )


# =====================================================
# CSV EXPORT
# =====================================================

@app.route(
    "/export-attendance"
)
def export_attendance():

    if not admin_required():

        return redirect(
            url_for("login")
        )


    records = (
        database.get_all_attendance()
    )


    output = io.StringIO()


    writer = csv.writer(
        output
    )


    # ---------------------------------------------
    # HEADER
    # ---------------------------------------------

    writer.writerow([
        "Student ID",
        "Name",
        "Date",
        "Time",
        "Status"
    ])


    # ---------------------------------------------
    # DATA
    # ---------------------------------------------

    for row in records:

        # Expected database row:
        # student_id, name, date, time, status

        writer.writerow([
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        ])


    output.seek(0)


    return Response(

        output.getvalue(),

        mimetype="text/csv",

        headers={
            "Content-Disposition":
                "attachment; "
                "filename=attendance.csv"
        }
    )


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route(
    "/health"
)
def health():

    return jsonify({
        "status": "ok",
        "message": "Face Attendance System is running."
    })


# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "index.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    print(
        "500 Error:",
        error
    )

    return jsonify({
        "success": False,
        "message": "Internal server error."
    }), 500


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )