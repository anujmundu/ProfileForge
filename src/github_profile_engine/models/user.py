from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    login: str
    name: str | None
    bio: str | None
    company: str | None
    location: str | None

    avatar_url: str
    html_url: str

    followers: int
    following: int

    public_repositories: int

    public_gists: int
