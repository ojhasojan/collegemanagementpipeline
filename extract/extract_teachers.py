from dotenv import load_dotenv
from pathlib import Path
from google_sheets import extract_sheet
from teacher_loader import (
    load_marks,
    load_theory_attendance,
    load_lab_attendance,
)
from logger import get_logger
from teachers_config import TEACHER_SHEETS

logger = get_logger("extract_teachers")

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / "docker" / ".env")

TEACHER_PIPELINE = [
    ("marks", load_marks),
    ("theory_attendance", load_theory_attendance),
    ("lab_attendance", load_lab_attendance),
]


def main():
    logger.info("=== Starting teacher pipeline ===")

    for teacher_name, spreadsheet_id in TEACHER_SHEETS.items():
        if not spreadsheet_id:
            logger.warning(f"No spreadsheet ID for {teacher_name}, skipping")
            continue

        logger.info(f"--- Processing: {teacher_name} ---")

        for tab_name, load_fn in TEACHER_PIPELINE:
            try:
                logger.info(f"Processing tab: {tab_name}")
                df = extract_sheet(spreadsheet_id, tab_name)
                load_fn(df, teacher_name)
            except Exception as e:
                logger.error(f"Failed {tab_name} for {teacher_name}: {e}")

    logger.info("=== Teacher pipeline complete ===")


if __name__ == "__main__":
    main()