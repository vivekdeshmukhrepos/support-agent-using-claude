"""APScheduler service for scheduling follow-up tasks."""

from datetime import datetime
from typing import Optional, Callable
from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger


class SchedulerService:
    """Service for managing APScheduler background tasks."""

    _instance: Optional["SchedulerService"] = None
    _scheduler: Optional[BackgroundScheduler] = None

    def __init__(self):
        """Initialize the scheduler service."""
        if self._scheduler is None:
            self._scheduler = BackgroundScheduler()

    @classmethod
    def get_instance(cls) -> Optional["SchedulerService"]:
        """Get the singleton instance of SchedulerService."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start(self) -> None:
        """Start the background scheduler."""
        if self._scheduler and not self._scheduler.running:
            self._scheduler.start()
            logger.info("APScheduler started")

    def shutdown(self) -> None:
        """Shutdown the background scheduler."""
        if self._scheduler and self._scheduler.running:
            self._scheduler.shutdown()
            logger.info("APScheduler shutdown")

    def is_running(self) -> bool:
        """Check if the scheduler is running."""
        return self._scheduler is not None and self._scheduler.running

    def schedule_followup(
        self,
        email_id: str,
        job_id: str,
        trigger_at: datetime,
        callback: Optional[Callable] = None,
    ) -> None:
        """
        Schedule a follow-up task for a specific email.

        Args:
            email_id: The email ID to follow up on
            job_id: Unique job ID for tracking
            trigger_at: When to trigger the follow-up
            callback: Optional callback function to execute
        """
        if not self._scheduler:
            logger.error("Scheduler not initialized")
            return

        try:
            # Default callback logs the follow-up
            if callback is None:
                def default_callback():
                    logger.info(f"Follow-up triggered for email {email_id}")

                callback = default_callback

            # Add job to scheduler
            self._scheduler.add_job(
                callback,
                trigger=DateTrigger(run_date=trigger_at),
                id=job_id,
                name=f"followup_{email_id}",
                replace_existing=True,
            )

            logger.debug(f"Scheduled follow-up job {job_id} for {trigger_at}")

        except Exception as e:
            logger.error(f"Failed to schedule follow-up job {job_id}: {e}")

    def get_job(self, job_id: str):
        """Get a scheduled job by ID."""
        if self._scheduler:
            return self._scheduler.get_job(job_id)
        return None

    def remove_job(self, job_id: str) -> None:
        """Remove a scheduled job by ID."""
        if self._scheduler:
            try:
                self._scheduler.remove_job(job_id)
                logger.info(f"Removed job {job_id}")
            except Exception as e:
                logger.error(f"Failed to remove job {job_id}: {e}")

    def list_jobs(self):
        """List all scheduled jobs."""
        if self._scheduler:
            return self._scheduler.get_jobs()
        return []
