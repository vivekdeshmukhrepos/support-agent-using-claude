"""Helper utility functions."""

import uuid
from datetime import datetime


def generate_email_id() -> str:
    """
    Generate a unique email ID.

    Returns:
        Unique email identifier
    """
    return f"email_{uuid.uuid4().hex[:8]}"


def get_timestamp() -> datetime:
    """
    Get current UTC timestamp.

    Returns:
        Current datetime in UTC
    """
    return datetime.utcnow()


# TODO: Add additional helper functions as needed:
# - Email parsing/validation
# - Text preprocessing
# - Token counting
# - Error handling utilities
