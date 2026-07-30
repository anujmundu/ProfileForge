"""Configuration Schema and Boundary Validator.

Validates raw merged dictionaries against ProfileForgeConfiguration Pydantic models
and raises structured domain exceptions on validation failure.
"""

from typing import Any

from pydantic import ValidationError as PydanticValidationError

from profileforge.configuration.exceptions import InvalidConfigurationError, ValidationError
from profileforge.configuration.models import ProfileForgeConfiguration
from profileforge.configuration.secrets import SecretStr


def validate_configuration_dict(data: dict[str, Any]) -> ProfileForgeConfiguration:
    """Validate a raw configuration dictionary and construct the immutable root model.

    Args:
        data: Raw merged configuration dictionary.

    Returns:
        Validated ProfileForgeConfiguration instance.

    Raises:
        ValidationError: If schema or field validation fails.
    """
    # Wrap plain string auth_token into SecretStr if present in dictionary
    if "github" in data and isinstance(data["github"], dict):
        raw_token = data["github"].get("auth_token")
        if isinstance(raw_token, str) and raw_token:
            data["github"]["auth_token"] = SecretStr(raw_token)

    try:
        config = ProfileForgeConfiguration.model_validate(data)
        _perform_domain_validation(config)
        return config
    except PydanticValidationError as exc:
        details = "; ".join(
            f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        )
        raise ValidationError(f"Configuration validation failed: {details}") from exc


def _perform_domain_validation(config: ProfileForgeConfiguration) -> None:
    """Perform cross-field and domain constraint validation."""
    # 1. Output formats check
    if not config.rendering.output_formats:
        raise InvalidConfigurationError(
            "rendering.output_formats cannot be empty. At least one format must be enabled."
        )

    # 2. Analytics scoring weights check
    if config.analytics.scoring_weights:
        total_weight = sum(config.analytics.scoring_weights.values())
        if abs(total_weight - 1.0) > 0.05:
            raise InvalidConfigurationError(
                f"analytics.scoring_weights must sum to 1.0 (got {total_weight:.2f})."
            )
