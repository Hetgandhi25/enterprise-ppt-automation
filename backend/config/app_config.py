import os
import logging
from pathlib import Path
from backend.config.mode import AppMode
from backend.config.feature_flags import FeatureFlags
from backend.config.credential_manager import CredentialManager
from backend.utils.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

class AppConfig:
    """Core Application Configuration and Startup Validation."""
    
    def __init__(self, mode: AppMode):
        self.mode = mode
        self.base_dir = Path(__file__).resolve().parent.parent
        self.features = FeatureFlags.from_env()
        self.credentials = CredentialManager()
        
        # Directories
        self.dirs = {
            "configs": self.base_dir / "config",
            "logs": self.base_dir / "logs",
            "downloads": self.base_dir / self.credentials.download_path,
            "outputs": self.base_dir / self.credentials.output_path,
            "charts": self.base_dir / "output" / "charts",
            "templates": self.base_dir / "templates"
        }
        
        # Find template
        template_files = list(self.dirs["templates"].glob("*.pptx"))
        default_template = self.dirs["templates"] / "ServiceReview.pptx"
        if default_template in template_files:
            self.template_path = default_template
        elif template_files:
            self.template_path = template_files[0]
        else:
            self.template_path = default_template
            
        self.manifest_path = self.dirs["templates"] / "template_manifest.yaml"
            
        self.theme_path = self.dirs["configs"] / "theme.json"
        self.portal_path = self.dirs["configs"] / "portal.json"
        self.logging_path = self.dirs["configs"] / "logging.yaml"
        self.auth_path = self.dirs["configs"] / "auth.json"
        
        # Business Configurations
        self.NORMALIZATION_STRATEGY = os.getenv("NORMALIZATION_STRATEGY", "REPORT_ONLY")  # REPORT_ONLY, AUTO, MANUAL
        self.SLA_THRESHOLDS = {
            "point_6": None,
            "point_7": None,
            "point_8": None,
            "point_9": None
        }
        
    def validate_startup(self):
        """Performs a full pre-flight check before application starts."""
        
        # 1. Validate Directories
        for name, d in self.dirs.items():
            if not d.exists():
                logger.info(f"Creating required directory: {d}")
                d.mkdir(parents=True, exist_ok=True)
                
        # 2. Validate Files
        required_files = [
            (self.template_path, "PPT Template"),
            (self.theme_path, "Theme Configuration"),
            (self.portal_path, "Portal Configuration"),
            (self.logging_path, "Logging Configuration")
        ]
        
        for path, desc in required_files:
            if not path.exists():
                raise ConfigurationError(f"Missing required file: {desc} at {path}")
                
        # 3. Validate Production Credentials
        if self.mode == AppMode.PRODUCTION:
            self.credentials.validate_for_production()
            logger.info("Application starting in PRODUCTION mode. Credentials validated.")
        else:
            logger.info("Application starting in DEMO mode. Skipping credential validation.")
            
        logger.info("Startup validation passed successfully.")
