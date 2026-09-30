import logging
from pathlib import Path
from typing import List

from backend.models.domain import RetentionRecord
from backend.processors.base_processor import BaseProcessor
from backend.processors.validators import validate_customer_exists

logger = logging.getLogger(__name__)


class RetentionProcessor(BaseProcessor):
    """Processes the Retention Report to generate a retention pendency snapshot."""
    
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.required_columns = ["Client ID", "Service Name", "Location", "Bandwidth", "Disconnection Reason", "Last Date", "Status"]
        
    def process(self, customer_names: List[str]) -> List['RetentionRecord']:
        """
        Processes the dataframe to aggregate pending retention details.
        Only includes records where Status is 'Pending'.
        
        Args:
            customer_names: List of acceptable names for the customer.
            
        Returns:
            List of RetentionRecord models.
        """
        logger.info(f"[{self.__class__.__name__}] Processing retention for customer: {customer_names[0]}")
        
        # 1. Load and validate
        self.load_and_validate()
        
        # 2. Filter by customer (Client ID is used here as per the mock data/report structure usually, but we fallback to Customer Name if it exists, or just filter via aliases)
        # We will assume "Client ID" column holds the customer name aliases in this specific CRM report format.
        filtered_df = validate_customer_exists(self.df, "Client ID", customer_names)
        
        # 3. Filter strictly for "Pending" status
        if "Status" in filtered_df.columns:
            # We want to ignore "terminated", "removed", etc.
            filtered_df = filtered_df[filtered_df["Status"].astype(str).str.contains("Pending", case=False, na=False)]
        
        # 4. Sort by Last Date if possible
        if "Last Date" in filtered_df.columns:
            try:
                filtered_df["Last Date"] = filtered_df["Last Date"].astype(str)
                filtered_df = filtered_df.sort_values(by="Last Date", ascending=False)
            except Exception as e:
                logger.warning(f"Could not sort by Last Date: {e}")
                
        # 5. Convert to models
        results = []
        for _, row in filtered_df.iterrows():
            record = RetentionRecord(
                service_name=str(row.get("Service Name", "")),
                client_id=str(row.get("Client ID", "")),
                location=str(row.get("Location", "")),
                bandwidth=str(row.get("Bandwidth", "")),
                disconnection_reason=str(row.get("Disconnection Reason", "")),
                last_date=str(row.get("Last Date", ""))
            )
            results.append(record)
            
        logger.info(f"[{self.__class__.__name__}] Generated {len(results)} pending retention records.")
        return results
