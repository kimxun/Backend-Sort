import os
import redis
from flask_caching import Cache

cache = Cache(
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
        "CACHE_REDIS_PORT": int(os.getenv("REDIS_PORT", 6379)),
        "CACHE_REDIS_DB": int(os.getenv("REDIS_DB", 0)),
        "CACHE_REDIS_PASSWORD": os.getenv("REDIS_PASSWORD") or None,
        "CACHE_DEFAULT_TIMEOUT": 300
    }
)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True
)
