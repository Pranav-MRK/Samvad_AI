import json
import redis


class RedisMemory:
    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True,
        )

    def save(self, session_id: str, state: dict):
        self.client.set(
            f"samvad:session:{session_id}",
            json.dumps(state),
        )

    def load(self, session_id: str):
        data = self.client.get(
            f"samvad:session:{session_id}"
        )

        if not data:
            return None

        return json.loads(data)

    def delete(self, session_id: str):
        self.client.delete(
            f"samvad:session:{session_id}"
        )