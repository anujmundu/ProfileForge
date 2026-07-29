from github_profile_engine.engine import ProfileEngine


def test_engine_import():
    """Verify the engine can be imported."""
    assert ProfileEngine is not None
