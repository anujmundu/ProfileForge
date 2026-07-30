"""Clean Environment Installation & Execution Verifier.

Tests package installation and basic public API import execution.
Governed by 01_ENGINEERING_QUALITY_GATES.md.
"""

import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    """Verify package installation in a isolated environment."""
    root_dir = Path(__file__).parent.parent
    dist_dir = root_dir / "dist"

    print("=== ProfileForge Installation Verifier ===")

    wheels = list(dist_dir.glob("*.whl"))
    if not wheels:
        print("Error: No wheel file found in dist/. Run build_release.py first.")
        return 1

    wheel_path = wheels[0]

    with tempfile.TemporaryDirectory() as tmp_dir:
        venv_dir = Path(tmp_dir) / "venv"
        print(f"Creating isolated virtual environment in {venv_dir}...")

        res = subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            print("Failed to create venv:", res.stderr)
            return res.returncode

        python_bin = (
            venv_dir / "Scripts" / "python.exe"
            if sys.platform == "win32"
            else venv_dir / "bin" / "python"
        )

        print(f"Installing wheel {wheel_path.name} into isolated venv...")
        res_inst = subprocess.run(
            [str(python_bin), "-m", "pip", "install", str(wheel_path)],
            capture_output=True,
            text=True,
        )
        if res_inst.returncode != 0:
            print("Installation failed:", res_inst.stderr)
            return res_inst.returncode

        print("Testing public API import in isolated environment...")
        verify_code = (
            "import profileforge; "
            "from profileforge.automation import AutomationOrchestrator; "
            "print('Imported ProfileForge version:', profileforge.__version__)"
        )
        res_run = subprocess.run(
            [str(python_bin), "-c", verify_code],
            capture_output=True,
            text=True,
        )

        if res_run.returncode != 0:
            print("Public API verification failed:", res_run.stderr)
            return res_run.returncode

        print(f"Output: {res_run.stdout.strip()}")
        print("\nClean environment installation verification successful!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
