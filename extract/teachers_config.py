import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / "docker" / ".env")

TEACHER_SHEETS = {
    "Sojan Ojha": os.getenv("SPREADSHEET_ID_TEACHER_SOJAN_OJHA")
}