"""
Typed configuration models for the GitHub Profile Engine.
"""

from datetime import date
from typing import List

from pydantic import BaseModel, Field


class Theme(BaseModel):
    background: str
    card: str
    border: str

    primary: str
    secondary: str
    accent: str

    text: str
    subtext: str

    font: str


class Project(BaseModel):
    name: str
    category: str
    status: str
    progress: int = Field(ge=0, le=100)


class CurrentResearch(BaseModel):
    title: str
    status: str
    progress: int = Field(ge=0, le=100)


class Research(BaseModel):
    papers_read: int
    currently_reading: CurrentResearch
    completed: List[str]
    domains: List[str]
    research_goal: str
    last_updated: date
    
class GitHubConfig(BaseModel):
    username: str
    repository: str
    cache_minutes: int = Field(ge=1)