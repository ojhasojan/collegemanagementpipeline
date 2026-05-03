from datetime import datetime
from db import get_connection, get_supabase_connection
from logger import get_logger

logger = get_logger("loader")

# =========================
# HELPERS
# =========================

def normalize_text(value):
    """Normalize text for joins."""
    if value is None:
        return None
    return str(value).strip().lower()


def parse_date(value):
    """Parse YYYY-MM-DD safely."""
    if not value:
        return None
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        logger.error(f"Invalid date format: {value}")
        return None


def to_int(value):
    if value is None or value == "":
        return None
    return int(value)


def get_all_connections():
    """Local = primary, Supabase = replica"""
    connections = [("local", get_connection())]

    try:
        connections.append(("supabase", get_supabase_connection()))
    except Exception as e:
        logger.warning(f"Supabase unavailable, continuing locally: {e}")

    return connections


# =========================
# PROGRAMS
# =========================

def load_programs(df):
    for _, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():
                    cur.execute(
                        """
                        INSERT INTO programs (program_name)
                        VALUES (%s)
                        ON CONFLICT (program_name) DO NOTHING
                        """,
                        (normalize_text(row["program_name"]),)
                    )
        conn.close()


# =========================
# SEMESTERS
# =========================

def load_semesters(df):
    for _, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():
                    cur.execute(
                        """
                        INSERT INTO semesters (semester_number)
                        VALUES (%s)
                        ON CONFLICT (semester_number) DO NOTHING
                        """,
                        (to_int(row["semester_number"]),)
                    )
        conn.close()


# =========================
# TEACHERS
# =========================

def load_teachers(df):
    for _, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():
                    cur.execute(
                        """
                        INSERT INTO teachers (teacher_name, department, email, phone)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (teacher_name) DO NOTHING
                        """,
                        (
                            normalize_text(row["teacher_name"]),
                            row.get("department"),
                            row.get("email"),
                            row.get("phone"),
                        )
                    )
        conn.close()


# =========================
# STUDENTS
# =========================

def load_students(df):
    for _, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():

                    # Resolve program
                    cur.execute(
                        "SELECT program_id FROM programs WHERE program_name = %s",
                        (normalize_text(row["program_name"]),)
                    )
                    prog = cur.fetchone()
                    if not prog:
                        logger.error(f"Program not found: {row['program_name']}")
                        continue
                    program_id = prog[0]

                    # Resolve semester
                    cur.execute(
                        "SELECT semester_id FROM semesters WHERE semester_number = %s",
                        (to_int(row["semester_number"]),)
                    )
                    sem = cur.fetchone()
                    if not sem:
                        logger.error(f"Semester not found: {row['semester_number']}")
                        continue
                    semester_id = sem[0]

                    cur.execute(
                        """
                        INSERT INTO students (
                            registration_number,
                            roll_no,
                            first_name,
                            last_name,
                            gender,
                            date_of_birth,
                            program_id,
                            semester_id,
                            admission_year
                        )
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (registration_number) DO UPDATE
                        SET
                            roll_no = EXCLUDED.roll_no,
                            first_name = EXCLUDED.first_name,
                            last_name = EXCLUDED.last_name,
                            gender = EXCLUDED.gender,
                            date_of_birth = EXCLUDED.date_of_birth,
                            program_id = EXCLUDED.program_id,
                            semester_id = EXCLUDED.semester_id,
                            admission_year = EXCLUDED.admission_year
                        """,
                        (
                            row["registration_number"],
                            row.get("roll_no"),
                            row["first_name"],
                            row["last_name"],
                            row.get("gender"),
                            parse_date(row.get("date_of_birth")),
                            program_id,
                            semester_id,
                            to_int(row.get("admission_year")),
                        )
                    )
        conn.close()


# =========================
# SUBJECTS
# =========================

def load_subjects(df):
    for _, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:

                for _, row in df.iterrows():

                    cur.execute(
                        "SELECT program_id FROM programs WHERE program_name = %s",
                        (normalize_text(row["program_name"]),)
                    )
                    prog = cur.fetchone()
                    if not prog:
                        logger.error(f"Program not found for subject {row['subject_code']}")
                        continue
                    program_id = prog[0]

                    cur.execute(
                        "SELECT semester_id FROM semesters WHERE semester_number = %s",
                        (to_int(row["semester_number"]),)
                    )
                    sem = cur.fetchone()
                    if not sem:
                        logger.error(f"Semester not found for subject {row['subject_code']}")
                        continue
                    semester_id = sem[0]

                    cur.execute(
                        """
                        INSERT INTO subjects (
                            subject_code, subject_name,
                            program_id, semester_id, subject_type
                        )
                        VALUES (%s,%s,%s,%s,%s)
                        ON CONFLICT (subject_code) DO NOTHING
                        """,
                        (
                            normalize_text(row["subject_code"]),
                            row["subject_name"],
                            program_id,
                            semester_id,
                            row["subject_type"],
                        )
                    )

        conn.close()


# =========================
# SUBJECT ↔ TEACHER
# =========================

def load_subject_teacher(df):
    for _, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():

                    cur.execute(
                        "SELECT subject_id FROM subjects WHERE subject_code = %s",
                        (normalize_text(row["subject_code"]),)
                    )
                    sub = cur.fetchone()
                    if not sub:
                        logger.error(f"Subject not found: {row['subject_code']}")
                        continue
                    subject_id = sub[0]

                    cur.execute(
                        "SELECT teacher_id FROM teachers WHERE teacher_name = %s",
                        (normalize_text(row["teacher_name"]),)
                    )
                    t = cur.fetchone()
                    if not t:
                        logger.error(f"Teacher not found: {row['teacher_name']}")
                        continue
                    teacher_id = t[0]

                    cur.execute(
                        """
                        INSERT INTO subject_teacher (subject_id, teacher_id, teacher_role)
                        VALUES (%s,%s,%s)
                        ON CONFLICT DO NOTHING
                        """,
                        (subject_id, teacher_id, row["teacher_role"])
                    )
        conn.close()


# =========================
# ENROLLMENTS
# =========================

def load_enrollments(df):
    for _, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():

                    cur.execute(
                        """
                        SELECT student_id, semester_id
                        FROM students
                        WHERE registration_number = %s
                        """,
                        (row["registration_number"],)
                    )
                    s = cur.fetchone()
                    if not s:
                        logger.error(f"Student not found: {row['registration_number']}")
                        continue

                    student_id, semester_id = s

                    cur.execute(
                        """
                        INSERT INTO enrollments (student_id, semester_id, academic_year)
                        VALUES (%s,%s,%s)
                        ON CONFLICT DO NOTHING
                        """,
                        (student_id, semester_id, row["academic_year"])
                    )
        conn.close()


# =========================
# EXAMS
# =========================

def load_exams(df):
    for _, conn in get_all_connections():
        with conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():
                    cur.execute(
                        """
                        INSERT INTO exams (exam_name, applies_to)
                        VALUES (%s,%s)
                        ON CONFLICT (exam_name) DO NOTHING
                        """,
                        (
                            normalize_text(row["exam_name"]),
                            row["applies_to"],
                        )
                    )
        conn.close()