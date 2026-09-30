import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from backend.utils.exceptions import ExcelValidationError

logger = logging.getLogger(__name__)


def read_excel_file(file_path: Path, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Reads an Excel file safely and returns a pandas DataFrame.

    Args:
        file_path: Path to the Excel file.
        sheet_name: Specific sheet to read. If None, reads the first sheet.

    Returns:
        pd.DataFrame: The parsed data.

    Raises:
        ExcelValidationError: If file doesn't exist, is corrupted, or sheet is missing.
    """
    logger.info(f"Attempting to read Excel file: {file_path}")
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise ExcelValidationError(f"Excel file not found at path: {file_path}")
        
    try:
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
            
        logger.info(f"Successfully read {len(df)} rows from {file_path.name}")
        return df
        
    except ValueError as ve:
        logger.error(f"ValueError reading {file_path.name}: {ve}")
        raise ExcelValidationError(f"Invalid sheet name or corrupted format in {file_path.name}: {ve}")
    except Exception as e:
        logger.error(f"Unexpected error reading {file_path.name}: {e}")
        raise ExcelValidationError(f"Failed to read Excel file {file_path.name}: {e}")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Performs basic cleaning on a DataFrame: strips whitespace from string columns."""
    df_cleaned = df.copy()
    
    # Strip whitespace from column names
    df_cleaned.columns = df_cleaned.columns.str.strip()
    
    # Strip whitespace from all string columns
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
        # Replace string 'nan' and 'None' with actual None for easier processing downstream
        df_cleaned[col] = df_cleaned[col].replace({'nan': None, 'None': None, '': None})
        
    return df_cleaned

def normalize_customer_ids(df: pd.DataFrame, strategy: str = "REPORT_ONLY") -> pd.DataFrame:
    """
    Detects and normalizes duplicate Customer IDs for the same Customer Name.
    Strategies:
      - REPORT_ONLY: Logs warnings but doesn't modify data.
      - AUTO: Picks the most frequent Customer ID.
      - MANUAL: (Not implemented, defaults to REPORT_ONLY)
    """
    if "Customer Name" not in df.columns or "Customer ID" not in df.columns:
        return df
        
    df_normalized = df.copy()
    grouped = df_normalized.groupby("Customer Name")["Customer ID"].nunique()
    duplicates = grouped[grouped > 1].index.tolist()
    
    if duplicates:
        logger.warning(f"Found {len(duplicates)} customers with multiple Customer IDs: {duplicates}")
        for cust in duplicates:
            ids = df_normalized[df_normalized["Customer Name"] == cust]["Customer ID"].unique()
            logger.warning(f"Customer '{cust}' has IDs: {ids}")
            
            if strategy == "AUTO":
                # Pick the most frequent ID
                primary_id = df_normalized[df_normalized["Customer Name"] == cust]["Customer ID"].mode()[0]
                logger.info(f"Auto-normalizing Customer '{cust}' to ID: {primary_id}")
                df_normalized.loc[df_normalized["Customer Name"] == cust, "Customer ID"] = primary_id
            elif strategy == "REPORT_ONLY":
                pass # Just report, don't modify
                
    return df_normalized
