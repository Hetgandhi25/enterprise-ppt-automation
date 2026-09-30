import logging
from typing import Dict, Any

from backend.config.loader import load_json_config

logger = logging.getLogger(__name__)

class ThemeLoader:
    """Loads and caches the charting theme."""
    
    _theme_cache: Dict[str, Any] = {}
    
    @classmethod
    def get_theme(cls) -> Dict[str, Any]:
        """Returns the loaded theme, caching it on first load."""
        if not cls._theme_cache:
            logger.info("Loading charting theme from theme.json")
            cls._theme_cache = load_json_config("theme.json")
        return cls._theme_cache

    @classmethod
    def get_color(cls, color_name: str, default: str = "#000000") -> str:
        """Helper to get a specific color."""
        theme = cls.get_theme()
        return theme.get("colors", {}).get(color_name, default)

    @classmethod
    def get_font(cls, font_type: str = "main", default: str = "Arial") -> str:
        """Helper to get a specific font family."""
        theme = cls.get_theme()
        return theme.get("fonts", {}).get(font_type, default)
