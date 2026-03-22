"""Email processing API routes."""

from typing import Optional
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from src.api.dependencies import get_settings
from src.core.config import Settings
from src.graph.agent_graph import build_agent_graph
from src.graph.state import AgentState
from src.services.email_service import EmailService
from src.utils.helpers import generate_email_id, get_timestamp

router = APIRouter()

# Cache compiled graph per settings instance
_graph_cache = {}


class EmailSubmitRequest(BaseModel):
    """Email submission request."""

    sender: EmailStr
    recipient: EmailStr
    subject: str
    body: str


class EmailSubmitResponse(BaseModel):
    """Email submission response."""

    email_id: str
    status: str
    message: str


class EmailStatusResponse(BaseModel):
    """Email status response."""

    email_id: str
    status: str
    intent: Optional[str] = None
    urgency: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    final_status: Optional[str] = None
    escalated: bool = False
    escalation_ticket_id: Optional[str] = None
    draft_response: Optional[str] = None


@router.post("/emails", response_model=EmailSubmitResponse)
async def submit_email(
    request: EmailSubmitRequest,
    settings: Settings = Depends(get_settings),
):
    """
    Submit an email for processing.

    Accepts an email request, processes it through the LangGraph pipeline,
    and returns the result.

    Args:
        request: Email submission request
        settings: Application settings

    Returns:
        Email processing response with email_id and status
    """
    try:
        logger.info(f"Received email from {request.sender}")

        # Generate email ID
        email_id = generate_email_id()

        # Store email in service
        email_service = EmailService(settings)
        await email_service.store_email(
            email_id=email_id,
            sender=request.sender,
            recipient=request.recipient,
            subject=request.subject,
            body=request.body,
        )

        # Build initial state
        initial_state: AgentState = {
            "email_id": email_id,
            "sender": request.sender,
            "recipient": request.recipient,
            "subject": request.subject,
            "body": request.body,
            "received_at": get_timestamp(),
            # Classification (will be filled by graph)
            "intent": "",
            "urgency": "",
            "category": "",
            "confidence": 0.0,
            # RAG
            "retrieved_docs": [],
            "retrieval_query": "",
            # Response
            "draft_response": "",
            "response_generated_at": None,
            # Human review
            "requires_human_review": False,
            "escalation_reason": None,
            "escalation_ticket_id": None,
            # Final
            "reply_sent": False,
            "reply_sent_at": None,
            "final_status": "processing",
            # Follow-up
            "followup_scheduled": False,
            "followup_job_id": None,
            "followup_trigger_at": None,
            # Error
            "error": None,
        }

        # Get or create compiled graph
        # Use a simple string key since Settings objects aren't hashable
        if "default" not in _graph_cache:
            _graph_cache["default"] = build_agent_graph(settings)
        graph = _graph_cache["default"]

        # Run the graph
        logger.info(f"Running graph for email {email_id}")
        final_state = await graph.ainvoke(initial_state)

        # Update email with final state
        await email_service.update_email_state(email_id, final_state)

        logger.info(f"Email {email_id} processed. Final status: {final_state.get('final_status')}")

        return EmailSubmitResponse(
            email_id=email_id,
            status=final_state.get("final_status", "completed"),
            message=f"Email processed successfully. "
            f"Status: {final_state.get('final_status')}",
        )

    except Exception as e:
        logger.error(f"Failed to submit email: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/emails/{email_id}", response_model=EmailStatusResponse)
async def get_email_status(
    email_id: str,
    settings: Settings = Depends(get_settings),
):
    """
    Get the status and details of a submitted email.

    Args:
        email_id: Email identifier
        settings: Application settings

    Returns:
        Email status with processing results
    """
    try:
        logger.debug(f"Retrieving status for email {email_id}")

        # Retrieve email from service
        email_service = EmailService(settings)
        email_record = await email_service.retrieve_email(email_id)

        if not email_record:
            raise HTTPException(status_code=404, detail=f"Email {email_id} not found")

        # Extract state from email record
        state = email_record.get("state", {})

        # Build response
        return EmailStatusResponse(
            email_id=email_id,
            status=state.get("final_status", "unknown"),
            intent=state.get("intent"),
            urgency=state.get("urgency"),
            category=state.get("category"),
            confidence=state.get("confidence"),
            final_status=state.get("final_status"),
            escalated=state.get("final_status") == "escalated",
            escalation_ticket_id=state.get("escalation_ticket_id"),
            draft_response=state.get("draft_response"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve email status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
