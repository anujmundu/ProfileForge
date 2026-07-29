from __future__ import annotations

from pydantic import BaseModel

from github_profile_engine.models.repository import Repository
from github_profile_engine.models.statistics import Statistics
from github_profile_engine.models.user import User


class Profile(BaseModel):
    user: User

    repositories: list[Repository]

    statistics: Statistics
