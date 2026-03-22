"""LangChain PromptTemplate definitions for email processing."""

from langchain_core.prompts import ChatPromptTemplate


def get_classification_prompt() -> ChatPromptTemplate:
    """
    Get email classification prompt template.

    Classifies emails into intent, urgency, category, and confidence.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert customer support email classifier.
Your task is to analyze customer emails and classify them accurately.

Classify the email based on:
1. **Intent**: What the customer wants (question, complaint, refund_request, technical_issue, general)
2. **Urgency**: How urgent the issue is (low, medium, high, critical)
3. **Category**: The topic area (billing, technical, account, shipping, general)
4. **Confidence**: Your confidence in the classification (0.0-1.0)

Respond ONLY with valid JSON matching this schema:
{{
    "intent": "string",
    "urgency": "string",
    "category": "string",
    "confidence": number
}}""",
            ),
            (
                "human",
                """Classify this customer email:

Subject: {subject}
Body: {body}

Respond ONLY with the JSON classification. No other text.""",
            ),
        ]
    )


def get_response_prompt() -> ChatPromptTemplate:
    """
    Get response generation prompt template.

    Generates a helpful customer support response using RAG context.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a professional and empathetic customer support agent.

Your task is to write a helpful response to the customer's email using the provided knowledge base context.

Guidelines:
- Be professional and empathetic
- Address the customer's concern directly
- Use the provided knowledge base context to give accurate information
- If the knowledge base doesn't have relevant information, offer to escalate or provide a sincere apology
- Keep the response concise but complete
- End with a clear next step or offer of further assistance""",
            ),
            (
                "human",
                """Customer Email:
Subject: {subject}
Body: {body}

Email Classification:
- Intent: {intent}
- Category: {category}
- Urgency: {urgency}

Knowledge Base Context:
{context}

Please write a professional response to this customer. Make sure to:
1. Acknowledge their concern
2. Provide helpful information using the knowledge base
3. Suggest a resolution or next steps
4. Offer further assistance if needed

Response:""",
            ),
        ]
    )


def get_escalation_reason_prompt() -> ChatPromptTemplate:
    """
    Get escalation reason prompt template.

    Generates a concise reason why an email needs human review.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert at identifying why customer emails need human review. Provide a brief, one-sentence reason.",
            ),
            (
                "human",
                """Email Details:
Subject: {subject}
Body: {body}
Urgency: {urgency}
Intent: {intent}
Confidence: {confidence}

Why does this email need human review? (One sentence only)""",
            ),
        ]
    )
