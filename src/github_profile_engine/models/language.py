from __future__ import annotations

from pydantic import BaseModel


class Language(BaseModel):
    name: str
    repositories: int
    percentage: float
