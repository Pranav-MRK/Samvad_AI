from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models import Conversation, Message


class ConversationRepository:

    def get_or_create(self, session_id: str) -> Conversation:
        with SessionLocal() as db:
            conversation = db.scalar(
                select(Conversation).where(
                    Conversation.session_id == session_id
                )
            )

            if conversation:
                return conversation

            conversation = Conversation(
                session_id=session_id
            )

            db.add(conversation)
            db.commit()
            db.refresh(conversation)

            return conversation

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):
        with SessionLocal() as db:
            conversation = db.scalar(
                select(Conversation).where(
                    Conversation.session_id == session_id
                )
            )

            if not conversation:
                conversation = Conversation(
                    session_id=session_id
                )
                db.add(conversation)
                db.flush()

            message = Message(
                conversation_id=conversation.id,
                role=role,
                content=content,
            )

            db.add(message)
            db.commit()

    def get_messages(self, session_id: str):
        with SessionLocal() as db:
            conversation = db.scalar(
                select(Conversation).where(
                    Conversation.session_id == session_id
                )
            )

            if not conversation:
                return []

            messages = db.scalars(
                select(Message)
                .where(
                    Message.conversation_id == conversation.id
                )
                .order_by(Message.created_at)
            ).all()

            return [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ]