from github import Github

from src.core.application import app


class GitHubClient:
    """Wrapper around the PyGithub client."""

    def __init__(self) -> None:
        config = app.config.load_github()

        self._client = Github()
        self._username = config.username

    def get_user(self):
        return self._client.get_user(self._username)