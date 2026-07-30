"""Unit tests for Configuration Subsystem.

Tests default loading, YAML parsing, environment overrides, precedence, validation,
immutability, secret redaction, and diagnostics.
"""

from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError as PydanticValidationError

from profileforge.configuration import (
    ConfigurationManager,
    ExecutionEnvironment,
    InvalidConfigurationError,
    LogLevel,
    OutputFormat,
    ProfileForgeConfiguration,
    SecretStr,
    ValidationError,
)


def test_default_configuration_loading() -> None:
    """Verify loading default configuration returns a valid root model."""
    manager = ConfigurationManager()
    config = manager.load(env_overrides={})

    assert isinstance(config, ProfileForgeConfiguration)
    assert config.app.app_name == "ProfileForge"
    assert config.app.environment == ExecutionEnvironment.DEVELOPMENT
    assert config.github.api_endpoint.unicode_string() == "https://api.github.com/"
    assert config.rendering.output_formats == [
        OutputFormat.MARKDOWN,
        OutputFormat.SVG,
        OutputFormat.JSON,
    ]


def test_yaml_configuration_loading(tmp_path: Path) -> None:
    """Verify configuration loading from a valid YAML file."""
    yaml_file = tmp_path / "custom_config.yml"
    yaml_file.write_text(
        """
app:
  debug: true
  environment: production
themes:
  active_theme: light_minimal
""",
        encoding="utf-8",
    )

    manager = ConfigurationManager(config_file=yaml_file)
    config = manager.load(env_overrides={})

    assert config.app.debug is True
    assert config.app.environment == ExecutionEnvironment.PRODUCTION
    assert config.themes.active_theme == "light_minimal"


def test_missing_optional_yaml_file() -> None:
    """Verify missing optional YAML file does not cause startup failure."""
    non_existent = Path("non_existent_config.yml")
    manager = ConfigurationManager(config_file=non_existent)
    config = manager.load(env_overrides={})

    assert config.app.app_name == "ProfileForge"


def test_malformed_yaml_file_raises_error(tmp_path: Path) -> None:
    """Verify malformed YAML file raises InvalidConfigurationError."""
    yaml_file = tmp_path / "bad.yml"
    yaml_file.write_text("app: [invalid yaml syntax", encoding="utf-8")

    manager = ConfigurationManager(config_file=yaml_file)
    with pytest.raises(InvalidConfigurationError):
        manager.load(env_overrides={})


def test_non_dict_root_yaml_raises_error(tmp_path: Path) -> None:
    """Verify root list YAML content raises InvalidConfigurationError."""
    yaml_file = tmp_path / "list.yml"
    yaml_file.write_text("- item1\n- item2\n", encoding="utf-8")

    manager = ConfigurationManager(config_file=yaml_file)
    with pytest.raises(InvalidConfigurationError):
        manager.load(env_overrides={})


def test_environment_variable_overrides() -> None:
    """Verify environment variables override default configuration."""
    env = {
        "GITHUB_TOKEN": "ghp_secret_token_1234567890",
        "PROFILEFORGE_APP_DEBUG": "true",
        "PROFILEFORGE_LOGGING_LEVEL": "DEBUG",
        "PROFILEFORGE_ANIMATION_STAGGER_INTERVAL_MS": "250",
    }

    manager = ConfigurationManager()
    config = manager.load(env_overrides=env)

    assert config.github.auth_token is not None
    assert config.github.auth_token.get_secret_value() == "ghp_secret_token_1234567890"
    assert config.app.debug is True
    assert config.logging.level == LogLevel.DEBUG
    assert config.animation.stagger_interval_ms == 250


def test_precedence_cli_over_env_over_yaml_over_defaults(tmp_path: Path) -> None:
    """Verify precedence order: CLI > Env > YAML > Defaults."""
    yaml_file = tmp_path / "config.yml"
    yaml_file.write_text("themes:\n  active_theme: yaml_theme\n", encoding="utf-8")

    env = {"PROFILEFORGE_THEMES_ACTIVE_THEME": "env_theme"}
    cli_override: dict[str, Any] = {"themes": {"active_theme": "cli_theme"}}

    manager = ConfigurationManager(config_file=yaml_file)
    config = manager.load(env_overrides=env, raw_overrides=cli_override)

    assert config.themes.active_theme == "cli_theme"


def test_secret_str_redaction() -> None:
    """Verify SecretStr never exposes raw secrets in str(), repr(), or dict conversions."""
    secret = SecretStr("ghp_secret_token_9999")

    assert secret.get_secret_value() == "ghp_secret_token_9999"
    assert "ghp_secret_token_9999" not in str(secret)
    assert "ghp_secret_token_9999" not in repr(secret)
    assert secret.redacted_value() == "ghp_****"


def test_configuration_immutability() -> None:
    """Verify configuration model raises error if mutated after validation."""
    manager = ConfigurationManager()
    config = manager.load(env_overrides={})

    with pytest.raises(PydanticValidationError):
        # Attribute assignment on frozen Pydantic model must fail
        config.app.debug = True  # type: ignore[misc]


def test_validation_scoring_weights_failure() -> None:
    """Verify scoring weights that do not sum to 1.0 raise InvalidConfigurationError."""
    invalid_weights = {
        "analytics": {
            "scoring_weights": {
                "recency": 0.5,
                "stars": 0.9,
            }
        }
    }

    manager = ConfigurationManager()
    with pytest.raises(InvalidConfigurationError):
        manager.load(env_overrides={}, raw_overrides=invalid_weights)


def test_validation_empty_output_formats_failure() -> None:
    """Verify empty output_formats list raises InvalidConfigurationError."""
    empty_formats: dict[str, Any] = {"rendering": {"output_formats": []}}

    manager = ConfigurationManager()
    with pytest.raises(InvalidConfigurationError):
        manager.load(env_overrides={}, raw_overrides=empty_formats)


def test_validation_invalid_type_raises_validation_error() -> None:
    """Verify invalid configuration type raises ValidationError."""
    invalid_data: dict[str, Any] = {"app": {"debug": "not_a_boolean"}}

    manager = ConfigurationManager()
    with pytest.raises(ValidationError):
        manager.load(env_overrides={}, raw_overrides=invalid_data)


def test_diagnostics_and_secret_redaction() -> None:
    """Verify ConfigurationDiagnostics produces safe, redacted audit summaries."""
    env = {"GITHUB_TOKEN": "ghp_secret_token_abc123"}
    manager = ConfigurationManager()
    config = manager.load(env_overrides=env)

    assert config.github.auth_token is not None
    summary = manager.diagnostics.get_summary()

    assert summary["has_github_token"] is True
    assert "ghp_secret_token_abc123" not in str(summary)
    assert summary["github_token_preview"] == "ghp_****"
    assert summary["configuration_snapshot"]["github"]["auth_token"] == "ghp_****"
