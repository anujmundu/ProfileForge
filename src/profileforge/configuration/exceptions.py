"""Configuration Subsystem Exception Hierarchy.

Governed by 11_CONFIGURATION_SPECIFICATION.md and 01_ENGINEERING_QUALITY_GATES.md.
"""

from profileforge.exceptions import ProfileForgeError


class ConfigurationError(ProfileForgeError):
    """Base exception for all configuration subsystem errors."""


class ValidationError(ConfigurationError):
    """Raised when configuration validation fails."""


class MissingConfigurationError(ConfigurationError):
    """Raised when a required configuration value or file is missing."""


class InvalidConfigurationError(ConfigurationError):
    """Raised when a configuration field contains an invalid value or type."""


class SecretExposureError(ConfigurationError):
    """Raised when a secret is inadvertently exposed or improperly handled."""
