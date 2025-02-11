import pandas as pd
import logging
from dashboard.utils.logger import setup_logger

# Set up logging
logger = setup_logger("INFO")

def clean_data(df):
    """Cleans the dataset by handling missing values and duplicates."""
    if df.empty:
        logger.warning("Received an empty DataFrame for cleaning. Skipping.")
        return df

    df.fillna(0, inplace=True)  # Replace NaN with 0
    df.drop_duplicates(inplace=True)  # Remove duplicate rows

    logger.info("Data cleaning completed successfully.")
    return df
