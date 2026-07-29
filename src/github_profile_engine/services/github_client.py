from __future__ import annotations

from github import Auth, Github


class GitHubClient:
    """
    Thin wrapper around the PyGithub client.
    """

    def __init__(self, token: str):
        auth = Auth.Token(token)
        self.client = Github(auth=auth)

    def get_user(self, username: str):
        return self.client.get_user(username)

    def close(self) -> None:
        self.client.close()
