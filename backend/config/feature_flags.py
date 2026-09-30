import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class FeatureFlags:
    """Feature toggles to enable or disable specific parts of the pipeline without changing code."""
    
    ENABLE_DOWNLOAD: bool = True
    ENABLE_SCREENSHOTS: bool = True
    ENABLE_NOTIFICATIONS: bool = True
    ENABLE_CLEANUP: bool = True
    ENABLE_CHARTS: bool = True
    ENABLE_PPT: bool = True
    ENABLE_METRICS: bool = True
    ENABLE_LOGGING: bool = True
    
    @classmethod
    def from_env(cls) -> "FeatureFlags":
        """Load feature flags from environment variables (defaults to True if not explicitly set to false)."""
        def get_bool(key: str, default: bool = True) -> bool:
            val = os.getenv(key)
            if val is None:
                return default
            return str(val).lower() in ("true", "1", "yes")
            
        return cls(
            ENABLE_DOWNLOAD=get_bool("ENABLE_DOWNLOAD", True),
            ENABLE_SCREENSHOTS=get_bool("ENABLE_SCREENSHOTS", True),
            ENABLE_NOTIFICATIONS=get_bool("ENABLE_NOTIFICATIONS", True),
            ENABLE_CLEANUP=get_bool("ENABLE_CLEANUP", True),
            ENABLE_CHARTS=get_bool("ENABLE_CHARTS", True),
            ENABLE_PPT=get_bool("ENABLE_PPT", True),
            ENABLE_METRICS=get_bool("ENABLE_METRICS", True),
            ENABLE_LOGGING=get_bool("ENABLE_LOGGING", True),
        )
