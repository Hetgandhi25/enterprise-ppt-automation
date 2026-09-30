from typing import List
from backend.ppt.base_ppt import BasePPT
from backend.ppt.placeholder_mapper import find_placeholder, find_table_by_headers
from backend.ppt.table_replacer import replace_table_data
from backend.models.domain import InventoryRecord
from backend.utils.exceptions import PPTGenerationError

class Slide5Inventory(BasePPT):
    
    def __init__(self, prs: Presentation):
        # Target Index 4 (Page 5: Inventory Snap Shot)
        super().__init__(prs, 4)
        
    def populate(self, records: List[InventoryRecord]) -> None:
        table_shape, header_idx = find_table_by_headers(self.slide, ["Customer Locations", "Services"])
        if not table_shape:
            # Fallback to hidden tag if headers changed
            table_shape = find_placeholder(self.slide, "{{inventory_table}}")
            header_idx = 0
            
        if not table_shape:
            raise PPTGenerationError("Inventory table placeholder not found.")
            
        data = []
        for r in records:
            data.append({
                "Customer": r.customer_name,
                "Service": r.service_type,
                "Links": r.link_count
            })
            
        replace_table_data(table_shape, data, ["Customer", "Service", "Links"])
