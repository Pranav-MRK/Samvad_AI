from app.db.database import Base, engine
from app.db.models import Conversation, Message


def init_db():
    Base.metadata.create_all(bind=engine)
    print(" PostgreSQL tables created")


if __name__ == "__main__":
    init_db()
    