import logging
from pathlib import Path
from typing import List, Tuple, Dict

from backend.models.domain import InventoryRecord
from backend.processors.base_processor import BaseProcessor
from backend.processors.validators import validate_customer_exists

logger = logging.getLogger(__name__)


class InventoryProcessor(BaseProcessor):
    """Processes the Customer Service Report to generate an inventory snapshot."""
    
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        # Using the actual CRM headers derived from the screenshot
        self.required_columns = ["Client Name", "Client Code", "Service Type", "Service ID", "Install City"]
        
    def process(self, customer_names: List[str]) -> Tuple[List['InventoryRecord'], Dict[str, int]]:
        """
        Processes the dataframe to aggregate link counts by Service Type for a specific customer.
        
        Args:
            customer_names: List of acceptable names for the customer.
            
        Returns:
            Tuple of (List of InventoryRecord models, Dict of retention metrics).
        """
        logger.info(f"[{self.__class__.__name__}] Processing inventory for customer: {customer_names[0]}")
        
        # 1. Load and validate
        self.load_and_validate()
        
        # 2. Filter by customer
        filtered_df = validate_customer_exists(self.df, "Client Name", customer_names)
        
        # 3. Group by Service Type and count Service ID
        grouped = filtered_df.groupby("Service Type")["Service ID"].count().reset_index()
        
        # 4. Sort alphabetically
        grouped = grouped.sort_values(by="Service Type")
        
        # 5. Convert to models
        results = []
        for _, row in grouped.iterrows():
            record = InventoryRecord(
                customer_name=customer_names[0],
                service_type=str(row["Service Type"]),
                link_count=int(row["Service ID"])
            )
            results.append(record)
            
        # 6. Calculate Retention Metrics
        total_customers = filtered_df["Client Code"].nunique() if "Client Code" in filtered_df.columns else 1
        
        retention_pending_services = 0
        retention_pending_customers = 0
        if "Status" in filtered_df.columns:
            ret_df = filtered_df[filtered_df["Status"] == "Retention Pending"]
            retention_pending_services = len(ret_df)
            if "Customer ID" in ret_df.columns:
                retention_pending_customers = ret_df["Customer ID"].nunique()
                
        metrics = {
            "total_customers": total_customers,
            "retention_pending_services": retention_pending_services,
            "retention_pending_customers": retention_pending_customers
        }
            
        logger.info(f"[{self.__class__.__name__}] Generated {len(results)} inventory records. Metrics: {metrics}")
        return results, metrics
