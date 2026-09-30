import logging
from pathlib import Path
from pptx import Presentation
from backend.utils.exceptions import PPTGenerationError

logger = logging.getLogger(__name__)

def load_presentation(path: Path) -> Presentation:
    if not path.exists():
        raise PPTGenerationError(f"Template not found: {path}")
    logger.info(f"Loading presentation template from {path}")
    return Presentation(str(path))

def save_presentation(prs: Presentation, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(path))
    logger.info(f"Saved presentation to {path}")
