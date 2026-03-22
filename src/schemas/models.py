"""Pydantic models for data validation."""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class EmailRequest(BaseModel):
    """Schema for incoming email submission."""

    sender: EmailStr = Field(..., description="Sender email address")
    recipient: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "sender": "user@example.com",
                "recipient": "support@company.com",
                "subject": "Issue with my account",
                "body": "I'm unable to login to my account.",
            }
        }


class EmailResponse(BaseModel):
    """Schema for email processing response."""

    email_id: str = Field(..., description="Unique email identifier")
    status: str = Field(..., description="Processing status")
    classification: Optional[str] = Field(None, description="Email classification")
    response: Optional[str] = Field(None, description="Generated response")
    escalated: bool = Field(False, description="Whether email was escalated")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "email_id": "email_123",
                "status": "pending",
                "classification": "technical_support",
                "response": None,
                "escalated": False,
            }
        }


class EmailStatus(BaseModel):
    """Schema for email status retrieval."""

    email_id: str = Field(..., description="Unique email identifier")
    status: str = Field(..., description="Current processing status")
    created_at: datetime = Field(..., description="Email creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    result: Optional[dict] = Field(None, description="Processing result")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "email_id": "email_123",
                "status": "completed",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:05:00Z",
                "result": {
                    "classification": "technical_support",
                    "escalated": False,
                },
            }
        }


class EmailClassification(BaseModel):
    """Schema for email classification results."""

    intent: str = Field(..., description="Email intent (question, complaint, request, etc.)")
    urgency: str = Field(..., description="Urgency level (low, medium, high, critical)")
    category: str = Field(..., description="Topic category (billing, technical, general, etc.)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence score")
