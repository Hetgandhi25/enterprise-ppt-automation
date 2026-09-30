import logging
import time
from pathlib import Path
from pptx import Presentation
from backend.utils.exceptions import PPTGenerationError

logger = logging.getLogger(__name__)

class BasePPT:
    """Abstract base class for all slide automation."""
    
    def __init__(self, prs: Presentation, slide_index: int):
        self.prs = prs
        if slide_index >= len(self.prs.slides):
            logger.warning(f"Slide index {slide_index} out of range. Falling back to slide 0 for testing.")
            slide_index = 0
        self.slide = self.prs.slides[slide_index]
        self.slide_index = slide_index
        
    def execute(self, *args, **kwargs) -> None:
        """Core execution logic wrapper."""
        start_time = time.time()
        logger.info(f"[{self.__class__.__name__}] Starting automation for slide {self.slide_index}")
        
        try:
            self.populate(*args, **kwargs)
            exec_time = (time.time() - start_time) * 1000
            logger.info(f"[{self.__class__.__name__}] Completed in {exec_time:.2f}ms.")
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Failed: {e}")
            raise PPTGenerationError(f"Slide {self.slide_index} error: {e}")
            
    def populate(self, *args, **kwargs) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError
