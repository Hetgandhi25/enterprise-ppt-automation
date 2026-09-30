import logging
from pathlib import Path
from typing import List, Optional
import pandas as pd
from backend.utils.exceptions import AutomationError

logger = logging.getLogger(__name__)

class DownloadValidator:
    """Validates downloaded Excel files to ensure they are complete and correct."""
    
    @staticmethod
    def validate(
        file_path: Path, 
        expected_extension: str = ".xlsx", 
        min_size_bytes: int = 1024,
        expected_columns: Optional[List[str]] = None
    ) -> bool:
        logger.info(f"Validating download: {file_path}")
        
        if not file_path.exists():
            raise AutomationError(f"Validation failed: File does not exist {file_path}")
            
        if file_path.suffix.lower() != expected_extension:
            raise AutomationError(f"Validation failed: Expected {expected_extension}, got {file_path.suffix}")
            
        if file_path.stat().st_size < min_size_bytes:
            raise AutomationError(f"Validation failed: File too small ({file_path.stat().st_size} bytes)")
            
        # Optional deep validation
        if expected_columns:
            try:
                # Read just the header row
                df = pd.read_excel(file_path, nrows=0)
                columns = set(df.columns)
                missing = [col for col in expected_columns if col not in columns]
                if missing:
                    raise AutomationError(f"Validation failed: Missing columns {missing}")
            except Exception as e:
                raise AutomationError(f"Validation failed: Could not read Excel file {file_path}: {e}")
                
        logger.info(f"File {file_path.name} validated successfully.")
        return True
