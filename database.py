import os
from datetime import datetime

from supabase import create_client, Client


# =====================================================
# SUPABASE CONNECTION
# =====================================================

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY"
)

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL environment variable is missing.")

if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError(
        "SUPABASE_SERVICE_ROLE_KEY environment variable is missing."
    )

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)


# =====================================================
# CREATE / CHECK DATABASE
# =====================================================

def create_database():
    """
    Supabase tables are created from the Supabase SQL Editor.
    This function only checks that the required tables are reachable.
    """

    try:
        supabase.table("students").select(
            "student_id"
        ).limit(1).execute()

        supabase.table("attendance").select(
            "student_id"
        ).limit(1).execute()

        print("Supabase database connection ready!")

    except Exception as e:
        print("Supabase database check failed:", e)
        raise


# =====================================================
# ADD STUDENT
# =====================================================

def add_student(
    student_id,
    name,
    roll_no,
    course,
    photo=""
):

    data = {
        "student_id": str(student_id),
        "name": name,
        "roll_no": roll_no,
        "course": course,
        "photo": photo or ""
    }

    response = (
        supabase
        .table("students")
        .insert(data)
        .execute()
    )

    return response.data


# =====================================================
# GET ONE STUDENT
# =====================================================

def get_student(student_id):

    response = (
        supabase
        .table("students")
        .select(
            "student_id,name,roll_no,course"
        )
        .eq("student_id", str(student_id))
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    student = response.data[0]

    return (
        student.get("student_id"),
        student.get("name"),
        student.get("roll_no"),
        student.get("course")
    )


# =====================================================
# GET ALL STUDENTS
# =====================================================

def get_all_students():

    response = (
        supabase
        .table("students")
        .select(
            "student_id,name,roll_no,course"
        )
        .order("student_id")
        .execute()
    )

    return [
        (
            row.get("student_id"),
            row.get("name"),
            row.get("roll_no"),
            row.get("course")
        )
        for row in (response.data or [])
    ]


# =====================================================
# UPDATE STUDENT
# =====================================================

def update_student(
    student_id,
    name,
    roll_no,
    course
):

    response = (
        supabase
        .table("students")
        .update({
            "name": name,
            "roll_no": roll_no,
            "course": course
        })
        .eq("student_id", str(student_id))
        .execute()
    )

    return response.data


# =====================================================
# DELETE STUDENT
# =====================================================

def delete_student(student_id):

    student_id = str(student_id)

    # Delete attendance first
    supabase.table("attendance").delete().eq(
        "student_id",
        student_id
    ).execute()

    # Delete student
    response = (
        supabase
        .table("students")
        .delete()
        .eq("student_id", student_id)
        .execute()
    )

    return response.data


# =====================================================
# STUDENT ATTENDANCE
# =====================================================

def get_student_attendance(student_id):

    response = (
        supabase
        .table("attendance")
        .select(
            "student_id,name,date,time,status"
        )
        .eq("student_id", str(student_id))
        .order("date", desc=True)
        .order("time", desc=True)
        .execute()
    )

    return [
        (
            row.get("student_id"),
            row.get("name"),
            row.get("date"),
            row.get("time"),
            row.get("status")
        )
        for row in (response.data or [])
    ]


# =====================================================
# STUDENT ATTENDANCE %
# =====================================================

def get_student_attendance_percentage(student_id):

    student_id = str(student_id)

    # Get all distinct attendance dates
    all_attendance = (
        supabase
        .table("attendance")
        .select("date")
        .execute()
    )

    dates = {
        row.get("date")
        for row in (all_attendance.data or [])
        if row.get("date")
    }

    total_days = len(dates)

    if total_days == 0:
        return 0

    # Get student's present attendance
    present_response = (
        supabase
        .table("attendance")
        .select("id", count="exact")
        .eq("student_id", student_id)
        .eq("status", "Present")
        .execute()
    )

    present_days = present_response.count or 0

    percentage = (
        present_days / total_days
    ) * 100

    return round(percentage, 2)


# =====================================================
# MARK ATTENDANCE
# =====================================================

def mark_attendance(student_id, name):

    student_id = str(student_id)

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Do not mark the same student twice on the same date.
    existing = (
        supabase
        .table("attendance")
        .select("id")
        .eq("student_id", student_id)
        .eq("date", date)
        .limit(1)
        .execute()
    )

    if existing.data:
        return False

    data = {
        "student_id": student_id,
        "name": name,
        "date": date,
        "time": time,
        "status": "Present"
    }

    try:
        (
            supabase
            .table("attendance")
            .insert(data)
            .execute()
        )

        return True

    except Exception as e:

        # The database also has UNIQUE(student_id, date),
        # so concurrent duplicate requests are safely rejected.
        error_text = str(e).lower()

        if (
            "duplicate" in error_text
            or "unique" in error_text
        ):
            return False

        raise


# =====================================================
# SAVE ATTENDANCE
# =====================================================

def save_attendance(student_id, name):
    return mark_attendance(student_id, name)


# =====================================================
# ALL ATTENDANCE
# =====================================================

def get_all_attendance():

    response = (
        supabase
        .table("attendance")
        .select(
            "student_id,name,date,time,status"
        )
        .order("date", desc=True)
        .order("time", desc=True)
        .execute()
    )

    return [
        (
            row.get("student_id"),
            row.get("name"),
            row.get("date"),
            row.get("time"),
            row.get("status")
        )
        for row in (response.data or [])
    ]


# =====================================================
# TOTAL STUDENTS
# =====================================================

def get_total_students():

    response = (
        supabase
        .table("students")
        .select("id", count="exact")
        .execute()
    )

    return response.count or 0


# =====================================================
# PRESENT TODAY
# =====================================================

def get_present_today():

    today = datetime.now().strftime("%Y-%m-%d")

    response = (
        supabase
        .table("attendance")
        .select("id", count="exact")
        .eq("date", today)
        .eq("status", "Present")
        .execute()
    )

    return response.count or 0


# =====================================================
# TOTAL ATTENDANCE
# =====================================================

def get_total_attendance():

    response = (
        supabase
        .table("attendance")
        .select("id", count="exact")
        .eq("status", "Present")
        .execute()
    )

    return response.count or 0


# =====================================================
# OVERALL ATTENDANCE %
# =====================================================

def get_attendance_percentage():

    total_students = get_total_students()

    if total_students == 0:
        return 0

    # Get all distinct attendance dates
    all_attendance = (
        supabase
        .table("attendance")
        .select("date")
        .execute()
    )

    dates = {
        row.get("date")
        for row in (all_attendance.data or [])
        if row.get("date")
    }

    total_days = len(dates)

    if total_days == 0:
        return 0

    total_possible_attendance = (
        total_students * total_days
    )

    total_present = get_total_attendance()

    percentage = (
        total_present / total_possible_attendance
    ) * 100

    return round(percentage, 2)


# =====================================================
# ATTENDANCE BY DATE
# =====================================================

def get_attendance_by_date(date):

    response = (
        supabase
        .table("attendance")
        .select(
            "student_id,name,date,time,status"
        )
        .eq("date", date)
        .order("time", desc=True)
        .execute()
    )

    return [
        (
            row.get("student_id"),
            row.get("name"),
            row.get("date"),
            row.get("time"),
            row.get("status")
        )
        for row in (response.data or [])
    ]


# =====================================================
# START / CHECK DATABASE
# =====================================================

if __name__ == "__main__":
    create_database()