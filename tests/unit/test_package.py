"""Foundation tests for profileforge package metadata and structure."""

import profileforge


def test_package_import() -> None:
    """Verify profileforge package imports and exposes valid version metadata."""
    assert profileforge.__version__ == "1.0.0"
