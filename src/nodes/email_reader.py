"""Email reader node - parses incoming email requests into state."""

from typing import Callable
from loguru import logger
from src.graph.state import AgentState
from src.utils.helpers import get_timestamp


def make_email_reader() -> Callable:
    """
    Factory function to create an email reader node.

    Returns:
        Async email reader function
    """

    async def read_email(state: AgentState) -> dict:
        """
        Parse and validate incoming email.

        In this simple implementation, the email is already parsed from the API request.
        This node validates the email content and sets initial state fields.

        Args:
            state: Current agent state with email_id, sender, recipient, subject, body

        Returns:
            Updated state with validation results and timestamp
        """
        try:
            logger.info(f"Reading email {state['email_id']} from {state['sender']}")

            # Validate required fields
            required_fields = ["email_id", "sender", "recipient", "subject", "body"]
            for field in required_fields:
                if not state.get(field):
                    raise ValueError(f"Missing required field: {field}")

            # Validate email addresses (basic)
            if "@" not in state["sender"] or "@" not in state["recipient"]:
                raise ValueError("Invalid email addresses")

            # Set timestamp
            logger.debug(
                f"Email {state['email_id']}: "
                f"subject='{state['subject'][:50]}...', "
                f"body_length={len(state['body'])} chars"
            )

            return {"received_at": get_timestamp()}

        except Exception as e:
            logger.error(f"Email reading failed for {state['email_id']}: {e}")
            return {"error": f"Email reading error: {str(e)}"}

    return read_email
