"""
GitHub data collectors.

Collectors transform PyGithub objects into the application's
domain models.
"""

from github.NamedUser import NamedUser
from github.Repository import Repository

from src.github.api import GitHubClient
from src.github.models import RepositorySummary
from src.github.models import UserProfile

class GitHubCollector:
    """Collects GitHub data and converts it into domain models."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client
        
    def collect_profile(self) -> UserProfile:
        """Collect the configured user's public profile."""

        user: NamedUser = self._client.fetch_user()

        return UserProfile(
            username=user.login,
            name=user.name,
            bio=user.bio,
            avatar_url=user.avatar_url,
            followers=user.followers,
            following=user.following,
            public_repositories=user.public_repos,
        )
        
    def collect_repositories(self) -> list[RepositorySummary]:
        """Collect all public repositories."""

        repositories = self._client.fetch_repositories()

        return [
            RepositorySummary(
                name=repo.name,
                description=repo.description,
                language=repo.language,

                stars=repo.stargazers_count,
                forks=repo.forks_count,

                archived=repo.archived,
                fork=repo.fork,

                html_url=repo.html_url,

                created_at=repo.created_at,
                updated_at=repo.updated_at,
                pushed_at=repo.pushed_at,

                default_branch=repo.default_branch,

                visibility=repo.visibility,

                size=repo.size,

                topics=repo.get_topics(),

                license_name=(
                    repo.license.name
                    if repo.license is not None
                    else None
                ),
            )
            for repo in repositories
        ]