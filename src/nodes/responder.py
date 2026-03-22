"""Response generation node."""

from datetime import datetime
from typing import Callable
from loguru import logger
from langchain_openai import ChatOpenAI
from src.graph.state import AgentState
from src.core.config import Settings
from src.prompts.templates import get_response_prompt
from src.utils.helpers import get_timestamp


def make_responder(settings: Settings) -> Callable:
    """
    Factory function to create a response generator node.

    Args:
        settings: Application settings with OpenAI config

    Returns:
        Async responder function
    """

    async def generate_response(state: AgentState) -> dict:
        """
        Generate a contextual response to the email using RAG.

        Args:
            state: Current agent state with classification and retrieved docs

        Returns:
            Updated state with generated response
        """
        try:
            logger.info(f"Generating response for email {state['email_id']}")

            # Initialize LLM
            llm = ChatOpenAI(
                model=settings.openai_model,
                api_key=settings.openai_api_key,
                temperature=0.7,  # Slightly higher for more natural responses
            )

            # Get prompt template
            prompt = get_response_prompt()

            # Build RAG context from retrieved docs
            context = "\n---\n".join(state["retrieved_docs"]) if state["retrieved_docs"] else "No relevant knowledge base found. Please escalate."

            # Build chain
            chain = prompt | llm

            # Run response generation
            response = await chain.ainvoke(
                {
                    "subject": state["subject"],
                    "body": state["body"],
                    "intent": state["intent"],
                    "category": state["category"],
                    "urgency": state["urgency"],
                    "context": context,
                }
            )

            draft_response = response.content

            logger.info(f"Response generated for email {state['email_id']}")
            logger.debug(f"Draft response length: {len(draft_response)} chars")

            return {
                "draft_response": draft_response,
                "response_generated_at": get_timestamp(),
            }

        except Exception as e:
            logger.error(f"Response generation failed for email {state['email_id']}: {e}")
            return {
                "error": f"Response generation error: {str(e)}",
                "draft_response": "",
            }

    return generate_response
