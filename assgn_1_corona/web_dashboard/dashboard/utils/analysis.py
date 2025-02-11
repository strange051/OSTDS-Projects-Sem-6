import logging
from dashboard.utils.logger import setup_logger

# Set up logging
logger = setup_logger("INFO")

def analyze_data(df):
    """Performs basic analysis and logs dataset statistics."""
    if df.empty:
        logger.warning("Received an empty DataFrame for analysis. Skipping.")
        return

    logger.info("Dataset Overview:\n%s", df.describe())
