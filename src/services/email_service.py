"""Email I/O and processing service."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from loguru import logger
from src.core.config import Settings

# Module-level in-memory storage for emails
_email_store: Dict[str, Dict[str, Any]] = {}


class EmailService:
    """Service for email I/O operations."""

    def __init__(self, settings: Settings):
        """
        Initialize email service with SMTP configuration.

        Args:
            settings: Application settings with SMTP credentials
        """
        self.settings = settings

    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Send an email via SMTP.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            logger.info(f"Sending email to {to} with subject: {subject[:50]}...")

            # Only send if SMTP credentials are configured
            if not self.settings.smtp_username or not self.settings.smtp_password:
                logger.warning(
                    "SMTP credentials not configured, skipping actual send. "
                    "Email would be sent to: {to}"
                )
                return True  # Pretend success for demo

            # Build MIME message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.settings.smtp_username
            msg["To"] = to

            # Attach body
            msg.attach(MIMEText(body, "plain"))

            # Send via SMTP
            with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port) as server:
                server.starttls()
                server.login(self.settings.smtp_username, self.settings.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to}: {e}")
            return False

    async def retrieve_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an email from in-memory storage.

        Args:
            email_id: Email identifier

        Returns:
            Email object or None if not found
        """
        try:
            email = _email_store.get(email_id)
            if email:
                logger.debug(f"Retrieved email {email_id} from storage")
            else:
                logger.warning(f"Email {email_id} not found in storage")
            return email
        except Exception as e:
            logger.error(f"Failed to retrieve email {email_id}: {e}")
            return None

    async def store_email(
        self, email_id: str, sender: str, recipient: str, subject: str, body: str
    ) -> str:
        """
        Store an incoming email in memory.

        Args:
            email_id: Unique email identifier
            sender: Sender email address
            recipient: Recipient email address
            subject: Email subject
            body: Email body

        Returns:
            Email ID for tracking
        """
        try:
            email_data = {
                "email_id": email_id,
                "sender": sender,
                "recipient": recipient,
                "subject": subject,
                "body": body,
                "state": {},  # Will be updated after graph processing
            }
            _email_store[email_id] = email_data
            logger.info(f"Email {email_id} stored in memory")
            return email_id

        except Exception as e:
            logger.error(f"Failed to store email: {e}")
            raise

    async def update_email_state(self, email_id: str, state: Dict[str, Any]) -> None:
        """
        Update the stored email with complete agent state.

        Args:
            email_id: Email identifier
            state: Complete AgentState from graph
        """
        try:
            if email_id in _email_store:
                _email_store[email_id]["state"] = state
                logger.debug(f"Updated state for email {email_id}")
            else:
                logger.warning(f"Email {email_id} not found for state update")
        except Exception as e:
            logger.error(f"Failed to update email state {email_id}: {e}")

    @staticmethod
    def get_all_emails() -> Dict[str, Dict[str, Any]]:
        """Get all stored emails (for debugging/admin purposes)."""
        return _email_store.copy()
