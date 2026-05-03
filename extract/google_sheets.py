import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
from logger import get_logger

logger = get_logger("google_sheets")

# Load .env from docker/ folder
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / "docker" / ".env")

# Google Sheets API scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def get_gspread_client():
    """Authenticate and return a gspread client."""
    creds_path = Path(__file__).resolve().parent.parent / "credentials.json"
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    logger.info("Google Sheets client authenticated.")
    return client


def extract_sheet(spreadsheet_id: str, tab_name: str) -> pd.DataFrame:
    """Extract a single tab from a Google Spreadsheet as a DataFrame."""
    try:
        client = get_gspread_client()
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(tab_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        logger.info(f"Extracted {len(df)} rows from tab '{tab_name}'.")
        return df
    except Exception as e:
        logger.error(f"Failed to extract sheet '{tab_name}': {e}")
        raise