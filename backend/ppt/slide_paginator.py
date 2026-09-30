import copy
import math
from typing import List, Dict, Any, Callable, Tuple

from pptx.presentation import Presentation
from pptx.slide import Slide
from backend.ppt.table_replacer import replace_table_data
from backend.ppt.placeholder_mapper import find_table_by_headers
from backend.utils.exceptions import PPTGenerationError

def duplicate_slide(prs: Presentation, source_slide: Slide, insert_after_slide: Slide) -> Slide:
    """
    Duplicates a slide perfectly by copying all XML shape elements to a new slide with the same layout.
    Inserts the new slide immediately after `insert_after_slide`.
    """
    # Create new slide from the same layout
    dest_slide = prs.slides.add_slide(source_slide.slide_layout)
    
    # Clean destination slide shapes (remove default layout placeholders)
    for shape in dest_slide.shapes:
        element = shape.element
        element.getparent().remove(element)
        
    # Deep copy source slide shapes
    for shape in source_slide.shapes:
        new_el = copy.deepcopy(shape.element)
        dest_slide.shapes._spTree.insert_element_before(new_el, 'p:extLst')
        
    # Move dest_slide to be immediately after source_slide
    sldIdLst = prs.slides._sldIdLst
    insert_after_id = None
    dest_id = None
    for sldId in sldIdLst:
        if sldId.id == insert_after_slide.slide_id:
            insert_after_id = sldId
        elif sldId.id == dest_slide.slide_id:
            dest_id = sldId
            
    if insert_after_id is not None and dest_id is not None:
        sldIdLst.remove(dest_id)
        insert_idx = sldIdLst.index(insert_after_id)
        sldIdLst.insert(insert_idx + 1, dest_id)
        
    return dest_slide

def paginate_table(prs: Presentation, 
                   base_slide: Slide, 
                   data: List[Dict[str, Any]], 
                   columns: List[str], 
                   headers: List[str],
                   max_rows_per_slide: int = 5) -> None:
    """
    Paginates a table across multiple slides if the data exceeds max_rows_per_slide.
    """
    if not data:
        # If no data, just clear the table on the base slide
        table_tuple = find_table_by_headers(base_slide, headers)
        if table_tuple and table_tuple[0] is not None:
            replace_table_data(table_tuple[0], [], columns, table_tuple[1])
        return

    # Calculate chunks
    chunks = [data[i:i + max_rows_per_slide] for i in range(0, len(data), max_rows_per_slide)]
    
    current_slide = base_slide
    for i, chunk in enumerate(chunks):
        # Find the table on the current slide
        table_tuple = find_table_by_headers(current_slide, headers)
        if not table_tuple:
            raise PPTGenerationError(f"Could not find table with headers {headers} for pagination.")
            
        # Populate the chunk
        replace_table_data(table_tuple[0], chunk, columns, table_tuple[1])
        
        # If there are more chunks, duplicate the base slide for the next iteration
        if i < len(chunks) - 1:
            current_slide = duplicate_slide(prs, base_slide, insert_after_slide=current_slide)
