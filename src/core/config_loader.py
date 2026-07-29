"""
Configuration loading service.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.core.models import (
    GitHubConfig,
    Project,
    Research,
    Theme,
)


class ConfigLoader:
    """
    Singleton configuration loader.

    Loads JSON configuration once and caches validated
    configuration objects.
    """

    _instance: ConfigLoader | None = None
    _cache: dict[str, object]

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    CONFIG_DIR = PROJECT_ROOT / "config"

    def __new__(cls) -> ConfigLoader:
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._cache = {}
            cls._instance = instance

        return cls._instance

    def _load_json(self, filename: str) -> Any:
        path = self.CONFIG_DIR / filename

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def load_theme(self) -> Theme:
        cached = self._cache.get("theme")

        if cached is None:
            cached = Theme(**self._load_json("theme.json"))
            self._cache["theme"] = cached

        assert isinstance(cached, Theme)
        return cached

    def load_projects(self) -> list[Project]:
        cached = self._cache.get("projects")

        if cached is None:
            cached = [
                Project(**project) for project in self._load_json("projects.json")
            ]
            self._cache["projects"] = cached

        assert isinstance(cached, list)
        return cached

    def load_research(self) -> Research:
        cached = self._cache.get("research")

        if cached is None:
            cached = Research(**self._load_json("research.json"))
            self._cache["research"] = cached

        assert isinstance(cached, Research)
        return cached

    def load_github(self) -> GitHubConfig:
        cached = self._cache.get("github")

        if cached is None:
            cached = GitHubConfig(**self._load_json("github.json"))
            self._cache["github"] = cached

        assert isinstance(cached, GitHubConfig)
        return cached

    def clear_cache(self) -> None:
        self._cache.clear()
