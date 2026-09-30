import logging
from typing import List

from pptx.presentation import Presentation
from backend.models.domain import InvoiceRecord
from backend.ppt.base_ppt import BasePPT
from backend.ppt.placeholder_mapper import find_placeholder, find_table_by_headers
from backend.ppt.slide_paginator import paginate_table

logger = logging.getLogger(__name__)

class Slide10Invoice(BasePPT):
    """Automates the Invoice / Client Ageing slide."""
    
    def __init__(self, prs: Presentation):
        # Target Index 11 (Page 12: Invoice Pendency)
        super().__init__(prs, 11)
    
    def populate(self, records: List[InvoiceRecord]) -> None:
        table_shape, header_idx = find_table_by_headers(self.slide, ["Service ID", "Invoice Date", "Amount"])
        if not table_shape:
            table_shape = find_placeholder(self.slide, "{{invoice_table}}")
            header_idx = 0
            
        if not table_shape:
            logger.warning(f"[{self.__class__.__name__}] Target table {{invoice_table}} not found on Slide 12.")
            return
            
        data = []
        for rec in records:
            data.append({
                "invoice_number": rec.invoice_number,
                "service_code": rec.service_code,
                "billing_period": rec.billing_period,
                "opening_balance": str(rec.opening_balance),
                "ageing_bucket": rec.ageing_bucket
            })
            
        columns = ["invoice_number", "service_code", "billing_period", "opening_balance", "ageing_bucket"]
        headers = ["Service ID", "Invoice Date", "Amount"] # Unique headers to find the table
        paginate_table(self.prs, self.slide, data, columns, headers, max_rows_per_slide=3)
