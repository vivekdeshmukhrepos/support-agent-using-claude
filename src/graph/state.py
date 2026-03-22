"""AgentState TypedDict for LangGraph state machine."""

from typing import TypedDict, Optional, List
from datetime import datetime


class AgentState(TypedDict):
    """
    Complete state for email support agent pipeline.

    Every field is tracked through the graph and updated by nodes.
    """

    # --- Input ---
    email_id: str
    sender: str
    recipient: str
    subject: str
    body: str
    received_at: datetime

    # --- Classification ---
    intent: str  # question | complaint | refund_request | technical_issue | general
    urgency: str  # low | medium | high | critical
    category: str  # billing | technical | account | shipping | general
    confidence: float  # 0.0 - 1.0

    # --- RAG ---
    retrieved_docs: List[str]  # page_content strings from ChromaDB
    retrieval_query: str

    # --- Response ---
    draft_response: str
    response_generated_at: Optional[datetime]

    # --- Human Review ---
    requires_human_review: bool
    escalation_reason: Optional[str]
    escalation_ticket_id: Optional[str]

    # --- Final Send ---
    reply_sent: bool
    reply_sent_at: Optional[datetime]
    final_status: str  # sent | escalated | failed

    # --- Follow-up ---
    followup_scheduled: bool
    followup_job_id: Optional[str]
    followup_trigger_at: Optional[datetime]

    # --- Error ---
    error: Optional[str]
