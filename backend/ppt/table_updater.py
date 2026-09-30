import logging

logger = logging.getLogger(__name__)

def update_table_in_place(shape, new_data: list):
    """
    Updates an existing table shape with new data.
    Implements safe overflow and empty data handling.
    """
    if not shape.has_table:
        return
        
    table = shape.table
    start_row = 1
    max_rows = len(table.rows) - start_row
    
    if new_data is None:
        new_data = []
        
    # Case C: Empty data
    if len(new_data) == 0:
        for i in range(max_rows):
            row_idx = start_row + i
            for col_idx in range(len(table.columns)):
                _set_cell_text(table.cell(row_idx, col_idx), "", fallback_mode=True)
        return

    # Case D & E: Overflow handling
    overflow = len(new_data) > max_rows
    if overflow:
        logger.warning(f"Table overflow: {len(new_data)} records for {max_rows} rows.")
        limit = max_rows - 1  # Leave last row for indicator
    else:
        limit = len(new_data)

    for i in range(max_rows):
        row_idx = start_row + i
        if i < limit:
            # Normal fill
            record = new_data[i]
            values = list(record.values()) if isinstance(record, dict) else record
                
            for col_idx in range(len(table.columns)):
                if col_idx < len(values):
                    val = values[col_idx]
                    # If val is None or empty, we use ""
                    str_val = str(val) if val is not None and val != "" else ""
                    _set_cell_text(table.cell(row_idx, col_idx), str_val)
                else:
                    _set_cell_text(table.cell(row_idx, col_idx), "", fallback_mode=True)
        elif i == limit and overflow:
            # Overflow indicator in the last available row
            _set_cell_text(table.cell(row_idx, 0), f"+{len(new_data) - limit} more", fallback_mode=True)
            for col_idx in range(1, len(table.columns)):
                _set_cell_text(table.cell(row_idx, col_idx), "", fallback_mode=True)
        else:
            # Clear remaining unused rows (Case B)
            for col_idx in range(len(table.columns)):
                _set_cell_text(table.cell(row_idx, col_idx), "", fallback_mode=True)

def _set_cell_text(cell, text: str, fallback_mode=False):
    text_frame = cell.text_frame
    if not text_frame.paragraphs:
        return
        
    p = text_frame.paragraphs[0]
    
    # Modify the text of the first run only, preserving other runs (e.g., " Mb" or " Aug")
    if not p.runs:
        p.add_run()
        
    p.runs[0].text = text
    
    # If this is fallback mode ("No data available" or "-"), we might want to clear other runs 
    # to avoid "- Mb"
    if fallback_mode:
        for i in range(len(p.runs)-1, 0, -1):
            r = p.runs[i]._r
            r.getparent().remove(r)
        for i in range(len(text_frame.paragraphs)-1, 0, -1):
            p_elem = text_frame.paragraphs[i]._p
            p_elem.getparent().remove(p_elem)
