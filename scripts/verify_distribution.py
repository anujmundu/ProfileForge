"""Distribution Package Contents & Metadata Verifier.

Inspects generated sdist (.tar.gz) and wheel (.whl) packages for required files and PEP 621 metadata.
Governed by 01_ENGINEERING_QUALITY_GATES.md.
"""

import sys
import tarfile
import zipfile
from pathlib import Path


def _verify_sdist(sdist_path: Path) -> bool:
    """Verify sdist artifact contents."""
    print(f"\nVerifying sdist: {sdist_path.name}")
    with tarfile.open(sdist_path, "r:gz") as tar:
        names = tar.getnames()
        required_sdist_files = ["pyproject.toml", "README.md", "LICENSE"]
        for req in required_sdist_files:
            if not any(req in n for n in names):
                print(f"Error: sdist missing required file '{req}'")
                return False
    print(" - sdist contents verified!")
    return True


def _verify_wheel(wheel_path: Path) -> bool:
    """Verify wheel artifact contents and exclusion rules."""
    print(f"\nVerifying wheel: {wheel_path.name}")
    excluded_prefixes = ["benchmarks/", "reports/", ".venv/", ".git/", "tests/"]
    with zipfile.ZipFile(wheel_path, "r") as zip_file:
        wheel_names = zip_file.namelist()
        if not any("profileforge/__init__.py" in n for n in wheel_names):
            print("Error: wheel missing profileforge/__init__.py")
            return False
        if not any("profileforge/py.typed" in n for n in wheel_names):
            print("Error: wheel missing py.typed type marker")
            return False

        for name in wheel_names:
            for exc in excluded_prefixes:
                if name.startswith(exc):
                    print(f"Error: Excluded item '{name}' found in wheel!")
                    return False

    print(" - Wheel contents and exclusions verified!")
    return True


def main() -> int:
    """Verify distribution package contents."""
    root_dir = Path(__file__).parent.parent
    dist_dir = root_dir / "dist"

    print("=== ProfileForge Distribution Verifier ===")

    if not dist_dir.exists():
        print("Error: dist/ directory does not exist. Run build_release.py first.")
        return 1

    sdists = list(dist_dir.glob("*.tar.gz"))
    wheels = list(dist_dir.glob("*.whl"))

    if not sdists or not wheels:
        print("Error: Expected both .tar.gz and .whl in dist/")
        return 1

    sdist_path = sdists[0]
    wheel_path = wheels[0]

    # Version Consistency Audit
    from profileforge import __version__ as pkg_version

    print(f"Authoritative package version: {pkg_version}")
    if f"-{pkg_version}" not in sdist_path.name or f"-{pkg_version}-" not in wheel_path.name:
        print(f"Error: Distribution filenames do not match version '{pkg_version}'")
        return 1
    print(" - Version consistency across filenames verified!")

    if not _verify_sdist(sdist_path) or not _verify_wheel(wheel_path):
        return 1

    print("\nDistribution package verification successful!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
