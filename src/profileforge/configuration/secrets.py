"""Secret Handling Utilities for Configuration Subsystem.

Ensures credentials (e.g. GitHub API tokens) are never exposed in logs,
diagnostics, representations, or serialized output.
"""

from typing import Any


class SecretStr:
    """Immutable container for sensitive string values with mandatory redaction."""

    def __init__(self, secret: str) -> None:
        if not isinstance(secret, str):
            raise TypeError("Secret value must be a string")
        self._secret: str = secret

    def get_secret_value(self) -> str:
        """Retrieve unredacted secret value for authorized API usage."""
        return self._secret

    def redacted_value(self) -> str:
        """Return a safe redacted version of the secret for display/diagnostics."""
        if not self._secret:
            return "[EMPTY]"
        if len(self._secret) <= 8:
            return "****"
        prefix = self._secret[:4]
        return f"{prefix}****"

    def __repr__(self) -> str:
        return f"SecretStr('{self.redacted_value()}')"

    def __str__(self) -> str:
        return self.redacted_value()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SecretStr):
            return self._secret == other._secret
        if isinstance(other, str):
            return self._secret == other
        return False

    def __hash__(self) -> int:
        return hash(self._secret)
