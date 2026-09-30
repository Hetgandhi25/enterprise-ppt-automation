import logging
from pathlib import Path
from typing import List

import pandas as pd

from backend.models.domain import IncidentRecord
from backend.processors.base_processor import BaseProcessor
from backend.processors.validators import validate_customer_exists

logger = logging.getLogger(__name__)


class IncidentProcessor(BaseProcessor):
    """Processes the Incident Report to generate a summary matrix."""
    
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.required_columns = ["Customer Name", "Location", "Issue Category"]
        
    def process(self, customer_names: List[str]) -> List[IncidentRecord]:
        """
        Processes the dataframe to count issues by category per location.
        
        Args:
            customer_names: List of acceptable customer names.
            
        Returns:
            List of IncidentRecord models.
        """
        logger.info(f"[{self.__class__.__name__}] Processing incidents for customer: {customer_names[0]}")
        
        self.load_and_validate()
        
        filtered_df = validate_customer_exists(self.df, "Customer Name", customer_names)
        
        # Fill missing locations
        filtered_df["Location"] = filtered_df["Location"].fillna("Unknown")
        
        # Group by Location and Issue Category, count incidents
        # Adding a dummy column to count
        filtered_df["count"] = 1
        pivot = filtered_df.pivot_table(
            index="Location", 
            columns="Issue Category", 
            values="count", 
            aggfunc="sum",
            fill_value=0
        ).reset_index()
        
        results = []
        # Safely extract known categories, defaulting to 0 if the column doesn't exist in the data
        for _, row in pivot.iterrows():
            record = IncidentRecord(
                location=str(row["Location"]),
                cable_issue=int(row.get("Cable", 0)),
                backhaul_impacted=int(row.get("Backhaul", 0)),
                electricity_issue=int(row.get("Electricity", 0))
            )
            results.append(record)
            
        # Sort by location alphabetically
        results.sort(key=lambda x: x.location)
        
        logger.info(f"[{self.__class__.__name__}] Generated incident summary for {len(results)} locations.")
        return results
