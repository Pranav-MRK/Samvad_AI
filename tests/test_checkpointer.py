from app.agent.graph import agent


config = {
    "configurable": {
        "thread_id": "student-002"
    }
}


result = agent.invoke(
    {
        "user_input": "Which documents do I need for B.Tech admission?",
        "intent": "",
        "context": "",
        "tool_result": "",
        "response": "",
        "confidence": 0.0,
    },
    config=config,
)


print("\n========== RESULT ==========\n")
print(result["response"])