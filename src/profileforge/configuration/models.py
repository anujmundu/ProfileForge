"""Strongly Typed Configuration Models for ProfileForge.

Defines immutable Pydantic v2 models for each configuration category and
the root ProfileForgeConfiguration model.
"""

from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from profileforge import __version__
from profileforge.configuration.secrets import SecretStr


class ExecutionEnvironment(StrEnum):
    """Supported execution environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Supported logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class OutputFormat(StrEnum):
    """Supported rendering output formats."""

    MARKDOWN = "markdown"
    SVG = "svg"
    JSON = "json"


class TimingPreset(StrEnum):
    """Animation timing duration presets."""

    INSTANT = "instant"
    FAST = "fast"
    NORMAL = "normal"
    SLOW = "slow"
    EXTENDED = "extended"


class EasingPreset(StrEnum):
    """Animation easing function presets."""

    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"


class OverwritePolicy(StrEnum):
    """Asset export overwrite policies."""

    ALWAYS = "always"
    NEVER = "never"
    IF_NEWER = "if_newer"


class ApplicationCategory(BaseModel):
    """Application level operational settings."""

    model_config = ConfigDict(frozen=True)

    app_name: str = "ProfileForge"
    version: str = Field(default_factory=lambda: __version__)
    environment: ExecutionEnvironment = ExecutionEnvironment.DEVELOPMENT
    debug: bool = False
    diagnostics_enabled: bool = True


class GitHubCategory(BaseModel):
    """GitHub API integration settings."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    auth_token: SecretStr | None = None
    api_endpoint: HttpUrl = Field(default_factory=lambda: HttpUrl("https://api.github.com"))
    timeout_seconds: float = Field(default=30.0, gt=0.0)
    max_retries: int = Field(default=3, ge=0, le=10)
    backoff_factor: float = Field(default=2.0, ge=1.0)
    cache_enabled: bool = True
    cache_ttl_seconds: int = Field(default=3600, ge=0)


class RenderingCategory(BaseModel):
    """Output rendering settings."""

    model_config = ConfigDict(frozen=True)

    output_formats: list[OutputFormat] = Field(
        default_factory=lambda: [
            OutputFormat.MARKDOWN,
            OutputFormat.SVG,
            OutputFormat.JSON,
        ]
    )
    enabled_renderers: list[str] = Field(
        default_factory=lambda: ["markdown", "svg", "json"]
    )
    template_dir: Path = Field(default_factory=lambda: Path("assets/templates"))
    layout_preference: str = "modern_grid"
    validate_output: bool = True


class ThemesCategory(BaseModel):
    """Visual theme settings."""

    model_config = ConfigDict(frozen=True)

    active_theme: str = "dark_glassmorphism"
    color_palette: dict[str, str] = Field(
        default_factory=lambda: {
            "background": "#0d1117",
            "card_bg": "#161b22",
            "border": "#30363d",
            "primary": "#58a6ff",
            "secondary": "#bc8cff",
            "text": "#c9d1d9",
            "accent": "#3fb950",
        }
    )
    typography: str = "Inter, sans-serif"
    icon_set: str = "octicons"
    spacing_preset: str = "comfortable"
    border_style: str = "rounded"


class AnimationCategory(BaseModel):
    """Animation engine settings."""

    model_config = ConfigDict(frozen=True)

    enabled: bool = True
    reduced_motion: bool = False
    timing_preset: TimingPreset = TimingPreset.NORMAL
    easing_preset: EasingPreset = EasingPreset.EASE_IN_OUT
    stagger_interval_ms: int = Field(default=100, ge=0, le=5000)
    animation_theme: str = "smooth_fade"


