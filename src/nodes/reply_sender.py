"""Reply sender node - sends the final response email."""

from typing import Callable
from loguru import logger
from src.graph.state import AgentState
from src.core.config import Settings
from src.services.email_service import EmailService
from src.utils.helpers import get_timestamp


def make_reply_sender(settings: Settings) -> Callable:
    """
    Factory function to create a reply sender node.

    Args:
        settings: Application settings with SMTP config

    Returns:
        Async reply sender function
    """

    async def send_reply(state: AgentState) -> dict:
        """
        Send the final response email to the customer.

        Args:
            state: Current agent state with draft_response

        Returns:
            Updated state with send confirmation
        """
        try:
            logger.info(f"Sending reply for email {state['email_id']}")

            # Create email service
            email_service = EmailService(settings)

            # Build email
            subject = f"Re: {state['subject']}"
            body = state["draft_response"]
            to = state["sender"]

            # Send email via SMTP
            success = await email_service.send_email(
                to=to, subject=subject, body=body
            )

            if success:
                logger.info(f"Reply sent successfully for email {state['email_id']}")
                return {
                    "reply_sent": True,
                    "reply_sent_at": get_timestamp(),
                    "final_status": "sent",
                }
            else:
                logger.warning(f"Failed to send reply for email {state['email_id']}")
                return {
                    "reply_sent": False,
                    "final_status": "failed",
                    "error": "SMTP send failed",
                }

        except Exception as e:
            logger.error(f"Reply sending failed for email {state['email_id']}: {e}")
            return {
                "reply_sent": False,
                "final_status": "failed",
                "error": f"Reply sending error: {str(e)}",
            }

    return send_reply
