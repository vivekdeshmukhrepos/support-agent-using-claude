"""LangChain PromptTemplate definitions for email processing."""

from langchain.prompts import PromptTemplate


# TODO: Implement prompt templates for:
# 1. Email Classification Prompt
# 2. Response Generation Prompt
# 3. Escalation Detection Prompt

# Example structure:
# CLASSIFY_EMAIL_PROMPT = PromptTemplate(
#     input_variables=["email_content"],
#     template="""Analyze the following email and classify it.
#     ...
#     """
# )


def get_classification_prompt() -> PromptTemplate:
    """Get email classification prompt template."""
    # TODO: Implement
    raise NotImplementedError("Classification prompt not yet implemented")


def get_response_prompt() -> PromptTemplate:
    """Get response generation prompt template."""
    # TODO: Implement
    raise NotImplementedError("Response prompt not yet implemented")


def get_escalation_prompt() -> PromptTemplate:
    """Get escalation detection prompt template."""
    # TODO: Implement
    raise NotImplementedError("Escalation prompt not yet implemented")
