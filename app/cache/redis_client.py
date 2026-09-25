import redis
import json

from app.core.config import settings


redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True
)


def set_cache(key: str, value, ttl: int = 300):
    redis_client.setex(
        key,
        ttl,
        json.dumps(value)
    )


def get_cache(key: str):
    value = redis_client.get(key)

    if value is None:
        return None

    return json.loads(value)


def delete_cache(key: str):
    redis_client.delete(key)