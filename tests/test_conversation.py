from app.agent.graph import agent


config = {
    "configurable": {
        "thread_id": "student-006"
    }
}


# TURN 1

result = agent.invoke(
    {
        "user_input": "Can you check my application status?",
        "intent": "",
        "context": "",
        "tool_result": "",
        "response": "",
        "confidence": 0.0,
    },
    config=config,
)

print("\n========== TURN 1 ==========")
print(result["response"])


print("\n========== HISTORY ==========")

for message in result["conversation_history"]:
    print(f"{message['role']}: {message['content']}")