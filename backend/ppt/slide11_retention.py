import logging
from typing import List

from pptx.presentation import Presentation
from backend.models.domain import RetentionRecord
from backend.ppt.base_ppt import BasePPT
from backend.ppt.placeholder_mapper import find_placeholder, find_table_by_headers
from backend.ppt.slide_paginator import paginate_table

logger = logging.getLogger(__name__)

class Slide11Retention(BasePPT):
    """Automates the Retention Pendency slide."""
    
    def __init__(self, prs: Presentation):
        # Target Index 10 (Page 11: Retention Pendency)
        super().__init__(prs, 10)
        
    def populate(self, records: List[RetentionRecord]) -> None:
        table_shape, header_idx = find_table_by_headers(self.slide, ["Location", "Reason", "Last Date"])
        if not table_shape:
            table_shape = find_placeholder(self.slide, "{{retention_table}}")
            header_idx = 0
            
        if not table_shape:
            logger.warning(f"[{self.__class__.__name__}] Target table {{retention_table}} not found on Slide 11.")
            return
            
        data = []
        for rec in records:
            data.append({
                "service_name": rec.service_name,
                "location": rec.location,
                "bandwidth": rec.bandwidth,
                "disconnection_reason": rec.disconnection_reason,
                "last_date": rec.last_date
            })
            
        columns = ["location", "disconnection_reason", "last_date"]
        headers = ["Location", "Reason", "Last Date"]
        paginate_table(self.prs, self.slide, data, columns, headers, max_rows_per_slide=3)
