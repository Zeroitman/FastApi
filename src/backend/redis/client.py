import redis
from typing import Generator
from backend.config import settings
from backend.redis.key_patterns import KeyPattern


class RedisClient:
    def __init__(self):
        self.client = redis.StrictRedis(connection_pool=settings.REDIS_POOL)

    def get_refresh_token(self, profile_id: str):
        return self.client.get(KeyPattern.refresh_token_key(profile_id))

    def place_refresh_token(self, profile_id: str, ttl: int, token_uuid: str):
        self.client.setex(
            KeyPattern.refresh_token_key(profile_id),
            ttl,
            token_uuid
        )

    def delete_refresh_token(self, profile_id: str):
        self.client.delete(KeyPattern.refresh_token_key(profile_id))


redis_client = RedisClient()


def get_redis() -> Generator:
    yield redis_client
