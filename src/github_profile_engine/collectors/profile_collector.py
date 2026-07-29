from __future__ import annotations

from github_profile_engine.collectors.repository_collector import RepositoryCollector
from github_profile_engine.models.profile import Profile
from github_profile_engine.models.statistics import Statistics
from github_profile_engine.models.user import User


class ProfileCollector:
    """
    Builds the complete Profile domain model.
    """

    @staticmethod
    def collect(github_user) -> Profile:
        repositories = RepositoryCollector.collect(github_user)

        user = User(
            login=github_user.login,
            name=github_user.name,
            bio=github_user.bio,
            company=github_user.company,
            location=github_user.location,
            avatar_url=github_user.avatar_url,
            html_url=github_user.html_url,
            followers=github_user.followers,
            following=github_user.following,
            public_repositories=github_user.public_repos,
            public_gists=github_user.public_gists,
        )

        statistics = Statistics(
            total_repositories=len(repositories),
            total_stars=sum(r.stars for r in repositories),
            total_forks=sum(r.forks for r in repositories),
            total_watchers=sum(r.watchers for r in repositories),
            total_open_issues=sum(r.open_issues for r in repositories),
        )

        return Profile(
            user=user,
            repositories=repositories,
            statistics=statistics,
        )
