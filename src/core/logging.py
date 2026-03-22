"""Logging configuration using loguru."""

import sys
from loguru import logger


def setup_logging(level: str = "INFO") -> None:
    """
    Configure loguru logging.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Remove default handler
    logger.remove()

    # Add new handler with custom format
    logger.add(
        sys.stdout,
        level=level,
        format=(
            "<level>{time:YYYY-MM-DD HH:mm:ss}</level> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )
