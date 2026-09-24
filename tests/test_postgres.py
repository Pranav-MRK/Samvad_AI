from app.db.repository import ConversationRepository


repository = ConversationRepository()

session_id = "student-001"

repository.get_or_create(session_id)

repository.add_message(
    session_id,
    "user",
    "I'm applying for B.Tech.",
)

repository.add_message(
    session_id,
    "assistant",
    "Great. I can help you with the B.Tech admission process.",
)

messages = repository.get_messages(session_id)

print("\n========== CONVERSATION HISTORY ==========\n")

for message in messages:
    print(f"{message['role']}: {message['content']}")