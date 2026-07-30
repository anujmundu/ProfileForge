"""Configuration Subsystem.

Centralized, strongly typed, and immutable configuration management for ProfileForge.
Governed by 11_CONFIGURATION_SPECIFICATION.md.
"""

from profileforge.configuration.exceptions import (
    ConfigurationError,
    InvalidConfigurationError,
    MissingConfigurationError,
    SecretExposureError,
    ValidationError,
)
from profileforge.configuration.manager import ConfigurationManager
from profileforge.configuration.models import (
    AnalyticsCategory,
    AnimationCategory,
    ApplicationCategory,
    AutomationCategory,
    DiagnosticsCategory,
    EasingPreset,
    ExecutionEnvironment,
    ExperimentalCategory,
    GitHubCategory,
    LoggingCategory,
    LogLevel,
    OutputCategory,
    OutputFormat,
    OverwritePolicy,
    PerformanceCategory,
    ProfileForgeConfiguration,
    RenderingCategory,
    ThemesCategory,
    TimingPreset,
)
from profileforge.configuration.secrets import SecretStr

__all__ = [
    "AnalyticsCategory",
    "AnimationCategory",
    "ApplicationCategory",
    "AutomationCategory",
    "ConfigurationError",
    "ConfigurationManager",
    "DiagnosticsCategory",
    "EasingPreset",
    "ExecutionEnvironment",
    "ExperimentalCategory",
    "GitHubCategory",
    "InvalidConfigurationError",
    "LoggingCategory",
    "LogLevel",
    "MissingConfigurationError",
    "OutputCategory",
    "OutputFormat",
    "OverwritePolicy",
    "PerformanceCategory",
    "ProfileForgeConfiguration",
    "RenderingCategory",
    "SecretExposureError",
    "SecretStr",
    "ThemesCategory",
    "TimingPreset",
    "ValidationError",
]
