"""Environment Variable Configuration Resolver.

Loads and maps environment variables into structured configuration dictionaries.
Environment settings override file-based settings and defaults.
"""

import os
from typing import Any

ENV_PREFIX = "PROFILEFORGE_"

# Known direct environment variable mappings
SPECIAL_ENV_MAPPINGS: dict[str, tuple[str, str]] = {
    "GITHUB_TOKEN": ("github", "auth_token"),
    "GH_TOKEN": ("github", "auth_token"),
    "PROFILEFORGE_TOKEN": ("github", "auth_token"),
}


def load_environment_variables(env: dict[str, str] | None = None) -> dict[str, Any]:
    """Parse environment variables into a nested configuration dictionary.

    Args:
        env: Optional environment dictionary override (defaults to os.environ).

    Returns:
        Nested dictionary containing environment configuration overrides.
    """
    target_env = os.environ if env is None else env
    overrides: dict[str, Any] = {}

    # 1. Process special environment variables
    for env_var, (category, key) in SPECIAL_ENV_MAPPINGS.items():
        if env_var in target_env and target_env[env_var]:
            if category not in overrides:
                overrides[category] = {}
            overrides[category][key] = target_env[env_var]

    # 2. Process standard PREFIXED variables (PROFILEFORGE_<CATEGORY>_<KEY>)
    for env_var, value in target_env.items():
        if not env_var.startswith(ENV_PREFIX):
            continue

        stripped = env_var[len(ENV_PREFIX) :].lower()
        parts = stripped.split("_", 1)

        if len(parts) != 2 or not parts[0] or not parts[1]:
            continue

        category, key = parts[0], parts[1]

        if category not in overrides:
            overrides[category] = {}

        # Parse string primitive types safely
        overrides[category][key] = _parse_env_value(value)

    return overrides


def _parse_env_value(val: str) -> Any:
    """Parse raw string environment variable into appropriate primitive type."""
    cleaned = val.strip()

    if cleaned.lower() == "true":
        return True
    if cleaned.lower() == "false":
        return False

    # Int conversion
    try:
        if cleaned.isdigit() or (cleaned.startswith("-") and cleaned[1:].isdigit()):
            return int(cleaned)
    except ValueError:
        pass

    # Float conversion
    try:
        return float(cleaned)
    except ValueError:
        pass

    # Comma-separated list check
    if "," in cleaned:
        return [item.strip() for item in cleaned.split(",") if item.strip()]

    return cleaned
