"""Human escalation node."""

from typing import Callable
from loguru import logger
from src.graph.state import AgentState
from src.utils.helpers import generate_email_id


def make_escalation_handler() -> Callable:
    """
    Factory function to create an escalation handler node.

    Returns:
        Async escalation function
    """

    async def escalate_email(state: AgentState) -> dict:
        """
        Escalate email to human support team.

        Args:
            state: Current agent state

        Returns:
            Updated state with escalation details
        """
        try:
            logger.warning(
                f"Escalating email {state['email_id']} for human review. "
                f"Urgency: {state['urgency']}, Confidence: {state['confidence']}"
            )

            # Generate escalation ticket ID
            ticket_id = generate_email_id()

            # Build escalation reason
            escalation_reason = (
                f"Urgent issue (urgency={state['urgency']}) requiring human expertise. "
                f"Category: {state['category']}, Intent: {state['intent']}"
            )

            # In a real system, this would:
            # - Add to escalation queue in database
            # - Send notification to support team (Slack, email, etc.)
            # - Create a support ticket in ticketing system
            # For now, we just log and update state

            logger.info(
                f"Escalation ticket {ticket_id} created for email {state['email_id']}"
            )

            return {
                "escalation_ticket_id": ticket_id,
                "escalation_reason": escalation_reason,
                "final_status": "escalated",
                "reply_sent": False,  # Email not auto-sent for escalations
            }

        except Exception as e:
            logger.error(f"Escalation failed for email {state['email_id']}: {e}")
            return {"error": f"Escalation error: {str(e)}"}

    return escalate_email
