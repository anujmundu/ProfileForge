from __future__ import annotations

from pydantic import BaseModel


class Repository(BaseModel):
    name: str
    full_name: str
    description: str | None
    html_url: str

    language: str | None

    stars: int
    forks: int

    watchers: int

    open_issues: int

    is_private: bool

    is_fork: bool

    default_branch: str

    score: float = 0.0
