from __future__ import annotations

from pydantic import BaseModel


class Statistics(BaseModel):
    total_repositories: int

    total_stars: int

    total_forks: int

    total_watchers: int

    total_open_issues: int
