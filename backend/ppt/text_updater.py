def update_text_preserve_style(shape, new_data, paragraph_mapping=None):
    """
    Updates text in a shape while preserving the styling of the runs.
    If paragraph_mapping is provided, it replaces specific paragraphs with keys from new_data dict.
    Otherwise, it treats new_data as a single string and replaces the whole text block while preserving the style of the first run.
    """
    if not shape.has_text_frame:
        return
        
    text_frame = shape.text_frame
    if not text_frame.paragraphs:
        return
        
    if paragraph_mapping and isinstance(new_data, dict):
        # Update specific paragraphs using 'fields' config
        for data_key, conf in paragraph_mapping.items():
            p_idx = conf.get("paragraph")
            prefix = conf.get("prefix", "")
            
            if p_idx is not None and p_idx < len(text_frame.paragraphs):
                p = text_frame.paragraphs[p_idx]
                val = new_data.get(data_key)
                
                # If value is explicitly missing or None, we might skip or put N/A.
                # Since this is a targeted update (like csm_name), we update it.
                val_str = str(val) if not new_data_is_empty(val) else ""
                final_str = f"{prefix}{val_str}"
                
                # Store original run style of the FIRST run in this paragraph
                _replace_paragraph_text_safely(p, final_str)
    else:
        # Full replacement, preserving the first paragraph's first run style
        val_str = str(new_data) if not new_data_is_empty(new_data) else ""
        
        p = text_frame.paragraphs[0]
        _replace_paragraph_text_safely(p, val_str)
        
        # Remove all other paragraphs
        for i in range(len(text_frame.paragraphs)-1, 0, -1):
            p_elem = text_frame.paragraphs[i]._p
            p_elem.getparent().remove(p_elem)


def _replace_paragraph_text_safely(p, text: str):
    font_name, font_size, font_bold, font_italic, font_color = None, None, None, None, None
    if p.runs:
        run = p.runs[0]
        font_name = run.font.name
        font_size = run.font.size
        font_bold = run.font.bold
        font_italic = run.font.italic
        try:
            font_color = run.font.color.rgb
        except Exception:
            pass
            
    if not p.runs:
        p.add_run()
        
    p.runs[0].text = text
    
    # Remove extra runs in this paragraph
    for i in range(len(p.runs)-1, 0, -1):
        r = p.runs[i]._r
        r.getparent().remove(r)
        
    # Reapply style to the first run
    run = p.runs[0]
    if font_name: run.font.name = font_name
    if font_size: run.font.size = font_size
    if font_bold is not None: run.font.bold = font_bold
    if font_italic is not None: run.font.italic = font_italic
    if font_color: run.font.color.rgb = font_color

def new_data_is_empty(val):
    if val is None: return True
    if isinstance(val, str) and val.strip() == "": return True
    import math
    if isinstance(val, float) and math.isnan(val): return True
    return False
