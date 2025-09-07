"""Prometheus metrics helpers."""

import time
from contextlib import contextmanager

from prometheus_client import Counter, Histogram, start_http_server


requests_total = Counter(
    "requests_total",
    "Total number of processed requests",
    ["endpoint"],
)


generation_duration = Histogram(
    "generation_duration_seconds",
    "Time spent generating content in seconds",
    ["endpoint"],
)


def start_metrics_server(port: int = 8000) -> None:
    """Start HTTP server for exposing metrics."""
    start_http_server(port)


def track_request(endpoint: str) -> None:
    """Increase request counter for the given endpoint."""
    requests_total.labels(endpoint=endpoint).inc()


@contextmanager
def observe_generation(endpoint: str):
    """Context manager to measure generation duration."""
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        generation_duration.labels(endpoint=endpoint).observe(duration)
