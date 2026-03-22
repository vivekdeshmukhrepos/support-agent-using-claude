"""UI routes for web interface."""

from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from loguru import logger

from src.services.email_service import EmailService
from src.core.config import Settings
from src.api.dependencies import get_settings

router = APIRouter()

# Setup templates directory
templates_dir = Path("templates")
if templates_dir.exists():
    templates = Jinja2Templates(directory=str(templates_dir))
else:
    templates = None


@router.get("/", response_class=HTMLResponse)
async def test_page(request: Request):
    """Render the test email page."""
    if not templates:
        return "<h1>Templates directory not found</h1>"

    try:
        return templates.TemplateResponse("test.html", {"request": request})
    except Exception as e:
        logger.error(f"Failed to render test page: {e}")
        return f"<h1>Error loading page: {e}</h1>"


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Render the dashboard page."""
    if not templates:
        return "<h1>Templates directory not found</h1>"

    try:
        return templates.TemplateResponse("dashboard.html", {"request": request})
    except Exception as e:
        logger.error(f"Failed to render dashboard page: {e}")
        return f"<h1>Error loading page: {e}</h1>"


@router.get("/api-docs", response_class=HTMLResponse)
async def api_docs_page(request: Request):
    """Render the API documentation page."""
    if not templates:
        return "<h1>Templates directory not found</h1>"

    try:
        return templates.TemplateResponse("api_docs.html", {"request": request})
    except Exception as e:
        logger.error(f"Failed to render API docs page: {e}")
        return f"<h1>Error loading page: {e}</h1>"


@router.get("/api/emails-list")
async def get_emails_list(settings: Settings = None):
    """
    Get list of all processed emails with statistics.

    Returns:
        List of emails with their details and statistics
    """
    if settings is None:
        settings = Settings()

    try:
        email_service = EmailService(settings)
        all_emails = email_service.get_all_emails()

        logger.debug(f"Fetching {len(all_emails)} emails for dashboard")

        # Prepare email list for display
        emails = []
        total_emails = 0
        sent_count = 0
        escalated_count = 0
        total_confidence = 0.0
        confidence_count = 0

        for email_id, email_data in all_emails.items():
            total_emails += 1
            state = email_data.get("state", {})

            # Count statistics
            final_status = state.get("final_status", "processing")
            if final_status == "sent":
                sent_count += 1
            elif final_status == "escalated":
                escalated_count += 1

            # Accumulate confidence for average
            confidence = state.get("confidence", 0.0)
            if confidence > 0:
                total_confidence += confidence
                confidence_count += 1

            emails.append({
                "email_id": email_id,
                "sender": email_data.get("sender", "Unknown"),
                "recipient": email_data.get("recipient", "Unknown"),
                "subject": email_data.get("subject", "No subject"),
                "state": state,
            })

        # Calculate average confidence
        avg_confidence = (
            total_confidence / confidence_count if confidence_count > 0 else 0.0
        )

        # Sort emails by most recent first (reverse insertion order)
        emails.reverse()

        return {
            "emails": emails,
            "stats": {
                "total": total_emails,
                "sent": sent_count,
                "escalated": escalated_count,
                "avg_confidence": avg_confidence,
            },
        }

    except Exception as e:
        logger.error(f"Failed to get emails list: {e}")
        return {
            "emails": [],
            "stats": {
                "total": 0,
                "sent": 0,
                "escalated": 0,
                "avg_confidence": 0.0,
            },
            "error": str(e),
        }
