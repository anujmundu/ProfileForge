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

    Loads JSON configuration once
    and caches validated objects.
    """

    _instance: "ConfigLoader | None" = None

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    CONFIG_DIR = PROJECT_ROOT / "config"

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)
            cls._instance._cache = {}

        return cls._instance

    def _load_json(self, filename: str) -> Any:

        path = self.CONFIG_DIR / filename

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def load_theme(self) -> Theme:

        if "theme" not in self._cache:

            self._cache["theme"] = Theme(
                **self._load_json("theme.json")
            )

        return self._cache["theme"]

    def load_projects(self) -> list[Project]:

        if "projects" not in self._cache:

            self._cache["projects"] = [

                Project(**project)

                for project

                in self._load_json("projects.json")

            ]

        return self._cache["projects"]

    def load_research(self) -> Research:

        if "research" not in self._cache:

            self._cache["research"] = Research(
                **self._load_json("research.json")
            )

        return self._cache["research"]

    def clear_cache(self) -> None:

        self._cache.clear()
        
    def load_github(self) -> GitHubConfig:

        if "github" not in self._cache:

            self._cache["github"] = GitHubConfig(
                **self._load_json("github.json")
            )

        return self._cache["github"]