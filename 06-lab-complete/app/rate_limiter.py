import time
import redis
from fastapi import HTTPException
from app.config import settings

# Create a global Redis client pool
r = redis.from_url(settings.redis_url, decode_responses=True)

def check_rate_limit(key: str):
    now = time.time()
    window_key = f"rate_limit:{key}"
    
    # Use Redis transaction (pipeline) for atomic operations
    with r.pipeline() as pipe:
        # Remove elements older than 60 seconds
        pipe.zremrangebyscore(window_key, 0, now - 60)
        # Add the current request timestamp
        pipe.zadd(window_key, {str(now): now})
        # Count requests in the last 60 seconds
        pipe.zcard(window_key)
        # Expire the key after 60 seconds to save memory
        pipe.expire(window_key, 60)
        
        results = pipe.execute()
        request_count = results[2]
        
    if request_count > settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} req/min",
            headers={"Retry-After": "60"},
        )
