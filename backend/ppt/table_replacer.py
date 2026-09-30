import logging
import copy
from typing import List, Dict, Any
from pptx.shapes.graphfrm import GraphicFrame
from backend.utils.exceptions import PPTGenerationError

logger = logging.getLogger(__name__)

def replace_table_data(table_shape: GraphicFrame, data: List[Dict[str, Any]], columns: List[str], header_row_index: int = 0) -> None:
    """
    Replaces data in a PPT table dynamically, strictly preserving font styles.
    Assumes `header_row_index` is the header, and `header_row_index + 1` is the template row.
    """
    if not table_shape.has_table:
        raise PPTGenerationError("Shape is not a table.")
        
    table = table_shape.table
    
    # We need a template row to copy styling
    template_row_index = header_row_index + 1
    if len(table.rows) <= template_row_index:
        raise PPTGenerationError("Table must have at least one template row after the header.")
        
    # Clear existing rows except header
    # python-pptx doesn't have a direct way to delete rows easily via API.
    # We will overwrite existing rows, and if we need more, we add them.
    # If we need less, we clear the text of the remaining ones.
    
    # Add rows if data is larger than existing template rows
    rows_to_add = len(data) - (len(table.rows) - template_row_index)
    for _ in range(max(0, rows_to_add)):
        # duplicate template row xml
        new_row = copy.deepcopy(table.rows[template_row_index]._tr)
        table._tbl.append(new_row)
        
    # Now write data
    for i, record in enumerate(data):
        row_idx = template_row_index + i
        for j, col_name in enumerate(columns):
            if j < len(table.columns):
                cell = table.cell(row_idx, j)
                new_text = str(record.get(col_name, ""))
                
                # STRICT FONT PRESERVATION: Keep the first run, delete others, modify text
                if cell.text_frame.paragraphs:
                    # Clear extra paragraphs
                    for p_idx in range(len(cell.text_frame.paragraphs)-1, 0, -1):
                        p = cell.text_frame.paragraphs[p_idx]
                        p._element.getparent().remove(p._element)
                        
                    p = cell.text_frame.paragraphs[0]
                    if p.runs:
                        # Clear extra runs
                        for r_idx in range(len(p.runs)-1, 0, -1):
                            r = p.runs[r_idx]
                            r._r.getparent().remove(r._r)
                        
                        p.runs[0].text = new_text
                    else:
                        p.text = new_text
                else:
                    cell.text = new_text
                    
    # Remove any extra rows completely to avoid empty grid lines, BUT keep at least 1 data row
    # to prevent PowerPoint from collapsing the table formatting.
    rows_to_keep = max(template_row_index + len(data), template_row_index + 1)
    
    for i in range(len(table.rows) - 1, rows_to_keep - 1, -1):
        tr = table.rows[i]._tr
        tr.getparent().remove(tr)
        
    # If we had 0 data, we kept 1 template row. We must clear its text.
    if len(data) == 0:
        for j in range(len(table.columns)):
            cell = table.cell(template_row_index, j)
            if cell.text_frame.paragraphs:
                for p_idx in range(len(cell.text_frame.paragraphs)-1, 0, -1):
                    p = cell.text_frame.paragraphs[p_idx]
                    p._element.getparent().remove(p._element)
                p = cell.text_frame.paragraphs[0]
                if p.runs:
                    for r_idx in range(len(p.runs)-1, 0, -1):
                        r = p.runs[r_idx]
                        r._r.getparent().remove(r._r)
                    p.runs[0].text = ""
                else:
                    p.text = ""
            else:
                cell.text = ""
            
    logger.info(f"Populated table with {len(data)} rows.")
