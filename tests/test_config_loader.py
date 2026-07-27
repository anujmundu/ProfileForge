from src.core.config_loader import ConfigLoader


def test_singleton():

    loader1 = ConfigLoader()

    loader2 = ConfigLoader()

    assert loader1 is loader2