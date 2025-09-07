"""Image generation service with Redis caching.

Before generating an image the cache is consulted for an entry with the
same ``prompt`` and ``seed``.  Generation itself is considered CPU
intensive and therefore executed in a worker thread so as not to block
the asyncio event loop.

The resulting image is uploaded to cloud storage via
:mod:`backend.app.storage` and only the resulting URL is persisted.
"""
from __future__ import annotations

import asyncio
import os
from typing import Optional

from redis.asyncio import Redis

from .storage import upload_image

# ---------------------------------------------------------------------------
# Redis configuration

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL = int(os.getenv("CACHE_TTL", 60 * 60 * 24))  # default: 24 hours
redis = Redis.from_url(REDIS_URL)


# ---------------------------------------------------------------------------
# Generation helpers

def _cpu_intensive_generation(prompt: str, seed: int) -> bytes:
    """Placeholder for the real, CPU heavy image generation process."""
    # In a real application this would invoke a ML model.  Here we simply
    # derive deterministic bytes from the prompt/seed pair.
    import hashlib

    h = hashlib.sha256()
    h.update(f"{prompt}:{seed}".encode("utf-8"))
    return h.digest()


async def save_image_record(prompt: str, seed: int, url: str) -> None:
    """Persist the generated image reference in the database.

    The actual database layer is application specific and therefore
    represented here as a stub.
    """
    # Placeholder for DB interaction
    return None


async def generate_image(prompt: str, *, seed: int, ttl: Optional[int] = None) -> str:
    """Generate an image for *prompt* and return its storage URL.

    If the ``prompt``/``seed`` combination was previously generated the
    cached URL is returned.  Otherwise a new image is created, uploaded to
    storage and both the database and cache are updated.
    """
    cache_key = f"image:{prompt}:{seed}"
    cached_url = await redis.get(cache_key)
    if cached_url:
        return cached_url.decode("utf-8")

    # Offload CPU intensive generation to a thread
    image_bytes = await asyncio.to_thread(_cpu_intensive_generation, prompt, seed)

    # Upload to cloud storage
    url = await upload_image(image_bytes)

    # Persist only the URL in the database
    await save_image_record(prompt, seed, url)

    # Cache the URL for subsequent requests
    await redis.set(cache_key, url, ex=ttl or CACHE_TTL)
    return url
