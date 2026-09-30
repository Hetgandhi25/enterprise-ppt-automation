from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def ensure_directory(path: Path) -> None:
    """Ensures that the directory for a path exists."""
    path.parent.mkdir(parents=True, exist_ok=True)
