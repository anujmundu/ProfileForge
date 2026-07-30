"""Centralized Default Configuration Definitions.

Single source of truth for all configuration defaults across the platform.
"""

from typing import Any

from profileforge.configuration.models import ProfileForgeConfiguration

# Default configuration instance
DEFAULT_CONFIGURATION: ProfileForgeConfiguration = ProfileForgeConfiguration()


def get_default_configuration_dict() -> dict[str, Any]:
    """Return raw default configuration dictionary."""
    return DEFAULT_CONFIGURATION.model_dump()
