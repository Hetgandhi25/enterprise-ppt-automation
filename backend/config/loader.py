import json
import logging
from pathlib import Path
from typing import Any, Dict

import yaml

logger = logging.getLogger(__name__)

CONFIG_DIR = Path(__file__).parent


def load_yaml_config(filename: str) -> Dict[str, Any]:
    """Loads a YAML configuration file from the config directory.

    Args:
        filename: Name of the YAML file.

    Returns:
        Dict[str, Any]: The parsed YAML content.
    """
    filepath = CONFIG_DIR / filename
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {filepath}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {filepath}: {e}")
        return {}


def load_json_config(filename: str) -> Dict[str, Any]:
    """Loads a JSON configuration file from the config directory.

    Args:
        filename: Name of the JSON file.

    Returns:
        Dict[str, Any]: The parsed JSON content.
    """
    filepath = CONFIG_DIR / filename
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {filepath}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file {filepath}: {e}")
        return {}
