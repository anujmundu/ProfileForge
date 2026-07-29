from src.core.config_loader import ConfigLoader
from src.core.logger import get_logger


class Application:
    """Application service container."""

    def __init__(self) -> None:
        self.logger = get_logger("github-profile-engine")
        self.config = ConfigLoader()


app = Application()
