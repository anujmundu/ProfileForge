"""Repository Scoring and Featured Selection Analyzer.

Ranks repositories deterministically using RepositoryScorer and selects featured projects.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from profileforge.analytics.models import (
    FeaturedRepositories,
    RankedRepository,
    RepositoryRanking,
)
from profileforge.analytics.scoring import RepositoryScorer
from profileforge.collectors.models import RepositoryCollection
from profileforge.configuration import AnalyticsCategory


class RepositoryAnalyzer:
    """Analyzer for repository scoring, ranking, and featured repository selection."""

    def __init__(
        self,
        scorer: RepositoryScorer | None = None,
        config: AnalyticsCategory | None = None,
    ) -> None:
        self._scorer = scorer or RepositoryScorer(config)
        self._config = config or AnalyticsCategory()

    def analyze_ranking(self, repos: RepositoryCollection) -> RepositoryRanking:
        """Score and rank all repositories deterministically with stable tie-breaking.

        Sorting key: (-total_score, repository.name)
        """
        scored: list[tuple[float, str, RankedRepository]] = []

        for repo in repos.repositories:
            score = self._scorer.compute_score(repo)
            ranked = RankedRepository(rank=1, repository=repo, score=score)
            scored.append((score.total_score, repo.name, ranked))

        # Deterministic sorting: highest score first, then alphabetical by name
        scored.sort(key=lambda item: (-item[0], item[1].lower()))

        ranked_list: list[RankedRepository] = []
        for index, (_, _, ranked_item) in enumerate(scored, start=1):
            ranked_list.append(
                RankedRepository(
                    rank=index,
                    repository=ranked_item.repository,
                    score=ranked_item.score,
                )
            )

        return RepositoryRanking(
            ranked_repositories=ranked_list,
            total_count=len(ranked_list),
        )

    def select_featured(
        self, ranking: RepositoryRanking, limit: int | None = None
    ) -> FeaturedRepositories:
        """Select top N featured repositories from ranking."""
        count = limit if limit is not None else self._config.featured_repo_count
        featured_list = ranking.ranked_repositories[:count]

        return FeaturedRepositories(
            featured=featured_list,
            count=len(featured_list),
        )
