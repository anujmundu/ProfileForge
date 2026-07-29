from __future__ import annotations

from collections import Counter

from github_profile_engine.models.language import Language
from github_profile_engine.models.repository import Repository


class LanguageAnalyzer:
    """
    Computes language usage statistics from repositories.
    """

    @staticmethod
    def analyze(repositories: list[Repository]) -> list[Language]:
        counter = Counter(
            repository.language
            for repository in repositories
            if repository.language is not None
        )

        total = sum(counter.values())

        if total == 0:
            return []

        languages: list[Language] = []

        for name, count in counter.most_common():
            languages.append(
                Language(
                    name=name,
                    repositories=count,
                    percentage=round((count / total) * 100, 2),
                )
            )

        return languages
