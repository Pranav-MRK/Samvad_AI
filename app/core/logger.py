def log_agent_start(user_input: str):
    print("\n" + "=" * 60)
    print("🤖 SamvadAI Agent Started")
    print("=" * 60)
    print(f"👤 User: {user_input}")


def log_guardrail(passed: bool, reason: str):
    status = "PASSED" if passed else "BLOCKED"
    print(f"\n🛡️ Guardrail: {status}")
    print(f"   └─ {reason}")


def log_intent(intent: str):
    print("\n🧠 Intent")
    print(f"   └─ {intent}")


def log_rag(query: str, result_count: int):
    print("\n📚 RAG")
    print(f"   └─ Query: {query}")
    print(f"   └─ Retrieved documents: {result_count}")


def log_tool(tool_name: str, arguments: dict):
    print("\n🔧 Tool")
    print(f"   └─ {tool_name}")
    print(f"   └─ Arguments: {arguments}")


def log_tool_result(result):
    print("\n📦 Tool Result")
    print(f"   └─ {result}")


def log_response(response: str):
    print("\n💬 Agent Response")
    print(f"   └─ {response}")


def log_agent_end():
    print("\n" + "=" * 60)
    print("✅ SamvadAI Agent Completed")
    print("=" * 60 + "\n")