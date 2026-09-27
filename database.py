import sqlite3
from datetime import datetime
import os

DB_PATH = "attendance.db"


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


# -------------------------------------------------
# CREATE DATABASE / TABLES
# -------------------------------------------------

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            course TEXT NOT NULL,
            photo TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'Present',
            UNIQUE(student_id, date)
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------------------------
# ADD STUDENT
# -------------------------------------------------

def add_student(student_id, name, roll_no, course, photo=""):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            (student_id, name, roll_no, course, photo)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, name, roll_no, course, photo))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# -------------------------------------------------
# GET ALL STUDENTS
# -------------------------------------------------

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, name, roll_no, course, photo
        FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    conn.close()

    return students


# -------------------------------------------------
# GET ONE STUDENT
# -------------------------------------------------

def get_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, name, roll_no, course, photo
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    student = cursor.fetchone()

    conn.close()

    return student


# -------------------------------------------------
# GET TOTAL STUDENTS
# -------------------------------------------------

def get_total_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM students
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# -------------------------------------------------
# GET TODAY'S PRESENT STUDENTS
# -------------------------------------------------

def get_present_today():
    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE date = ?
        AND status = 'Present'
    """, (today,))

    total = cursor.fetchone()[0]

    conn.close()

    return total


# -------------------------------------------------
# GET TOTAL ATTENDANCE
# -------------------------------------------------

def get_total_attendance():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status = 'Present'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# -------------------------------------------------
# OVERALL ATTENDANCE PERCENTAGE
# -------------------------------------------------

def get_attendance_percentage():

    total_students = get_total_students()

    if total_students == 0:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    # Total attendance days
    cursor.execute("""
        SELECT COUNT(DISTINCT date)
        FROM attendance
    """)

    total_days = cursor.fetchone()[0]

    if total_days == 0:
        conn.close()
        return 0

    # Maximum possible attendance
    maximum_attendance = total_students * total_days

    # Actual attendance
    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status = 'Present'
    """)

    actual_attendance = cursor.fetchone()[0]

    conn.close()

    percentage = (actual_attendance / maximum_attendance) * 100

    return round(percentage, 2)


# -------------------------------------------------
# STUDENT ATTENDANCE PERCENTAGE
# -------------------------------------------------

def get_student_attendance_percentage(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Total attendance days
    cursor.execute("""
        SELECT COUNT(DISTINCT date)
        FROM attendance
    """)

    total_days = cursor.fetchone()[0]

    if total_days == 0:
        conn.close()
        return 0

    # Student's present days
    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE student_id = ?
        AND status = 'Present'
    """, (student_id,))

    present_days = cursor.fetchone()[0]

    conn.close()

    percentage = (present_days / total_days) * 100

    return round(percentage, 2)


# -------------------------------------------------
# SAVE ATTENDANCE
# -------------------------------------------------

def save_attendance(student_id, name):

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO attendance
            (student_id, name, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            student_id,
            name,
            today,
            current_time,
            "Present"
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        # Already marked present today
        return False

    finally:
        conn.close()


# -------------------------------------------------
# GET ALL ATTENDANCE
# -------------------------------------------------

def get_all_attendance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_id,
            name,
            date,
            time,
            status
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    attendance = cursor.fetchall()

    conn.close()

    return attendance


# -------------------------------------------------
# GET STUDENT ATTENDANCE
# -------------------------------------------------

def get_student_attendance(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_id,
            name,
            date,
            time,
            status
        FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC, time DESC
    """, (student_id,))

    attendance = cursor.fetchall()

    conn.close()

    return attendance


# -------------------------------------------------
# UPDATE STUDENT
# -------------------------------------------------

def update_student(student_id, name, roll_no, course):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET
            name = ?,
            roll_no = ?,
            course = ?
        WHERE student_id = ?
    """, (
        name,
        roll_no,
        course,
        student_id
    ))

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# -------------------------------------------------
# DELETE STUDENT
# -------------------------------------------------

def delete_student(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Delete student's attendance first
        cursor.execute("""
            DELETE FROM attendance
            WHERE student_id = ?
        """, (student_id,))

        # Delete student
        cursor.execute("""
            DELETE FROM students
            WHERE student_id = ?
        """, (student_id,))

        conn.commit()

        deleted = cursor.rowcount > 0

        return deleted

    finally:
        conn.close()


# -------------------------------------------------
# UPDATE STUDENT PHOTO
# -------------------------------------------------

def update_student_photo(student_id, photo):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET photo = ?
        WHERE student_id = ?
    """, (photo, student_id))

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# -------------------------------------------------
# INITIALIZE DATABASE
# -------------------------------------------------

create_database()