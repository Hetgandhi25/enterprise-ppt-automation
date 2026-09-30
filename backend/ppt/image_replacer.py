import logging
from pathlib import Path
from pptx.util import Inches
from typing import Any

logger = logging.getLogger(__name__)

def replace_image(slide, shape: Any, image_path: Path) -> None:
    """
    Replaces a placeholder shape with an image, preserving position and dimensions.
    """
    if not image_path.exists():
        logger.error(f"Image not found at {image_path}")
        return
        
    x, y = shape.left, shape.top
    width, height = shape.width, shape.height
    
    # Insert new picture
    new_pic = slide.shapes.add_picture(
        str(image_path), 
        x, y, width, height
    )
    
    # Send to same z-order conceptually or simply delete the old shape
    sp = shape._element
    sp.getparent().remove(sp)
    
    logger.info(f"Replaced shape with image: {image_path.name}")
