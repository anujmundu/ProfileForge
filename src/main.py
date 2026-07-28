"""
Application entry point.

Generates the GitHub profile dashboard SVG.
"""

from pathlib import Path

from src.bootstrap.container import build_dashboard_generator
from src.core.application import app


def write_dashboard(
    svg: str,
    output_path: Path,
) -> None:
    """
    Persist the generated SVG dashboard.

    Args:
        svg:
            SVG document.

        output_path:
            Destination file.
    """

    output_path.write_text(
        svg,
        encoding="utf-8",
    )


def main() -> None:
    """Generate the GitHub profile dashboard."""

    logger = app.logger

    try:
        logger.info("Building application...")

        generator = build_dashboard_generator()

        logger.info("Generating dashboard...")

        svg = generator.generate()

        output_path = Path("dashboard.svg")

        write_dashboard(
            svg=svg,
            output_path=output_path,
        )

        logger.info(
            "Dashboard written to '%s'.",
            output_path.resolve(),
        )

        logger.info(
            "Dashboard generation completed successfully."
        )

    except Exception:
        logger.exception(
            "Dashboard generation failed."
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()