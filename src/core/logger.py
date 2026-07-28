"""
Application logging.
"""

from __future__ import annotations

import logging

LOG_LEVEL = logging.INFO

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured application logger.

    The logger is configured only once and reused for all
    subsequent requests.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler()

    handler.setFormatter(
        logging.Formatter(LOG_FORMAT)
    )

    logger.addHandler(handler)

    logger.propagate = False

    return logger