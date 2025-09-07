"""Application scheduler setup.

The scheduler runs periodic maintenance tasks.  Currently it includes a
job for clearing stale cache entries in Redis.
"""
from __future__ import annotations

import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis = Redis.from_url(REDIS_URL)

scheduler = AsyncIOScheduler()


async def clear_stale_cache() -> None:
    """Delete cached image references that have no remaining TTL."""
    async for key in redis.scan_iter(match="image:*"):
        ttl = await redis.ttl(key)
        if ttl == -2:  # already expired
            continue
        if ttl == -1:  # no TTL -> remove explicitly
            await redis.delete(key)


def start() -> None:
    """Start the APScheduler instance with the maintenance jobs."""
    scheduler.add_job(clear_stale_cache, "interval", hours=1, id="clear_cache")
    scheduler.start()
