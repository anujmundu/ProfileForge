from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class GeneratedFile(BaseModel):
    """
    Represents a generated artifact.
    """

    path: Path

    content: str
