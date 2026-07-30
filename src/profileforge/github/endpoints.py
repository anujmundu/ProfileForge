"""Centralized GitHub Endpoint URL Definitions.

Single source of truth for GitHub REST API endpoint paths.
Endpoint paths shall never be duplicated throughout the repository.
"""


class GitHubEndpoints:
    """Factory for building normalized GitHub REST API endpoints."""

    @staticmethod
    def user() -> str:
        """Endpoint for current authenticated user."""
        return "/user"

    @staticmethod
    def user_profile(username: str) -> str:
        """Endpoint for specific user profile details."""
        return f"/users/{username}"

    @staticmethod
    def user_repositories(username: str) -> str:
        """Endpoint for public repositories of a user."""
        return f"/users/{username}/repos"

    @staticmethod
    def authenticated_user_repositories() -> str:
        """Endpoint for repositories of the authenticated user."""
        return "/user/repos"

    @staticmethod
    def repository(owner: str, repo: str) -> str:
        """Endpoint for a specific repository."""
        return f"/repos/{owner}/{repo}"

    @staticmethod
    def repository_languages(owner: str, repo: str) -> str:
        """Endpoint for repository language statistics."""
        return f"/repos/{owner}/{repo}/languages"

    @staticmethod
    def rate_limit() -> str:
        """Endpoint for rate limit status."""
        return "/rate_limit"
