import logging
from backend.ppt.base_ppt import BasePPT
from backend.ppt.placeholder_mapper import find_table_by_headers
from backend.ppt.table_replacer import replace_table_data

logger = logging.getLogger(__name__)

class Slide3MOM(BasePPT):
    
    def __init__(self, prs):
        # Target Index 2 (Page 3: Previous Month MOM)
        super().__init__(prs, 2)
        
    def execute(self) -> None:
        logger.info(f"[{self.__class__.__name__}] Starting automation for slide 2")
        
        # We look for "Discussion Point" or "Action Item" to identify the MOM table
        table_tuple = find_table_by_headers(self.slide, ["Discussion Point", "Action Item"])
        if not table_tuple:
            # Fallback if specific headers aren't found
            table_tuple = find_table_by_headers(self.slide, ["Sr. No.", "Status"])
            
        if table_tuple and table_tuple[0] is not None:
            table_shape, header_row_index = table_tuple
            # Clear out the dummy content present in the template, preserving all original rows
            for i in range(header_row_index + 1, len(table_shape.table.rows)):
                for j in range(len(table_shape.table.columns)):
                    cell = table_shape.table.cell(i, j)
                    if cell.text_frame.paragraphs:
                        # Keep only the first paragraph to maintain formatting, clear the rest
                        for p_idx in range(len(cell.text_frame.paragraphs)-1, 0, -1):
                            p = cell.text_frame.paragraphs[p_idx]
                            p._element.getparent().remove(p._element)
                        p = cell.text_frame.paragraphs[0]
                        if p.runs:
                            # Keep only the first run to maintain font style, clear the rest
                            for r_idx in range(len(p.runs)-1, 0, -1):
                                r = p.runs[r_idx]
                                r._r.getparent().remove(r._r)
                            p.runs[0].text = ""
                        else:
                            p.text = ""
                    else:
                        cell.text = ""
        else:
            logger.warning("Could not find the MOM table on Slide 3.")
            
        logger.info(f"[{self.__class__.__name__}] Completed.")
