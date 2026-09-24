from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

DATABASE_URL = "postgresql://samvad:samvad@localhost:5432/samvad"

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    max_size=10,
    kwargs={"autocommit": True},
)

checkpointer = PostgresSaver(pool)  # pyrefly: ignore

checkpointer.setup()
