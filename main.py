"""
FastAPI application entry point for Customer Support Email Agent.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.core.config import Settings
from src.core.logging import setup_logging
from src.api.routes import email

# Initialize settings and logging
settings = Settings()
setup_logging(settings.log_level)

# Create FastAPI app
app = FastAPI(
    title="Customer Support Email Agent",
    description="LangGraph-based email support agent using LangChain and OpenAI",
    version="0.1.0",
)

# Include routers
app.include_router(email.router, prefix="/api", tags=["emails"])


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
