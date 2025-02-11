import logging
import os
from datetime import datetime

def setup_logger(log_level: str = "INFO") -> logging.Logger:
    """Set up a logger with both console and file handlers."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists

    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    log_filename = os.path.join(log_dir, f"corona_da_{timestamp}.log")

    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        logger.handlers.clear()  # Clear existing handlers to avoid duplicates

    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(log_filename, mode='a')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
