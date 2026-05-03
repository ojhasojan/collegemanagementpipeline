import psycopg2
from dotenv import load_dotenv
import os
import logging
from pathlib import Path

# Load .env from docker/ folder
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / "docker" / ".env")

logger = logging.getLogger(__name__)


def get_connection():
    """Returns a local PostgreSQL connection using .env credentials."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        logger.info("Local database connection established.")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to local database: {e}")
        raise


def get_supabase_connection():
    """Returns a Supabase PostgreSQL connection using .env credentials."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("SUPABASE_HOST"),
            port=os.getenv("SUPABASE_PORT", "5432"),
            dbname=os.getenv("SUPABASE_DB", "postgres"),
            user=os.getenv("SUPABASE_USER", "postgres"),
            password=os.getenv("SUPABASE_PASSWORD"),
        )
        logger.info("Supabase database connection established.")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {e}")
        raise


def get_all_connections():
    """Returns both local and Supabase connections."""
    connections = [("local", get_connection())]

    if os.getenv("SUPABASE_HOST"):
        connections.append(("supabase", get_supabase_connection()))

    return connections