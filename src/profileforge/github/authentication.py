"""GitHub Authenticator and Header Factory.

Supports Personal Access Tokens (PAT) and Anonymous mode.
Integrates strictly with Configuration subsystem SecretStr handling.
Guarantees credentials are never exposed in string representations or logs.
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""


from profileforge.configuration import SecretStr


class GitHubAuthenticator:
    """Authenticator managing headers and authentication mode for GitHub requests."""

    def __init__(self, auth_token: SecretStr | str | None = None) -> None:
        if isinstance(auth_token, str):
            self._auth_token: SecretStr | None = SecretStr(auth_token) if auth_token else None
        else:
            self._auth_token = auth_token

    @property
    def is_authenticated(self) -> bool:
        """Check if authenticator operates in authenticated mode (vs. anonymous)."""
        return self._auth_token is not None and bool(self._auth_token.get_secret_value())

    def get_headers(self) -> dict[str, str]:
        """Generate HTTP headers for GitHub API requests."""
        headers: dict[str, str] = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ProfileForge-Engine",
        }

        if self.is_authenticated and self._auth_token is not None:
            token_val = self._auth_token.get_secret_value()
            headers["Authorization"] = f"Bearer {token_val}"

        return headers

    def __repr__(self) -> str:
        mode = "Authenticated" if self.is_authenticated else "Anonymous"
        preview = (
            self._auth_token.redacted_value()
            if self._auth_token is not None
            else "None"
        )
        return f"GitHubAuthenticator(mode='{mode}', token='{preview}')"

    def __str__(self) -> str:
        return self.__repr__()
