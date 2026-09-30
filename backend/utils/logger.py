import logging
import logging.config
from pathlib import Path

import yaml

from backend.config.loader import CONFIG_DIR


def setup_logging() -> None:
    """Configures the application's logging using the logging.yaml configuration file.

    This function sets up structured JSON logging for file output and human-readable
    formatting for console output, as defined in config/logging.yaml.
    """
    logging_config_path = CONFIG_DIR / "logging.yaml"
    
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    if logging_config_path.exists():
        with open(logging_config_path, "r", encoding="utf-8") as f:
            try:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
                logging.getLogger(__name__).info("Logging configured successfully from logging.yaml")
            except Exception as e:
                logging.basicConfig(level=logging.INFO)
                logging.getLogger(__name__).error(f"Failed to load logging config, using defaults: {e}")
    else:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).warning("logging.yaml not found, using basic configuration.")
