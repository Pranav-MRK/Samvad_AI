from app.agent.graph import run_agent


session_id = "student-001"

result = run_agent(
    session_id=session_id,
    user_input="Which documents do I need for B.Tech admission?",
)

print("\n========== AGENT RESULT ==========\n")

print("INTENT:")
print(result["intent"])

print("\nANSWER:")
print(result["response"])