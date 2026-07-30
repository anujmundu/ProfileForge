"""Configuration Diagnostics and Audit Reporting.

Tracks configuration sources, applied defaults, overridden values, and produces
redacted audit summaries.
"""

from typing import Any

from profileforge.configuration.models import ProfileForgeConfiguration


class ConfigurationDiagnostics:
    """Report and audit configuration sources and settings with guaranteed secret redaction."""

    def __init__(
        self,
        config: ProfileForgeConfiguration,
        sources: list[str],
        applied_overrides: dict[str, Any],
    ) -> None:
        self.config = config
        self.sources = sources
        self.applied_overrides = applied_overrides

    def get_summary(self) -> dict[str, Any]:
        """Generate a structured diagnostic summary with secrets redacted."""
        return {
            "app_name": self.config.app.app_name,
            "version": self.config.app.version,
            "environment": self.config.app.environment.value,
            "sources_loaded": self.sources,
            "has_github_token": self.config.github.auth_token is not None,
            "github_token_preview": (
                self.config.github.auth_token.redacted_value()
                if self.config.github.auth_token
                else None
            ),
            "output_dir": str(self.config.output.output_dir),
            "active_theme": self.config.themes.active_theme,
            "configuration_snapshot": self.config.to_dict_redacted(),
        }
