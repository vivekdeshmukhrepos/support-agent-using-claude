"""FastAPI dependency injection stubs."""

from src.core.config import Settings


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
