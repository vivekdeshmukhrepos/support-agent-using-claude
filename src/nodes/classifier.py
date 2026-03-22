"""Email classification node."""


async def classify_email(state):
    """
    Classify incoming email by intent and urgency.

    Args:
        state: Current agent state with email content

    Returns:
        Updated state with classification results
    """
    # TODO: Implement email classification using LangChain + OpenAI
    # - Extract intent (question, complaint, request, etc.)
    # - Determine urgency (low, medium, high, critical)
    # - Categorize topic (billing, technical, general, etc.)

    raise NotImplementedError("Email classification not yet implemented")
