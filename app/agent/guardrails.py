SUPPORTED_INTENTS = {
    "admission_documents",
    "application_status",
    "fee_information",
    "technical_support",
    "appointment",
    "general_query",
}


def validate_input(user_input: str) -> dict:
    """
    Validate whether the user's request can be processed
    by the SamvadAI college admission assistant.
    """

    if not user_input or not user_input.strip():
        return {
            "guardrail_passed": False,
            "guardrail_reason": "User input is empty.",
            "requires_escalation": False,
        }

    if len(user_input) > 2000:
        return {
            "guardrail_passed": False,
            "guardrail_reason": "User input exceeds the allowed length.",
            "requires_escalation": False,
        }

    return {
        "guardrail_passed": True,
        "guardrail_reason": "Input passed basic validation.",
        "requires_escalation": False,
    }