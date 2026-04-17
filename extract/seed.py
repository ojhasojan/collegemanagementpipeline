from db import get_connection
from logger import get_logger

logger = get_logger("seed")

# ─── Reference Data ───────────────────────────────────────────

PROGRAMS = [
    "Civil Engineering",
    "IT Engineering",
    "Mechanical Engineering",
    "Electronic Engineering",
    "Electrical Engineering",
    "Architecture",
    "Electronics & Electrical Engineering",
    "Pre-Diploma Civil",
    "Pre-Diploma Mechanical",
    "Pre-Diploma IT",
    "Pre-Diploma Electrical",
]

SEMESTERS = list(range(1, 7))  # 1 to 6

EXAMS = [
    ("Internal Theory",    "THEORY"),
    ("Internal Practical", "LAB"),
    ("Assignment",         "BOTH"),
    ("First Term",         "THEORY"),
    ("Second Term",        "THEORY"),
    ("Final Term",         "THEORY"),
]

# 7 subjects per semester — each has a THEORY and LAB pair
SUBJECT_NAMES = [
    "Mathematics",
    "Physics",
    "English",
    "Programming",
    "Engineering Drawing",
    "Workshop Technology",
    "Applied Science",
]

# ─── Seeder Functions ─────────────────────────────────────────

def seed_programs(cur):
    logger.info("Seeding programs...")
    for program in PROGRAMS:
        cur.execute("""
            INSERT INTO programs (program_name)
            VALUES (%s)
            ON CONFLICT (program_name) DO NOTHING
        """, (program,))
    logger.info(f"  {len(PROGRAMS)} programs seeded.")


def seed_semesters(cur):
    logger.info("Seeding semesters...")
    for sem in SEMESTERS:
        cur.execute("""
            INSERT INTO semesters (semester_number)
            VALUES (%s)
            ON CONFLICT (semester_number) DO NOTHING
        """, (sem,))
    logger.info(f"  {len(SEMESTERS)} semesters seeded.")


def seed_exams(cur):
    logger.info("Seeding exams...")
    for exam_name, applies_to in EXAMS:
        cur.execute("""
            INSERT INTO exams (exam_name, applies_to)
            VALUES (%s, %s)
            ON CONFLICT (exam_name) DO NOTHING
        """, (exam_name, applies_to))
    logger.info(f"  {len(EXAMS)} exams seeded.")


def seed_subjects(cur):
    logger.info("Seeding subjects...")
    count = 0

    cur.execute("SELECT program_id, program_name FROM programs")
    programs = cur.fetchall()

    cur.execute("SELECT semester_id, semester_number FROM semesters")
    semesters = cur.fetchall()

    for program_id, program_name in programs:
        for semester_id, semester_number in semesters:
            for idx, subject_name in enumerate(SUBJECT_NAMES, start=1):

                # THEORY subject
                theory_code = f"P{program_id}_S{semester_number}_T{idx:02d}"
                theory_name = f"{subject_name} {semester_number}"
                cur.execute("""
                    INSERT INTO subjects
                        (subject_code, subject_name, program_id, semester_id, subject_type)
                    VALUES (%s, %s, %s, %s, 'THEORY')
                    ON CONFLICT (subject_code) DO NOTHING
                """, (theory_code, theory_name, program_id, semester_id))
                count += 1

                # LAB subject (paired with theory)
                lab_code = f"P{program_id}_S{semester_number}_L{idx:02d}"
                lab_name = f"{subject_name} {semester_number} Lab"
                cur.execute("""
                    INSERT INTO subjects
                        (subject_code, subject_name, program_id, semester_id, subject_type)
                    VALUES (%s, %s, %s, %s, 'LAB')
                    ON CONFLICT (subject_code) DO NOTHING
                """, (lab_code, lab_name, program_id, semester_id))
                count += 1

    logger.info(f"  {count} subjects seeded across all programs and semesters.")


# ─── Main ─────────────────────────────────────────────────────

def main():
    logger.info("=== Starting seed process ===")
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                seed_programs(cur)
                seed_semesters(cur)
                seed_exams(cur)
                seed_subjects(cur)
        logger.info("=== Seed process completed successfully ===")
    except Exception as e:
        logger.error(f"Seed process failed: {e}")
        raise
    finally:
        conn.close()
        logger.info("Database connection closed.")


if __name__ == "__main__":
    main()