import logging
from pathlib import Path
from typing import List

from backend.models.domain import InvoiceRecord
from backend.processors.base_processor import BaseProcessor
from backend.processors.validators import validate_customer_exists

logger = logging.getLogger(__name__)


class InvoiceProcessor(BaseProcessor):
    """Processes the Client Ageing V2 Report to generate an invoice snapshot."""
    
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.required_columns = ["Customer Name", "Invoice Number", "Invoice Date", "Billing Period Duration", "Opening Balance", "Ageing Bucket", "Service Code"]
        
    def process(self, customer_names: List[str]) -> List['InvoiceRecord']:
        """
        Processes the dataframe to aggregate invoice ageing details.
        Uses 'Opening Balance' as directed by business logic.
        
        Args:
            customer_names: List of acceptable names for the customer.
            
        Returns:
            List of InvoiceRecord models.
        """
        logger.info(f"[{self.__class__.__name__}] Processing invoices for customer: {customer_names[0]}")
        
        # 1. Load and validate
        self.load_and_validate()
        
        # 2. Filter by customer
        filtered_df = validate_customer_exists(self.df, "Customer Name", customer_names)
        
        # 3. Sort by Invoice Date (newest first)
        if "Invoice Date" in filtered_df.columns:
            try:
                filtered_df["Invoice Date"] = filtered_df["Invoice Date"].astype(str)
                filtered_df = filtered_df.sort_values(by="Invoice Date", ascending=False)
            except Exception as e:
                logger.warning(f"Could not sort by Invoice Date: {e}")
        
        # 4. Convert to models
        results = []
        for _, row in filtered_df.iterrows():
            # Skip rows where Opening Balance is 0 or NaN if needed, but for now we extract all matching rows.
            try:
                opening_balance = float(row.get("Opening Balance", 0.0))
            except (ValueError, TypeError):
                opening_balance = 0.0

            record = InvoiceRecord(
                invoice_number=str(row.get("Invoice Number", "")),
                invoice_date=str(row.get("Invoice Date", "")),
                billing_period=str(row.get("Billing Period Duration", "")),
                opening_balance=opening_balance,
                ageing_bucket=str(row.get("Ageing Bucket", "")),
                service_code=str(row.get("Service Code", ""))
            )
            results.append(record)
            
        logger.info(f"[{self.__class__.__name__}] Generated {len(results)} invoice records.")
        return results
