import pandas as pd
import logging
from dashboard.utils.logger import setup_logger

# Set up logging
logger = setup_logger("INFO")

def load_data(csv_file_path):
    """Loads CSV data into a Pandas DataFrame with error handling."""
    try:
        df = pd.read_csv(csv_file_path)
        logger.info(f"Successfully loaded data from {csv_file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"Error: File {csv_file_path} not found.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        logger.error(f"Error: File {csv_file_path} is empty.")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return pd.DataFrame()
