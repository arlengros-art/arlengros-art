import aiosmtplib
from email.message import EmailMessage
from pywebpush import webpush, WebPushException


async def send_email(to_address: str, subject: str, body: str) -> None:
    """Send an email using aiosmtplib."""
    message = EmailMessage()
    message["From"] = "no-reply@example.com"
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(message, hostname="localhost", port=1025)


def send_web_push(subscription_info: dict, data: str) -> None:
    """Send a web push notification using pywebpush."""
    try:
        webpush(
            subscription_info=subscription_info,
            data=data,
            vapid_private_key="test_private_key",
            vapid_claims={"sub": "mailto:admin@example.com"},
        )
    except WebPushException as exc:  # pragma: no cover - logging stub
        print(f"Web push failed: {exc}")
