"""Backend application package.

Provides image generation, storage utilities, and scheduled maintenance
tasks. The modules are intentionally lightweight and rely on external
services (Redis, S3) which must be configured via environment
variables.
"""
