"""Knowledge base retrieval node."""

from typing import Callable
from loguru import logger
from src.graph.state import AgentState
from src.core.config import Settings
from src.services.knowledge_service import KnowledgeService


def make_retriever(settings: Settings) -> Callable:
    """
    Factory function to create a knowledge retriever node.

    Args:
        settings: Application settings

    Returns:
        Async retriever function
    """

    async def retrieve_knowledge(state: AgentState) -> dict:
        """
        Retrieve relevant documents from knowledge base.

        Args:
            state: Current agent state with email content

        Returns:
            Updated state with retrieved documents
        """
        try:
            logger.info(f"Retrieving knowledge base documents for email {state['email_id']}")

            # Create knowledge service
            knowledge_service = KnowledgeService(settings)

            # Build query from subject and body
            query = f"{state['subject']} {state['body']}"
            logger.debug(f"Retrieval query: {query[:100]}...")

            # Retrieve relevant documents
            docs = await knowledge_service.retrieve_relevant_docs(query, top_k=5)

            logger.info(
                f"Retrieved {len(docs)} documents for email {state['email_id']}"
            )

            # Convert docs to page_content strings
            doc_contents = [doc if isinstance(doc, str) else doc.page_content for doc in docs]

            return {
                "retrieved_docs": doc_contents,
                "retrieval_query": query,
            }

        except Exception as e:
            logger.error(
                f"Knowledge retrieval failed for email {state['email_id']}: {e}"
            )
            # Return empty docs but continue pipeline
            return {
                "retrieved_docs": [],
                "retrieval_query": "",
                "error": f"Knowledge retrieval error: {str(e)}",
            }

    return retrieve_knowledge
