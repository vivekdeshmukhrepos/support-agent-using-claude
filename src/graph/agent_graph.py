"""LangGraph state machine for email support agent."""

from loguru import logger
from langgraph.graph import StateGraph, START, END

from src.graph.state import AgentState
from src.core.config import Settings
from src.nodes.email_reader import make_email_reader
from src.nodes.classifier import make_classifier
from src.nodes.knowledge_retriever import make_retriever
from src.nodes.responder import make_responder
from src.nodes.escalation import make_escalation_handler
from src.nodes.reply_sender import make_reply_sender
from src.nodes.followup_scheduler import make_followup_scheduler


def build_agent_graph(settings: Settings):
    """
    Build the LangGraph state machine for email processing.

    The graph flows through these nodes:
    1. email_reader - Validate email
    2. classify_email - Classify intent, urgency, category
    3. knowledge_retriever - Retrieve relevant docs from knowledge base
    4. generate_response - Generate draft response using RAG
    5. human_review_router - Route to escalation or reply
    6. escalate_email OR reply_sender
    7. followup_scheduler - Schedule follow-ups

    Args:
        settings: Application settings

    Returns:
        Compiled StateGraph ready for execution
    """
    logger.info("Building LangGraph state machine")

    # Create state graph
    graph = StateGraph(AgentState)

    # Create node factories with settings injected
    email_reader = make_email_reader()
    classifier = make_classifier(settings)
    retriever = make_retriever(settings)
    responder = make_responder(settings)
    escalation_handler = make_escalation_handler()
    reply_sender = make_reply_sender(settings)
    followup_scheduler = make_followup_scheduler(settings)

    # Add nodes
    graph.add_node("email_reader", email_reader)
    graph.add_node("classify_email", classifier)
    graph.add_node("knowledge_retriever", retriever)
    graph.add_node("generate_response", responder)
    graph.add_node("escalate_email", escalation_handler)
    graph.add_node("reply_sender", reply_sender)
    graph.add_node("followup_scheduler", followup_scheduler)

    # Add edges
    graph.add_edge(START, "email_reader")
    graph.add_edge("email_reader", "classify_email")
    graph.add_edge("classify_email", "knowledge_retriever")
    graph.add_edge("knowledge_retriever", "generate_response")

    # Conditional edge: route to escalation or reply sender
    graph.add_conditional_edges(
        "generate_response",
        _route_human_review,
        {
            "escalate": "escalate_email",
            "send": "reply_sender",
        },
    )

    # Terminal edges
    graph.add_edge("escalate_email", END)
    graph.add_edge("reply_sender", "followup_scheduler")
    graph.add_edge("followup_scheduler", END)

    logger.info("LangGraph state machine built successfully")

    # Compile the graph
    compiled_graph = graph.compile()

    return compiled_graph


def _route_human_review(state: AgentState) -> str:
    """
    Router function to decide between escalation and automated reply.

    Routes to escalation if:
    - requires_human_review is True (set by classifier)

    Otherwise routes to reply_sender.

    Args:
        state: Current agent state

    Returns:
        "escalate" or "send"
    """
    if state.get("requires_human_review", False):
        logger.info(f"Routing email {state['email_id']} to escalation")
        return "escalate"
    else:
        logger.info(f"Routing email {state['email_id']} to auto-reply")
        return "send"
