import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def replace_text_in_slide(slide, replacements: Dict[str, str]) -> None:
    """
    Globally replaces text like {{customer_name}} or applies Regex replacements.
    """
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
            
        for paragraph in shape.text_frame.paragraphs:
            if not paragraph.runs:
                continue
                
            # First, check for regex matches on the entire paragraph text (to handle cross-run splits)
            paragraph_text = paragraph.text
            paragraph_modified = False
            for key, value in replacements.items():
                if not key.startswith("{{"):
                    # Use a regex that allows for smart quotes or regular quotes
                    # Replace literal ' in the regex key with a pattern that matches both
                    safe_key = key.replace("'", "['’‘]")
                    new_text = re.sub(safe_key, str(value), paragraph_text, flags=re.IGNORECASE)
                    if new_text != paragraph_text:
                        logger.info(f"Regex replaced paragraph: {paragraph_text} -> {new_text}")
                        paragraph_text = new_text
                        paragraph_modified = True
                        
            if paragraph_modified:
                # Fix \x0b soft line breaks which write out as _x000B_ in XML if left untouched
                paragraph_text = paragraph_text.replace('\x0b', '\n')
                # Apply the consolidated text to the first run, clear others
                paragraph.runs[0].text = paragraph_text
                for i in range(len(paragraph.runs) - 1, 0, -1):
                    r = paragraph.runs[i]
                    r._r.getparent().remove(r._r)
                continue
                
            # Fallback for standard tags inside runs
            for run in paragraph.runs:
                for key, value in replacements.items():
                    if key.startswith("{{"):
                        if key in run.text:
                            logger.info(f"Replacing text: {key} -> {value}")
                            run.text = run.text.replace(key, str(value))
