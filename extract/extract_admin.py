import os
from dotenv import load_dotenv
from pathlib import Path
from google_sheets import extract_sheet
from loader import (
    load_programs,
    load_semesters,
    load_teachers,
    load_students,
    load_subjects,
    load_subject_teacher,
    load_enrollments,
    load_exams,
)
from logger import get_logger

logger = get_logger("extract_admin")

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / "docker" / ".env")

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID_MAIN")

ADMIN_PIPELINE = [
    ("programs",        load_programs),
    ("semesters",       load_semesters),
    ("teachers",        load_teachers),
    ("students",        load_students),
    ("subjects",        load_subjects),
    ("subject_teacher", load_subject_teacher),
    ("enrollments",     load_enrollments),
    ("exams",           load_exams),
]


def main():
    logger.info("=== Starting admin pipeline ===")
    for tab_name, load_fn in ADMIN_PIPELINE:
        logger.info(f"--- Processing: {tab_name} ---")
        try:
            df = extract_sheet(SPREADSHEET_ID, tab_name)
            load_fn(df)
        except Exception as e:
            logger.error(f"Failed at {tab_name}: {e}")
            raise
    logger.info("=== Admin pipeline complete ===")


if __name__ == "__main__":
    main()