from __future__ import annotations

from pydantic import BaseModel

from github_profile_engine.models.repository import Repository


class RepositoryInsight(BaseModel):
    """
    Enriched repository information used by renderers.
    """

    repository: Repository

    score: float

    category: str

    maturity: str

    technologies: list[str]

    tags: list[str]
