import logging
from typing import Any

logger = logging.getLogger(__name__)

def get_shape_alt_text(shape: Any) -> str:
    """Safely extracts alt text or name from a shape."""
    if hasattr(shape, "name"):
        # We mapped alt_text to name in dummy generation, and natively in PPT, title/description 
        # can also be accessed sometimes through shape.name if set properly.
        # Let's check native description first
        try:
            if hasattr(shape, "_element"):
                cNvPr = shape._element.xpath('.//p:cNvPr')
                if cNvPr:
                    desc = cNvPr[0].get("descr")
                    title = cNvPr[0].get("title")
                    if desc: return desc
                    if title: return title
        except Exception:
            pass
        return shape.name
    return ""

def find_placeholder(slide, placeholder_name: str) -> Any:
    """Finds a shape in a slide by its alt text/name."""
    for shape in slide.shapes:
        if get_shape_alt_text(shape) == placeholder_name:
            return shape
    return None

def validate_placeholder(slide, placeholder_name: str) -> bool:
    """Validates if a placeholder exists on the slide."""
    return find_placeholder(slide, placeholder_name) is not None

def find_table_by_headers(slide, expected_headers: list) -> Any:
    """
    Finds a table by checking if its first few rows contain the expected headers.
    Returns (shape, header_row_index) or (None, -1) if not found.
    """
    for shape in slide.shapes:
        if shape.has_table:
            # Check the first 3 rows (in case row 0 is blank/merged for styling)
            for row_idx in range(min(3, len(shape.table.rows))):
                row_texts = []
                for cell in shape.table.rows[row_idx].cells:
                    text = cell.text_frame.text.replace('\n', ' ').strip().lower()
                    row_texts.append(text)
                
                # Check if all expected headers are present in this row
                matches = 0
                for expected in expected_headers:
                    if any(expected.lower() in text for text in row_texts):
                        matches += 1
                if matches == len(expected_headers):
                    return shape, row_idx
    return None, -1

def find_shape_by_position(slide, position: str) -> Any:
    """
    Finds a picture/chart placeholder by horizontal position.
    position: 'left' or 'right'
    """
    candidates = []
    for shape in slide.shapes:
        # Assuming placeholders for charts are often empty picture frames or rectangles
        # Or they are already charts. We just grab shapes that are in the main body area.
        # Let's filter out very small shapes, lines, or things clearly not chart containers.
        if shape.shape_type in [1, 14, 13, 16, 20]: # AutoShape, Placeholder, Picture, GraphicFrame, etc
            candidates.append(shape)
            
    if not candidates:
        return None
        
    # Sort left to right
    candidates.sort(key=lambda s: s.left)
    
    # Simple heuristic: if we have 2 main boxes (like Slide 6), left is 0, right is -1
    # Often there's a title box which spans the top. We ignore shapes spanning the whole slide.
    slide_width = 9144000 # default 10 inches
    filtered = [s for s in candidates if s.width < slide_width * 0.8]
    
    if not filtered:
        return None
        
    if position == 'left':
        return filtered[0]
    elif position == 'right':
        return filtered[-1]
    return None
