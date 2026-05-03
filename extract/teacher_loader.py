import csv
from datetime import datetime
from pathlib import Path
from db import get_connection, get_supabase_connection
from logger import get_logger

logger = get_logger("teacher_loader")

# =========================
# ERROR LOGGING
# =========================

ERROR_LOG_DIR = Path(__file__).resolve().parent / "logs"
ERROR_LOG_DIR.mkdir(exist_ok=True)

ERROR_FILE = ERROR_LOG_DIR / f"teacher_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


def log_error(teacher, tab, row_idx, field, value, message):
    is_new = not ERROR_FILE.exists()
    with open(ERROR_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["teacher", "tab", "row", "field", "value", "error"])
        writer.writerow([teacher, tab, row_idx + 2, field, value, message])


# =========================
# HELPERS
# =========================

def normalize_text(value):
    if value is None:
        return None
    return str(value).strip().lower()


def parse_date(value):
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except Exception:
        return None


def to_bool(value):
    try:
        return str(value).strip() in ("1", "true", "True")
    except Exception:
        return False


def get_all_connections():
    """
    Local Postgres = PRIMARY (must succeed)
    Supabase = REPLICA (best‑effort)
    """
    connections = [("local", get_connection())]

    try:
        connections.append(("supabase", get_supabase_connection()))
    except Exception as e:
        logger.warning(f"Supabase unavailable for teacher load: {e}")

    return connections


# =========================
# SEMESTER VALIDATION ✅
# =========================

def semester_matches(cur, student_id, subject_id):
    """
    Ensure student.semester_id == subject.semester_id
    """
    cur.execute(
        """
        SELECT 1
        FROM students s
        JOIN subjects sub ON sub.subject_id = %s
        WHERE s.student_id = %s
          AND s.semester_id = sub.semester_id
        """,
        (subject_id, student_id)
    )
    return cur.fetchone() is not None


# =========================
# MARKS
# =========================

def load_marks(df, teacher_name):
    for name, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for idx, row in df.iterrows():

                    # Student
                    cur.execute(
                        "SELECT student_id FROM students WHERE registration_number = %s",
                        (str(row["registration_number"]),)
                    )
                    s = cur.fetchone()
                    if not s:
                        log_error(teacher_name, "marks", idx,
                                  "registration_number", row["registration_number"],
                                  "Student not found")
                        continue
                    student_id = s[0]

                    # Subject
                    cur.execute(
                        "SELECT subject_id FROM subjects WHERE subject_code = %s",
                        (normalize_text(row["subject_code"]),)
                    )
                    sub = cur.fetchone()
                    if not sub:
                        log_error(teacher_name, "marks", idx,
                                  "subject_code", row["subject_code"],
                                  "Subject not found")
                        continue
                    subject_id = sub[0]

                    # Semester validation ✅
                    if not semester_matches(cur, student_id, subject_id):
                        log_error(teacher_name, "marks", idx,
                                  "subject_code", row["subject_code"],
                                  "Semester mismatch")
                        continue

                    # Exam
                    cur.execute(
                        "SELECT exam_id FROM exams WHERE exam_name = %s",
                        (normalize_text(row["exam_name"]),)
                    )
                    ex = cur.fetchone()
                    if not ex:
                        log_error(teacher_name, "marks", idx,
                                  "exam_name", row["exam_name"],
                                  "Exam not found")
                        continue
                    exam_id = ex[0]

                    # Insert
                    cur.execute(
                        """
                        INSERT INTO marks (student_id, subject_id, exam_id, marks)
                        VALUES (%s,%s,%s,%s)
                        ON CONFLICT (student_id, subject_id, exam_id)
                        DO UPDATE SET marks = EXCLUDED.marks
                        """,
                        (student_id, subject_id, exam_id, int(row["marks"]))
                    )

        conn.close()
        logger.info(f"Marks loaded into {name}")


# =========================
# THEORY ATTENDANCE
# =========================

def load_theory_attendance(df, teacher_name):
    for name, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for idx, row in df.iterrows():

                    cur.execute(
                        "SELECT student_id FROM students WHERE registration_number = %s",
                        (str(row["registration_number"]),)
                    )
                    s = cur.fetchone()
                    if not s:
                        log_error(teacher_name, "theory_attendance", idx,
                                  "registration_number", row["registration_number"],
                                  "Student not found")
                        continue
                    student_id = s[0]

                    cur.execute(
                        "SELECT subject_id FROM subjects WHERE subject_code = %s",
                        (normalize_text(row["subject_code"]),)
                    )
                    sub = cur.fetchone()
                    if not sub:
                        log_error(teacher_name, "theory_attendance", idx,
                                  "subject_code", row["subject_code"],
                                  "Subject not found")
                        continue
                    subject_id = sub[0]

                    if not semester_matches(cur, student_id, subject_id):
                        log_error(teacher_name, "theory_attendance", idx,
                                  "subject_code", row["subject_code"],
                                  "Semester mismatch")
                        continue

                    cur.execute(
                        """
                        INSERT INTO theory_attendance
                        (student_id, subject_id, attendance_date, is_present)
                        VALUES (%s,%s,%s,%s)
                        ON CONFLICT (student_id, subject_id, attendance_date)
                        DO NOTHING
                        """,
                        (
                            student_id,
                            subject_id,
                            parse_date(row["attendance_date"]),
                            to_bool(row["is_present"])
                        )
                    )

        conn.close()
        logger.info(f"Theory attendance loaded into {name}")


# =========================
# LAB ATTENDANCE
# =========================

def load_lab_attendance(df, teacher_name):
    for name, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for idx, row in df.iterrows():

                    cur.execute(
                        "SELECT student_id FROM students WHERE registration_number = %s",
                        (str(row["registration_number"]),)
                    )
                    s = cur.fetchone()
                    if not s:
                        log_error(teacher_name, "lab_attendance", idx,
                                  "registration_number", row["registration_number"],
                                  "Student not found")
                        continue
                    student_id = s[0]

                    cur.execute(
                        "SELECT subject_id FROM subjects WHERE subject_code = %s",
                        (normalize_text(row["subject_code"]),)
                    )
                    sub = cur.fetchone()
                    if not sub:
                        log_error(teacher_name, "lab_attendance", idx,
                                  "subject_code", row["subject_code"],
                                  "Subject not found")
                        continue
                    subject_id = sub[0]

                    if not semester_matches(cur, student_id, subject_id):
                        log_error(teacher_name, "lab_attendance", idx,
                                  "subject_code", row["subject_code"],
                                  "Semester mismatch")
                        continue

                    cur.execute(
                        """
                        INSERT INTO lab_attendance
                        (student_id, subject_id, attendance_date, is_present)
                        VALUES (%s,%s,%s,%s)
                        ON CONFLICT (student_id, subject_id, attendance_date)
                        DO NOTHING
                        """,
                        (
                            student_id,
                            subject_id,
                            parse_date(row["attendance_date"]),
                            to_bool(row["is_present"])
                        )
                    )

        conn.close()
        logger.info(f"Lab attendance loaded into {name}")