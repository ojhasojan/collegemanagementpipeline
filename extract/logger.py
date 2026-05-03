import logging
import os
from datetime import datetime
from pathlib import Path

# Always save logs relative to this file's location
LOG_DIR = Path(__file__).resolve().parent / "logs"


def get_logger(name: str) -> logging.Logger:
    """Returns a logger that writes to both console and logs/ folder."""

    os.makedirs(LOG_DIR, exist_ok=True)

    log_filename = LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logger = logging.getLogger(name)

    # Ensure logger is configured only once
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.propagate = False  # ✅ prevent duplicate logs

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_filename, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console)
        logger.addHandler(file_handler)

    return logger