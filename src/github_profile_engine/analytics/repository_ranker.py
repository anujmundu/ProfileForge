from __future__ import annotations

from github_profile_engine.models.repository import Repository


class RepositoryRanker:
    """
    Scores repositories for showcasing.
    """

    STAR_WEIGHT = 5.0
    FORK_WEIGHT = 3.0
    WATCHER_WEIGHT = 2.0

    DESCRIPTION_BONUS = 2.0
    LANGUAGE_BONUS = 1.0

    FORK_PENALTY = -5.0
    PRIVATE_PENALTY = -100.0

    @classmethod
    def score(cls, repository: Repository) -> float:
        score = 0.0

        score += repository.stars * cls.STAR_WEIGHT
        score += repository.forks * cls.FORK_WEIGHT
        score += repository.watchers * cls.WATCHER_WEIGHT

        if repository.description:
            score += cls.DESCRIPTION_BONUS

        if repository.language:
            score += cls.LANGUAGE_BONUS

        if repository.is_fork:
            score += cls.FORK_PENALTY

        if repository.is_private:
            score += cls.PRIVATE_PENALTY

        return round(score, 2)

    @classmethod
    def rank(cls, repositories: list[Repository]) -> list[Repository]:
        ranked: list[Repository] = []

        for repository in repositories:
            repository.score = cls.score(repository)
            ranked.append(repository)

        ranked.sort(
            key=lambda repository: repository.score,
            reverse=True,
        )

        return ranked
