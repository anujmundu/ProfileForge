from __future__ import annotations

from pydantic import BaseModel

from github_profile_engine.models.language import Language
from github_profile_engine.models.profile import Profile
from github_profile_engine.models.repository import Repository


class ProfileContext(BaseModel):
    """
    Fully analyzed profile ready for rendering.
    """

    profile: Profile

    featured_repositories: list[Repository]

    languages: list[Language]
