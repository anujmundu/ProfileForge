"""Deterministic Repository Scoring Engine.

Computes repository scores (0.0 - 100.0) using weights from Configuration subsystem.
Every score provides a transparent breakdown.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from datetime import UTC, datetime

from profileforge.analytics.models import RepositoryScore
from profileforge.collectors.models import Repository
from profileforge.configuration import AnalyticsCategory


class RepositoryScorer:
    """Computes deterministic repository scores and component breakdowns."""

    def __init__(self, config: AnalyticsCategory | None = None) -> None:
        self._config = config or AnalyticsCategory()
        self._weights = self._config.scoring_weights

    def compute_score(self, repository: Repository) -> RepositoryScore:
        """Compute transparent, deterministic score for a repository.

        Args:
            repository: Canonical Repository domain object.

        Returns:
            RepositoryScore containing total score and component breakdown.
        """
        w_recency = self._weights.get("recency", 0.25)
        w_stars = self._weights.get("stars", 0.20)
        w_forks = self._weights.get("forks", 0.15)
        w_activity = self._weights.get("activity", 0.25)
        w_completeness = self._weights.get("completeness", 0.15)

        # 1. Stars Component (0 - 100)
        stars_score = min(100.0, (repository.stargazers_count / 50.0) * 100.0)

        # 2. Forks Component (0 - 100)
        forks_score = min(100.0, (repository.forks_count / 20.0) * 100.0)

        # 3. Completeness Component (0 - 100)
        completeness_score = 0.0
        if repository.description:
            completeness_score += 30.0
        if repository.license_name:
            completeness_score += 25.0
        if len(repository.topics) >= 2:
            completeness_score += 25.0
        elif len(repository.topics) == 1:
            completeness_score += 15.0
        if repository.language:
            completeness_score += 20.0

        # 4. Recency Component (0 - 100)
        recency_score = self._compute_recency_score(repository.pushed_at or repository.updated_at)

        # 5. Activity Component (0 - 100)
        activity_score = self._compute_activity_score(repository)

        # Total weighted score
        total_score = (
            (stars_score * w_stars)
            + (forks_score * w_forks)
            + (completeness_score * w_completeness)
            + (activity_score * w_activity)
            + (recency_score * w_recency)
        )

        total_score = round(max(0.0, min(100.0, total_score)), 2)

        breakdown = {
            "stars_score": round(stars_score, 2),
            "forks_score": round(forks_score, 2),
            "completeness_score": round(completeness_score, 2),
            "activity_score": round(activity_score, 2),
            "recency_score": round(recency_score, 2),
        }

        return RepositoryScore(
            repository_name=repository.full_name,
            total_score=total_score,
            breakdown=breakdown,
        )

    def _compute_recency_score(self, timestamp_str: str) -> float:
        """Compute recency score based on timestamp age."""
        if not timestamp_str:
            return 20.0

        try:
            ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            now = datetime.now(UTC)
            days_old = (now - ts).days

            if days_old <= 30:
                return 100.0
            if days_old <= 90:
                return 80.0
            if days_old <= 180:
                return 60.0
            if days_old <= 365:
                return 40.0
            return 20.0
        except ValueError:
            return 20.0

    def _compute_activity_score(self, repository: Repository) -> float:
        """Compute activity score based on issue counts and push activity."""
        base = 50.0
        if repository.open_issues_count > 0:
            base += min(30.0, repository.open_issues_count * 5.0)
        if not repository.fork:
            base += 20.0
        return min(100.0, base)
