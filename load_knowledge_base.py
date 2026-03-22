"""
Utility script to load and test the FAISS knowledge base.

Run this once to initialize the FAISS index with sample documents.
"""

import asyncio
from loguru import logger
from src.core.config import Settings
from src.core.logging import setup_logging
from src.services.knowledge_service import KnowledgeService


async def main():
    """Load knowledge base and test retrieval."""
    # Initialize settings and logging
    settings = Settings()
    setup_logging(settings.log_level)

    logger.info("=" * 80)
    logger.info("FAISS Knowledge Base Loader")
    logger.info("=" * 80)

    # Create knowledge service
    service = KnowledgeService(settings)

    # Load knowledge base from documents
    logger.info("Loading knowledge base documents...")
    await service.load_knowledge_base()

    # Get stats
    stats = service.get_vectorstore_stats()
    logger.info(f"Knowledge Base Stats: {stats}")

    # Test retrieval with sample queries
    logger.info("\n" + "=" * 80)
    logger.info("Testing Document Retrieval")
    logger.info("=" * 80)

    test_queries = [
        "How do I reset my password?",
        "What payment methods do you accept?",
        "I'm getting a 500 error",
        "Can I export my data?",
        "How much does the Pro plan cost?",
        "What browsers are supported?",
        "How do I enable 2FA?",
    ]

    for query in test_queries:
        logger.info(f"\n🔍 Query: {query}")
        docs = await service.retrieve_relevant_docs(query, top_k=3)

        if docs:
            for i, doc in enumerate(docs, 1):
                # Truncate for display
                preview = doc[:200].replace("\n", " ")
                logger.info(f"   [{i}] {preview}...")
        else:
            logger.warning("   No relevant documents found")

    logger.info("\n" + "=" * 80)
    logger.info("Knowledge base loaded successfully!")
    logger.info(f"Index saved to: {service.faiss_index_path}")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
