"""Application logging utilities with structlog."""

import logging
from typing import Optional

import structlog


def configure_logging(level: int = logging.INFO) -> None:
    """Configure structlog for structured JSON logging."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(level),
        cache_logger_on_first_use=True,
    )


configure_logging()


def bind_context(*, user_id: Optional[str] = None, job_id: Optional[str] = None) -> None:
    """Bind user and job identifiers to the log context."""
    structlog.contextvars.clear_contextvars()
    if user_id:
        structlog.contextvars.bind_contextvars(user_id=user_id)
    if job_id:
        structlog.contextvars.bind_contextvars(job_id=job_id)


def get_logger() -> structlog.stdlib.BoundLogger:
    """Return a structlog logger instance."""
    return structlog.get_logger()
