from pathlib import Path
from pptx.util import Inches
from backend.utils.exceptions import PPTGenerationError
import logging

logger = logging.getLogger(__name__)

def send_to_back(shape):
    """Moves the shape to the back of the z-order on the slide."""
    try:
        element = shape._element
        parent = element.getparent()
        # The first few elements in spTree are properties, we insert after them
        # Usually nvGrpSpPr is index 0, grpSpPr is index 1
        parent.insert(2, element)
    except Exception as e:
        logger.warning(f"Could not send shape to back: {e}")

def inject_global_images(prs, background_path: Path, logo_path: Path):
    """
    Injects the logo onto every slide, and the background onto Slide 1 and Slide 15.
    """
    if not logo_path.exists() or not background_path.exists():
        logger.warning("Global images not found, skipping injection.")
        return
        
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    
    last_idx = len(prs.slides) - 1
    # 1. Backgrounds on Slide 1 and Last Slide
    target_indices = [0, last_idx]
    for idx in target_indices:
        if idx < len(prs.slides):
            slide = prs.slides[idx]
            try:
                # Add background picture filling the entire slide
                bg_shape = slide.shapes.add_picture(str(background_path), 0, 0, slide_width, slide_height)
                # Send to back so it doesn't cover text
                send_to_back(bg_shape)
            except Exception as e:
                logger.error(f"Failed to inject background on slide {idx+1}: {e}")
                
    # 2. Logo on every page
    # Position: Top Right (e.g., right-aligned with a small margin)
    logo_width = Inches(1.2)
    logo_left = slide_width - logo_width - Inches(0.2)
    logo_top = Inches(0.2)
    
    for i, slide in enumerate(prs.slides):
        if i in [0, last_idx]:
            continue
        try:
            slide.shapes.add_picture(str(logo_path), logo_left, logo_top, width=logo_width)
        except Exception as e:
            logger.error(f"Failed to inject logo on slide {i+1}: {e}")
