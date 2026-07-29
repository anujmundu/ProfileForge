from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def get_github_token() -> str:
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise RuntimeError("Missing GITHUB_TOKEN in .env file.")

    return token
