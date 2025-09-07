"""Stub generation module that notifies users when done."""
from dataclasses import dataclass
from typing import Dict, Optional

from .notifications import send_email, send_web_push


@dataclass
class User:
    id: int
    email: Optional[str] = None
    push_subscription: Optional[dict] = None


users: Dict[int, User] = {}


async def generate(user_id: int) -> str:
    """Pretend to generate some data for a user and notify them."""
    result = "generated data"

    user = users.get(user_id)
    if user:
        if user.email:
            await send_email(user.email, "Generation complete", "Your content is ready.")
        if user.push_subscription:
            send_web_push(user.push_subscription, "Generation complete")

    return result
