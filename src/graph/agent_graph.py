"""LangGraph state machine for email support agent."""

from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# TODO: Define AgentState TypedDict with email, classification, response, escalation fields
# TODO: Implement email classifier node
# TODO: Implement response generator node
# TODO: Implement escalation node
# TODO: Build graph with routing logic


def build_agent_graph() -> StateGraph:
    """
    Build the LangGraph state machine for email processing.

    Returns:
        Compiled StateGraph
    """
    # TODO: Implement graph construction
    # Example structure:
    # - START -> classifier node
    # - classifier node -> router (response/escalation)
    # - response node -> END
    # - escalation node -> END

    raise NotImplementedError("Agent graph construction not yet implemented")
