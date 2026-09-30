import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List

import pandas as pd

from backend.processors.excel_reader import read_excel_file, clean_dataframe, normalize_customer_ids
from backend.processors.validators import validate_required_columns, validate_empty_dataframe
import os

logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    """Abstract base class for all data processors."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.df: pd.DataFrame = pd.DataFrame()
        self.required_columns: List[str] = []
        
    def load_and_validate(self) -> None:
        """Loads the Excel file, cleans it, and validates required columns."""
        start_time = time.time()
        logger.info(f"[{self.__class__.__name__}] Starting data load from {self.file_path.name}")
        
        # Read Excel
        raw_df = read_excel_file(self.file_path)
        
        # Clean dataframe (strip whitespace, etc.)
        self.df = clean_dataframe(raw_df)
        
        # Normalize Customer IDs
        strategy = os.getenv("NORMALIZATION_STRATEGY", "REPORT_ONLY")
        self.df = normalize_customer_ids(self.df, strategy=strategy)
        
        # Validate empty
        # validate_empty_dataframe(self.df, self.file_path.name)
        
        # Validate columns
        if self.required_columns:
            validate_required_columns(self.df, self.required_columns, self.file_path.name)
            
        execution_time = (time.time() - start_time) * 1000
        logger.info(f"[{self.__class__.__name__}] Load and validate completed in {execution_time:.2f}ms. {len(self.df)} rows loaded.")
        
    @abstractmethod
    def process(self, *args: Any, **kwargs: Any) -> Any:
        """Core processing logic to be implemented by subclasses."""
        pass
