
from langgraph.graph import StateGraph, START, END

from app.agent.state import AgentState
from app.agent.llm import classify_intent
from app.agent.application import check_application_status

from app.rag.retriever import KnowledgeRetriever
from app.rag.context import format_context
from app.rag.chain import generate_answer
from app.memory.redis import RedisMemory
from app.db.repository import ConversationRepository
from app.agent.checkpointer import checkpointer
from app.agent.guardrails import validate_input
from app.core.logger import (
    log_agent_start,
    log_guardrail,
    log_intent,
    log_rag,
    log_tool,
    log_tool_result,
    log_response,
    log_agent_end,
)

retriever = KnowledgeRetriever()
memory = RedisMemory()
conversation_repo = ConversationRepository()

def process_request(state: AgentState):
    intent = classify_intent(state["user_input"])

    log_intent(intent)

    return {
        "intent": intent,
        "confidence": 0.0,
    }


def route_request(state: AgentState):
    intent = state["intent"]

    if intent in {
        "admission_documents",
        "fee_information",
        "general_query",
    }:
        return "knowledge"

    if intent in {
        "application_status",
        "appointment",
    }:
        return "action"

    if intent == "technical_support":
        return "support"

    return "knowledge"


def knowledge_node(state: AgentState):
    question = state["user_input"]
    
    
    # 1. Retrieve relevant documents
    results = retriever.hybrid_search(question, k=3)

    log_rag(question, len(results))
    # 2. Convert retrieved documents into context
    context = format_context(results)


    # 3. Generate grounded answer using Gemini
    answer = generate_answer(
        question=question,
        context=context,
    )
    log_response(answer)

    log_agent_end()

    return {
        "context": context,
        "response": answer,
    }


def action_node(state: AgentState):
    intent = state["intent"]

    if intent == "application_status":
        application_number = "APP1001"

        log_tool(
            "check_application_status",
            {"application_number": application_number},
        )

        result = check_application_status(application_number)

        log_tool_result(result)

        response = str(result)

        log_response(response)
        log_agent_end()

        return {
            "tool_result": response,
            "response": response,
        }

    response = "This action is not implemented yet."

    log_response(response)
    log_agent_end()

    return {
        "response": response,
    }


def support_node(state: AgentState):
    return {
        "response": "This request will be handled as a support request."
    }

def input_guardrail_node(state: AgentState):
    log_agent_start(state["user_input"])

    result = validate_input(state["user_input"])

    log_guardrail(
        result["guardrail_passed"],
        result["guardrail_reason"],
    )

    return {
        "guardrail_passed": result["guardrail_passed"],
        "guardrail_reason": result["guardrail_reason"],
        "requires_escalation": result["requires_escalation"],
    }

def route_after_guardrail(state: AgentState):
    if not state["guardrail_passed"]:
        return "guardrail_failed"

    return "process_request"


def guardrail_failure_node(state: AgentState):
    return {
        "response": "I’m sorry, but I can’t process that request.",
    }

    

def update_history(state: AgentState):
    history = state.get("conversation_history", []).copy()

    history.append(
        {
            "role": "user",
            "content": state["user_input"],
        }
    )

    if state.get("response"):
        history.append(
            {
                "role": "assistant",
                "content": state["response"],
            }
        )

    return {
        "conversation_history": history,
    }


def build_graph():
    graph = StateGraph(AgentState)  # pyrefly: ignore

    graph.add_node("process_request", process_request)
    graph.add_node("knowledge", knowledge_node)
    graph.add_node("update_history", update_history)
    graph.add_node("input_guardrail", input_guardrail_node)
    graph.add_node("guardrail_failed", guardrail_failure_node)

    graph.add_node("action", action_node)
    graph.add_node("support", support_node)

    graph.add_edge(START, "input_guardrail")

    graph.add_conditional_edges(
        "input_guardrail",
        route_after_guardrail,
        {
            "process_request": "process_request",
            "guardrail_failed": "guardrail_failed",
        },
    )

    graph.add_conditional_edges(
        "process_request",
        route_request,
        {
            "knowledge": "knowledge",
            "action": "action",
            "support": "support",
        },
    )
    graph.add_edge("guardrail_failed", END)

    graph.add_edge("knowledge", "update_history")
    graph.add_edge("action", "update_history")
    graph.add_edge("support", "update_history")
    graph.add_edge("update_history", END)
    

    return graph.compile(checkpointer=checkpointer)


agent = build_graph()



def run_agent(session_id: str, user_input: str):
    # 1. Load active session state from Redis
    previous_state = memory.load(session_id)

    # 2. Log user message to PostgreSQL
    conversation_repo.add_message(
        session_id=session_id,
        role="user",
        content=user_input,
    )

    # 3. Initialize state dictionary
    state = {
        "user_input": user_input,
        "intent": "",
        "context": "",
        "tool_result": "",
        "response": "",
        "confidence": 0.0,
        "conversation_history": [],
    }

    # 4. Restore previous state details if they exist
    if previous_state:
        state["conversation_history"] = previous_state.get(
            "conversation_history",
            [],
        )
        state["context"] = previous_state.get("context", "")
        state["tool_result"] = previous_state.get("tool_result", "")

    # 5. Append current user input to conversation history
    state["conversation_history"].append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # 6. Invoke agent graph once with Postgres checkpointer thread config
    result = agent.invoke(
        state,  # type: ignore
        config={
            "configurable": {
                "thread_id": session_id,
            }
        },
    )

    # 7. Append assistant response to history
    assistant_response = result.get("response", "")
    
    if "conversation_history" not in result:
        result["conversation_history"] = state["conversation_history"]

    result["conversation_history"].append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )

    # 8. Log assistant response to PostgreSQL
    conversation_repo.add_message(
        session_id=session_id,
        role="assistant",
        content=assistant_response,
    )

    # 9. Save current state back to Redis short-term memory
    memory.save(
        session_id,
        {
            "user_input": user_input,
            "intent": result.get("intent", ""),
            "context": result.get("context", ""),
            "tool_result": result.get("tool_result", ""),
            "response": assistant_response,
            "confidence": result.get("confidence", 0.0),
            "conversation_history": result["conversation_history"],
        },
    )

    return result