from typing import List
from pathlib import Path
from backend.ppt.base_ppt import BasePPT
from backend.ppt.placeholder_mapper import find_table_by_headers
from backend.ppt.table_replacer import replace_table_data
from backend.ppt.image_replacer import replace_image
from backend.models.domain import IncidentRecord
from backend.utils.exceptions import PPTGenerationError

class Slide9Incident(BasePPT):
    
    def __init__(self, prs):
        # Target Index 8 (Page 9: Incident Summary)
        super().__init__(prs, 8)
        
    def populate(self, incident_records: List[IncidentRecord]) -> None:
        # 1. Populate the table
        table_tuple = find_table_by_headers(self.slide, ["Location", "Cable issue"])
        if table_tuple and table_tuple[0] is not None:
            # We must map the IncidentRecord properties to dict keys for the table_replacer
            data_dicts = [
                {
                    "Location": rec.location,
                    "Cable issue": rec.cable_issue,
                    "Backhaul Impacted": rec.backhaul_impacted,
                    "Electricity issue": rec.electricity_issue
                }
                for rec in incident_records
            ]
            cols = ["Location", "Cable issue", "Backhaul Impacted", "Electricity issue"]
            replace_table_data(table_tuple[0], data_dicts, cols, table_tuple[1])
            
        # 2. Delete the unnecessary chart picture
        try:
            target_shape = None
            # Find the picture shape (usually Picture 3 based on earlier analysis)
            for shape in self.slide.shapes:
                if getattr(shape, 'shape_type', None) == 13:
                    target_shape = shape
                    break
                    
            if target_shape:
                # Delete the shape from the slide XML
                element = target_shape._element
                element.getparent().remove(element)
        except Exception as e:
            raise PPTGenerationError(f"Failed to delete incident chart picture: {e}")
