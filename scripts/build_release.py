"""Release Package Builder Script.

Builds source distribution (sdist) and wheel (.whl) for ProfileForge using build module.
Governed by 01_ENGINEERING_QUALITY_GATES.md.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Build sdist and wheel artifacts."""
    root_dir = Path(__file__).parent.parent
    dist_dir = root_dir / "dist"

    print("=== ProfileForge Release Package Builder ===")

    # Clean existing dist directory
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    # Ensure build package is available
    try:
        import build  # noqa: F401
    except ImportError:
        print("Installing 'build' dependency...")
        subprocess.run([sys.executable, "-m", "pip", "install", "build"], check=True)

    print("Building sdist and wheel using python -m build...")
    res = subprocess.run(
        [sys.executable, "-m", "build"],
        cwd=str(root_dir),
        capture_output=True,
        text=True,
    )

    if res.returncode != 0:
        print(f"Build failed with exit code {res.returncode}:")
        print(res.stderr)
        return res.returncode

    print("Build output:")
    print(res.stdout)

    artifacts = list(dist_dir.glob("*"))
    print(f"\nGenerated {len(artifacts)} distribution artifact(s):")
    for artifact in artifacts:
        size_kb = artifact.stat().st_size / 1024.0
        print(f" - {artifact.name} ({size_kb:.1f} KB)")

    print("\nRelease build successful!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
