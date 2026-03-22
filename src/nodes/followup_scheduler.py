"""Follow-up scheduler node - schedules future follow-up tasks."""

from datetime import datetime, timedelta
from typing import Callable
from loguru import logger
from src.graph.state import AgentState
from src.core.config import Settings
from src.services.scheduler_service import SchedulerService
from src.utils.helpers import generate_email_id, get_timestamp


def make_followup_scheduler(settings: Settings) -> Callable:
    """
    Factory function to create a follow-up scheduler node.

    Args:
        settings: Application settings

    Returns:
        Async scheduler function
    """

    async def schedule_followup(state: AgentState) -> dict:
        """
        Schedule a follow-up task if needed.

        Follow-ups are scheduled for high-urgency or technical issues
        to ensure customer satisfaction.

        Args:
            state: Current agent state

        Returns:
            Updated state with follow-up details
        """
        try:
            # Only schedule follow-ups for sent emails (not escalations)
            if state["final_status"] != "sent":
                logger.debug(
                    f"No follow-up scheduled for email {state['email_id']} "
                    f"(status: {state['final_status']})"
                )
                return {
                    "followup_scheduled": False,
                    "followup_job_id": None,
                    "followup_trigger_at": None,
                }

            # Determine follow-up delay based on urgency
            delay_hours = {
                "critical": 2,
                "high": 24,
                "medium": 48,
                "low": 72,
            }.get(state["urgency"], 48)

            logger.info(
                f"Scheduling follow-up for email {state['email_id']} "
                f"in {delay_hours} hours"
            )

            # Generate follow-up job ID
            job_id = generate_email_id()
            trigger_time = datetime.utcnow() + timedelta(hours=delay_hours)

            # Schedule the follow-up (using APScheduler via SchedulerService)
            scheduler = SchedulerService.get_instance()
            if scheduler and scheduler.is_running():
                scheduler.schedule_followup(
                    email_id=state["email_id"],
                    job_id=job_id,
                    trigger_at=trigger_time,
                )
                logger.info(
                    f"Follow-up job {job_id} scheduled for {trigger_time}"
                )

                return {
                    "followup_scheduled": True,
                    "followup_job_id": job_id,
                    "followup_trigger_at": trigger_time,
                }
            else:
                logger.warning("Scheduler not available for follow-up scheduling")
                return {
                    "followup_scheduled": False,
                    "followup_job_id": None,
                    "followup_trigger_at": None,
                    "error": "Scheduler not available",
                }

        except Exception as e:
            logger.error(
                f"Follow-up scheduling failed for email {state['email_id']}: {e}"
            )
            return {
                "followup_scheduled": False,
                "followup_job_id": None,
                "error": f"Scheduling error: {str(e)}",
            }

    return schedule_followup
