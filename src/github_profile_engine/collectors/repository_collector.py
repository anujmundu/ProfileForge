from __future__ import annotations

from github_profile_engine.models.repository import Repository


class RepositoryCollector:
    """
    Converts GitHub repositories into our internal Repository model.
    """

    @staticmethod
    def collect(user) -> list[Repository]:
        repositories: list[Repository] = []

        for repo in user.get_repos(sort="updated"):
            repositories.append(
                Repository(
                    name=repo.name,
                    full_name=repo.full_name,
                    description=repo.description,
                    html_url=repo.html_url,
                    language=repo.language,
                    stars=repo.stargazers_count,
                    forks=repo.forks_count,
                    watchers=repo.watchers_count,
                    open_issues=repo.open_issues_count,
                    is_private=repo.private,
                    is_fork=repo.fork,
                    default_branch=repo.default_branch,
                )
            )

        return repositories
