from typing import List, Any
import pandas as pd
from backend.utils.exceptions import ExcelValidationError, CustomerNotFoundError


def validate_required_columns(df: pd.DataFrame, required_columns: List[str], file_name: str = "Unknown") -> None:
    """Validates that all required columns are present in the DataFrame."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ExcelValidationError(f"File '{file_name}' is missing required columns: {missing}")


def validate_empty_dataframe(df: pd.DataFrame, file_name: str = "Unknown") -> None:
    """Validates that the DataFrame is not empty."""
    if df.empty:
        raise ExcelValidationError(f"File '{file_name}' contains no data rows.")


def validate_customer_exists(df: pd.DataFrame, customer_column: str, customer_names: List[str]) -> pd.DataFrame:
    """Validates that at least one of the provided customer names exists in the DataFrame and filters it."""
    # Normalize names for comparison
    customer_names_lower = [name.strip().lower() for name in customer_names]
    
    # Fill NaN and convert to string for safety
    mask = df[customer_column].fillna("").astype(str).str.strip().str.lower().isin(customer_names_lower)
    filtered_df = df[mask]
    
    if filtered_df.empty:
        # We now allow empty DataFrames if the customer isn't found (no records for them)
        logger = __import__('logging').getLogger(__name__)
        logger.warning(f"Customer '{customer_names[0]}' not found in column '{customer_column}'. Returning empty DataFrame.")
        
    return filtered_df


def validate_numeric_columns(df: pd.DataFrame, numeric_columns: List[str], file_name: str = "Unknown") -> None:
    """Validates that specified columns can be converted to numeric types."""
    for col in numeric_columns:
        if col in df.columns:
            try:
                pd.to_numeric(df[col])
            except ValueError:
                raise ExcelValidationError(f"Column '{col}' in '{file_name}' contains non-numeric data.")


def validate_month_format(month_str: str) -> None:
    """Validates that a month string matches YYYY-MM format."""
    import re
    if not re.match(r"^\d{4}-\d{2}$", month_str):
        raise ExcelValidationError(f"Invalid month format: '{month_str}'. Expected 'YYYY-MM'.")


def validate_sla_percentage(sla: float) -> None:
    """Validates that an SLA percentage is between 0 and 100."""
    if not (0.0 <= sla <= 100.0):
        raise ExcelValidationError(f"Invalid SLA percentage: {sla}. Must be between 0.0 and 100.0.")

def validate_sla_metrics(df: pd.DataFrame, thresholds: dict) -> pd.DataFrame:
    """
    Validates SLA metrics against configured thresholds.
    Logs warnings for rows falling below thresholds instead of failing.
    
    Args:
        df: The dataframe containing SLA records.
        thresholds: Dictionary of column names to threshold values.
        
    Returns:
        The original dataframe (or augmented with violation flags).
    """
    import logging
    logger = logging.getLogger(__name__)
    
    df_validated = df.copy()
    
    for metric, threshold in thresholds.items():
        if threshold is None:
            continue
            
        if metric in df_validated.columns:
            # Assume metric values might be strings or percentages
            try:
                numeric_series = pd.to_numeric(df_validated[metric].astype(str).str.rstrip('%'), errors='coerce')
                violations = df_validated[numeric_series < threshold]
                if not violations.empty:
                    logger.warning(f"SLA Violation: {len(violations)} rows fell below the {threshold} threshold for '{metric}'.")
            except Exception as e:
                logger.warning(f"Could not validate SLA for '{metric}': {e}")
                
    return df_validated
