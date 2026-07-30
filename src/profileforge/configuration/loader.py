"""Configuration File Loader.

Loads YAML configuration files and performs deep merging of configuration sources.
"""

from pathlib import Path
from typing import Any

import yaml

from profileforge.configuration.exceptions import InvalidConfigurationError


def load_yaml_file(file_path: Path | str) -> dict[str, Any]:
    """Load configuration from a YAML file.

    Args:
        file_path: Path to the YAML configuration file.

    Returns:
        Dictionary containing raw configuration settings.

    Raises:
        InvalidConfigurationError: If the YAML file is malformed or not a dictionary.
    """
    path = Path(file_path)

    if not path.is_file():
        return {}

    try:
        content = path.read_text(encoding="utf-8")
        if not content.strip():
            return {}

        parsed = yaml.safe_load(content)

        if parsed is None:
            return {}

        if not isinstance(parsed, dict):
            raise InvalidConfigurationError(
                f"Configuration file '{path}' must contain a key-value mapping at root."
            )

        return parsed
    except yaml.YAMLError as exc:
        raise InvalidConfigurationError(
            f"Failed to parse YAML configuration file '{path}': {exc}"
        ) from exc
    except Exception as exc:
        if isinstance(exc, InvalidConfigurationError):
            raise
        raise InvalidConfigurationError(
            f"Error reading configuration file '{path}': {exc}"
        ) from exc


def deep_merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge override dictionary into base dictionary.

    Args:
        base: The base dictionary (e.g., default configuration).
        override: The overriding dictionary.

    Returns:
        Merged dictionary.
    """
    result = base.copy()

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value

    return result
