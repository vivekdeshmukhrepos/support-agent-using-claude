"""Email classification node."""

import json
from typing import Callable
from loguru import logger
from langchain_openai import ChatOpenAI
from src.graph.state import AgentState
from src.core.config import Settings
from src.prompts.templates import get_classification_prompt
from pydantic import BaseModel, Field


class ClassificationOutput(BaseModel):
    """Structured output for email classification."""

    intent: str = Field(..., description="Email intent")
    urgency: str = Field(..., description="Urgency level")
    category: str = Field(..., description="Email category")
    confidence: float = Field(..., description="Confidence score")


def make_classifier(settings: Settings) -> Callable:
    """
    Factory function to create a classifier node.

    Args:
        settings: Application settings with OpenAI config

    Returns:
        Async classifier function
    """

    async def classify_email(state: AgentState) -> dict:
        """
        Classify incoming email by intent, urgency, and category.

        Args:
            state: Current agent state with email content

        Returns:
            Updated state with classification results
        """
        try:
            logger.info(f"Classifying email {state['email_id']}")

            # Initialize LLM
            llm = ChatOpenAI(
                model=settings.openai_model,
                api_key=settings.openai_api_key,
                temperature=0.3,  # Lower temperature for consistent classification
            )

            # Get prompt template
            prompt = get_classification_prompt()

            # Build chain with structured output
            chain = prompt | llm.with_structured_output(ClassificationOutput)

            # Run classification
            result = await chain.ainvoke(
                {"subject": state["subject"], "body": state["body"]}
            )

            logger.info(
                f"Email {state['email_id']} classified as: "
                f"intent={result.intent}, urgency={result.urgency}, "
                f"category={result.category}, confidence={result.confidence}"
            )

            # Determine if human review is needed
            requires_review = (
                result.urgency in ["critical", "high"] or result.confidence < 0.6
            )

            return {
                "intent": result.intent,
                "urgency": result.urgency,
                "category": result.category,
                "confidence": result.confidence,
                "requires_human_review": requires_review,
            }

        except Exception as e:
            logger.error(f"Classification failed for email {state['email_id']}: {e}")
            return {"error": f"Classification error: {str(e)}"}

    return classify_email
