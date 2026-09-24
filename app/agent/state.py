from typing_extensions import TypedDict


class AgentState(TypedDict):
    user_input: str
    intent: str
    context: str
    tool_result: str
    response: str
    confidence: float
    conversation_history: list[dict]
    guardrail_passed: bool
    guardrail_reason: str
    requires_escalation: bool
    

 
    