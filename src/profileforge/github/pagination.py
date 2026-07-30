"""GitHub API Link Header Parser and Pagination Metadata.

Extracts page navigation URLs and page metadata from GitHub HTTP response Link headers.
Governed by 07_GITHUB_INTEGRATION_SPECIFICATION.md.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PageMetadata:
    """Navigation URLs extracted from Link headers."""

    next_url: str | None = None
    prev_url: str | None = None
    first_url: str | None = None
    last_url: str | None = None


class GitHubPagination:
    """Link header parser for GitHub REST API pagination."""

    # Regex matching Link header format: <url>; rel="relation"
    LINK_REGEX = re.compile(r'<([^>]+)>;\s*rel="([^"]+)"')

    @classmethod
    def parse_link_header(cls, header_value: str | None) -> PageMetadata:
        """Parse raw GitHub Link header value into PageMetadata.

        Args:
            header_value: The Link header string from HTTP response.

        Returns:
            PageMetadata containing next, prev, first, and last URLs.
        """
        if not header_value:
            return PageMetadata()

        urls: dict[str, str] = {}
        for match in cls.LINK_REGEX.finditer(header_value):
            url, rel = match.group(1), match.group(2)
            urls[rel] = url

        return PageMetadata(
            next_url=urls.get("next"),
            prev_url=urls.get("prev"),
            first_url=urls.get("first"),
            last_url=urls.get("last"),
        )