class AnalyticsCategory(BaseModel):
    """Repository scoring and intelligence settings."""

    model_config = ConfigDict(frozen=True)

    scoring_weights: dict[str, float] = Field(
        default_factory=lambda: {
            "recency": 0.25,
            "stars": 0.20,
            "forks": 0.15,
            "activity": 0.25,
            "completeness": 0.15,
        }
    )
    featured_repo_count: int = Field(default=6, ge=1, le=20)
    category_mappings: dict[str, str] = Field(
        default_factory=lambda: {
            "pytorch": "Artificial Intelligence",
            "tensorflow": "Machine Learning",
            "fastapi": "Backend Development",
            "react": "Frontend Development",
        }
    )
    technology_aliases: dict[str, str] = Field(
        default_factory=lambda: {
            "py": "Python",
            "ts": "TypeScript",
            "js": "JavaScript",
        }
    )
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    research_keywords: list[str] = Field(
        default_factory=lambda: [
            "paper",
            "arxiv",
            "benchmark",
            "dataset",
            "experiment",
        ]
    )


class LoggingCategory(BaseModel):
    """Structured logging configuration."""

    model_config = ConfigDict(frozen=True)

    level: LogLevel = LogLevel.INFO
    destination: str = "stdout"
    format: str = "structured"
    diagnostics_verbosity: int = Field(default=1, ge=0, le=3)


class AutomationCategory(BaseModel):
    """GitHub Actions automation settings."""

    model_config = ConfigDict(frozen=True)

    enabled: bool = True
    trigger_events: list[str] = Field(
        default_factory=lambda: ["push", "schedule", "workflow_dispatch"]
    )
    auto_commit: bool = True
    commit_message_template: str = (
        "chore(profile): auto-update GitHub profile assets [skip ci]"
    )
    workflow_file: str = ".github/workflows/update_profile.yml"


class OutputCategory(BaseModel):
    """Export and file path configuration."""

    model_config = ConfigDict(frozen=True)

    output_dir: Path = Field(default_factory=lambda: Path("assets/generated"))
    readme_filename: str = "README.md"
    asset_naming_pattern: str = "{category}_{name}.svg"
    overwrite_policy: OverwritePolicy = OverwritePolicy.ALWAYS


class DiagnosticsCategory(BaseModel):
    """Diagnostics and telemetry configuration."""

    model_config = ConfigDict(frozen=True)

    collect_timing: bool = True
    subsystem_metrics: bool = True
    summary_enabled: bool = True
    report_warnings: bool = True


class PerformanceCategory(BaseModel):
    """Performance & concurrency settings."""

    model_config = ConfigDict(frozen=True)

    cache_enabled: bool = True
    cache_ttl_seconds: int = Field(default=3600, ge=0)
    concurrency_limit: int = Field(default=5, ge=1, le=50)
    max_retry_attempts: int = Field(default=3, ge=0, le=10)


class ExperimentalCategory(BaseModel):
    """Experimental feature flags."""

    model_config = ConfigDict(frozen=True)

    feature_flags: dict[str, bool] = Field(default_factory=dict)


class ProfileForgeConfiguration(BaseModel):
    """Root immutable configuration model for the ProfileForge platform."""

    model_config = ConfigDict(frozen=True)

    app: ApplicationCategory = Field(default_factory=ApplicationCategory)
    github: GitHubCategory = Field(default_factory=GitHubCategory)
    rendering: RenderingCategory = Field(default_factory=RenderingCategory)
    themes: ThemesCategory = Field(default_factory=ThemesCategory)
    animation: AnimationCategory = Field(default_factory=AnimationCategory)
    analytics: AnalyticsCategory = Field(default_factory=AnalyticsCategory)
    logging: LoggingCategory = Field(default_factory=LoggingCategory)
    automation: AutomationCategory = Field(default_factory=AutomationCategory)
    output: OutputCategory = Field(default_factory=OutputCategory)
    diagnostics: DiagnosticsCategory = Field(default_factory=DiagnosticsCategory)
    performance: PerformanceCategory = Field(default_factory=PerformanceCategory)
    experimental: ExperimentalCategory = Field(
        default_factory=ExperimentalCategory
    )

    def to_dict_redacted(self) -> dict[str, Any]:
        """Return raw configuration dict with all secret fields safely redacted."""
        data = self.model_dump()

        # Handle secret redaction in github category
        if "github" in data and isinstance(data["github"], dict):
            if self.github.auth_token is not None:
                data["github"]["auth_token"] = self.github.auth_token.redacted_value()
            else:
                data["github"]["auth_token"] = None

        return data
