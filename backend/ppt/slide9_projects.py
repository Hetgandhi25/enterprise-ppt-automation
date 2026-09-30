import logging
from backend.ppt.base_ppt import BasePPT
from backend.ppt.placeholder_mapper import find_table_by_headers
from backend.ppt.table_replacer import replace_table_data

logger = logging.getLogger(__name__)

class Slide9Projects(BasePPT):
    
    def __init__(self, prs):
        # Target Index 9 (Page 10: Projects in Progress)
        super().__init__(prs, 9)
        
    def execute(self) -> None:
        logger.info(f"[{self.__class__.__name__}] Starting automation for slide {self.slide_index}")
        
        # We look for "New Link/Upgrade" or "Target Completion" to identify the Projects table
        table_tuple = find_table_by_headers(self.slide, ["New Link/Upgrade", "Target Completion"])
        
        if table_tuple and table_tuple[0] is not None:
            table_shape, header_row_index = table_tuple
            
            # Use replace_table_data with empty data list to completely clear the table rows
            columns = ["Location", "New Link/Upgrade", "Bandwidth", "Target Completion"]
            replace_table_data(table_shape, [], columns, header_row_index)
            
        else:
            logger.warning("Could not find the Projects in Progress table on Slide 9.")
            
        logger.info(f"[{self.__class__.__name__}] Completed.")
