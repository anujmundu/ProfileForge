from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------
# Configuration Models
# ---------------------------------------------------------------------


class ProfileConfig(BaseModel):
    github_username: str


class PersonalConfig(BaseModel):
    name: str
    headline: str
    location: str
    bio: str


class SocialConfig(BaseModel):
    github: str
    linkedin: str = ""
    twitter: str = ""
    website: str = ""


class CareerConfig(BaseModel):
    currently_learning: list[str] = Field(default_factory=list)
    open_to_work: bool = True


class ThemeConfig(BaseModel):
    active: str


class ProfileConfiguration(BaseModel):
    profile: ProfileConfig
    personal: PersonalConfig
    social: SocialConfig
    career: CareerConfig
    theme: ThemeConfig


# ---------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------


class ConfigurationLoader:
    """
    Loads every configuration file inside the config directory.
    """

    def __init__(self, config_directory: Path):
        self.config_directory = config_directory

    def _load_yaml(self, filename: str) -> dict[str, Any]:
        path = self.config_directory / filename

        if not path.exists():
            raise FileNotFoundError(f"Missing configuration file: {path}")

        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def load_profile(self) -> ProfileConfiguration:
        data = self._load_yaml("profile.yaml")
        return ProfileConfiguration.model_validate(data)
