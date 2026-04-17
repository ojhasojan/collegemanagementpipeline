import psycopg2
from dotenv import load_dotenv
import os
import logging
from pathlib import Path

# Load .env from docker/ folder
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / "docker" / ".env")

logger = logging.getLogger(__name__)

def get_connection():
    """Returns a PostgreSQL connection using .env credentials."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        logger.info("Database connection established.")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise