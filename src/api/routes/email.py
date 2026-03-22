"""Email processing API routes."""

from fastapi import APIRouter, Depends
from src.api.dependencies import get_settings
from src.core.config import Settings

router = APIRouter()


@router.post("/emails")
async def submit_email(settings: Settings = Depends(get_settings)):
    """
    Submit an email for processing.

    Args:
        settings: Application settings

    Returns:
        Email processing response
    """
    # TODO: Implement email submission endpoint
    return {"message": "Email submission endpoint - not yet implemented"}


@router.get("/emails/{email_id}")
async def get_email_status(email_id: str, settings: Settings = Depends(get_settings)):
    """
    Get the status of a submitted email.

    Args:
        email_id: Email identifier
        settings: Application settings

    Returns:
        Email status information
    """
    # TODO: Implement email status retrieval endpoint
    return {"email_id": email_id, "status": "pending"}
