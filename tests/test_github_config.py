from src.core.application import app


def test_load_github_config():

    github = app.config.load_github()

    assert github.username == "anujmundu"