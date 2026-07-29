from pathlib import Path

from github_profile_engine.engine import ProfileEngine


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]

    engine = ProfileEngine(project_root)

    engine.run()


if __name__ == "__main__":
    main()
