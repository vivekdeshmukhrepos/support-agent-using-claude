"""
FastAPI application entry point for Customer Support Email Agent.
"""

import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from loguru import logger

from src.core.config import Settings
from src.core.logging import setup_logging
from src.api.routes import email, ui
from src.services.scheduler_service import SchedulerService

# Initialize settings and logging
settings = Settings()
setup_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage app lifecycle - startup and shutdown events.

    Starts and stops APScheduler for follow-up task scheduling.
    """
    # Startup
    logger.info("Starting Customer Support Email Agent")
    scheduler = SchedulerService.get_instance()
    if scheduler:
        scheduler.start()

    yield

    # Shutdown
    logger.info("Shutting down Customer Support Email Agent")
    if scheduler:
        scheduler.shutdown()


# Create FastAPI app with lifespan
app = FastAPI(
    title="Customer Support Email Agent",
    description="LangGraph-based email support agent using LangChain and OpenAI",
    version="0.1.0",
    lifespan=lifespan,
)

# Setup static files and templates
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates_dir = Path("templates")

# Include routers
app.include_router(email.router, prefix="/api", tags=["emails"])
app.include_router(ui.router, tags=["ui"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={"status": "ok"},
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
