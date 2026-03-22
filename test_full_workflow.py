"""
Test script to demonstrate the full email processing workflow with FAISS.

This script:
1. Loads the knowledge base into FAISS
2. Submits sample emails through the API
3. Shows the classification and retrieved documents
"""

import asyncio
import json
from loguru import logger
from src.core.config import Settings
from src.core.logging import setup_logging
from src.graph.agent_graph import build_agent_graph
from src.graph.state import AgentState
from src.services.email_service import EmailService
from src.services.knowledge_service import KnowledgeService
from src.utils.helpers import generate_email_id, get_timestamp


async def load_knowledge_base():
    """Load FAISS knowledge base with sample documents."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 1: Loading FAISS Knowledge Base")
    logger.info("=" * 80)

    settings = Settings()
    service = KnowledgeService(settings)

    logger.info(f"Loading documents from: {settings.knowledge_base_path}")
    await service.load_knowledge_base()

    stats = service.get_vectorstore_stats()
    logger.info(f"✅ Knowledge Base Loaded: {stats['total_vectors']} vectors indexed")

    return settings


async def test_email_workflow(settings: Settings, email_request: dict):
    """Process a single email through the entire workflow."""
    logger.info("\n" + "=" * 80)
    logger.info(f"Processing Email: {email_request['subject']}")
    logger.info("=" * 80)

    # Generate email ID
    email_id = generate_email_id()
    logger.info(f"Email ID: {email_id}")

    # Store email
    email_service = EmailService(settings)
    await email_service.store_email(
        email_id=email_id,
        sender=email_request["sender"],
        recipient=email_request["recipient"],
        subject=email_request["subject"],
        body=email_request["body"],
    )

    # Build initial state
    initial_state: AgentState = {
        "email_id": email_id,
        "sender": email_request["sender"],
        "recipient": email_request["recipient"],
        "subject": email_request["subject"],
        "body": email_request["body"],
        "received_at": get_timestamp(),
        "intent": "",
        "urgency": "",
        "category": "",
        "confidence": 0.0,
        "retrieved_docs": [],
        "retrieval_query": "",
        "draft_response": "",
        "response_generated_at": None,
        "requires_human_review": False,
        "escalation_reason": None,
        "escalation_ticket_id": None,
        "reply_sent": False,
        "reply_sent_at": None,
        "final_status": "processing",
        "followup_scheduled": False,
        "followup_job_id": None,
        "followup_trigger_at": None,
        "error": None,
    }

    # Build graph
    graph = build_agent_graph(settings)

    logger.info("Running email through LangGraph pipeline...")

    try:
        # Run the graph
        final_state = await graph.ainvoke(initial_state)

        # Display results
        logger.info("\n📊 CLASSIFICATION RESULTS:")
        logger.info(f"  Intent: {final_state.get('intent')}")
        logger.info(f"  Urgency: {final_state.get('urgency')}")
        logger.info(f"  Category: {final_state.get('category')}")
        logger.info(f"  Confidence: {final_state.get('confidence'):.2f}")

        logger.info("\n📚 RETRIEVED DOCUMENTS:")
        retrieved_docs = final_state.get("retrieved_docs", [])
        if retrieved_docs:
            for i, doc in enumerate(retrieved_docs, 1):
                preview = doc[:150].replace("\n", " ")
                logger.info(f"  [{i}] {preview}...")
        else:
            logger.warning("  No documents retrieved")

        logger.info("\n💬 GENERATED RESPONSE:")
        response = final_state.get("draft_response", "")
        if response:
            # Show first 300 chars
            logger.info(f"  {response[:300]}...")
        else:
            logger.warning("  No response generated")

        logger.info("\n✅ FINAL STATUS:")
        logger.info(f"  Status: {final_state.get('final_status')}")
        logger.info(f"  Escalated: {final_state.get('final_status') == 'escalated'}")
        if final_state.get('escalation_ticket_id'):
            logger.info(f"  Escalation Ticket: {final_state.get('escalation_ticket_id')}")

        # Update email with final state
        await email_service.update_email_state(email_id, final_state)

        return final_state

    except Exception as e:
        logger.error(f"❌ Error processing email: {e}")
        return None


async def main():
    """Main test workflow."""
    logger.info("\n")
    logger.info("╔" + "=" * 78 + "╗")
    logger.info("║" + " FAISS Knowledge Base + LangGraph Email Agent Demo ".center(78) + "║")
    logger.info("╚" + "=" * 78 + "╝")

    # Step 1: Load knowledge base
    settings = await load_knowledge_base()

    # Step 2: Test with sample emails
    sample_emails = [
        {
            "sender": "john@customer.com",
            "recipient": "support@company.com",
            "subject": "Unable to reset my password",
            "body": "I tried to reset my password but didn't receive any email. "
            "Can you help me regain access to my account?",
        },
        {
            "sender": "jane@business.com",
            "recipient": "support@company.com",
            "subject": "Question about Pro plan pricing and features",
            "body": "Hi, I'm interested in upgrading to the Pro plan. "
            "What are the exact features included and can I upgrade mid-month?",
        },
        {
            "sender": "error@critical.com",
            "recipient": "support@company.com",
            "subject": "URGENT: Application keeps crashing",
            "body": "The application crashes immediately after login on both Chrome and Firefox. "
            "This is blocking my team's work. Please help ASAP!",
        },
    ]

    logger.info(f"\n\n📧 Testing with {len(sample_emails)} sample emails...\n")

    for email in sample_emails:
        await test_email_workflow(settings, email)
        logger.info("\n")

    logger.info("=" * 80)
    logger.info("✅ All tests completed successfully!")
    logger.info("=" * 80)


if __name__ == "__main__":
    # Initialize logging
    settings = Settings()
    setup_logging(settings.log_level)

    # Run async main
    asyncio.run(main())
