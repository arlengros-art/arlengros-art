"""Utilities for uploading generated images to cloud storage.

The implementation uses Amazon S3 via :mod:`boto3`.  Uploading is
performed in a thread so that synchronous boto3 operations do not block
the asyncio event loop.
"""
from __future__ import annotations

import asyncio
import os
import uuid
from typing import Optional

import boto3


def _upload_to_s3(image_bytes: bytes, filename: str, bucket: str) -> str:
    """Upload *image_bytes* under *filename* to *bucket* and return the URL."""
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=filename, Body=image_bytes, ContentType="image/png")
    return f"https://{bucket}.s3.amazonaws.com/{filename}"


async def upload_image(image_bytes: bytes, *, filename: Optional[str] = None) -> str:
    """Upload *image_bytes* to S3 and return a public URL.

    Parameters
    ----------
    image_bytes:
        Raw image data to upload.
    filename:
        Optional explicit filename.  If omitted, a UUID based name is used.
    """
    bucket = os.getenv("S3_BUCKET")
    if not bucket:
        raise RuntimeError("S3_BUCKET environment variable is required")

    name = filename or f"{uuid.uuid4().hex}.png"
    # boto3 is synchronous, so delegate to a thread
    return await asyncio.to_thread(_upload_to_s3, image_bytes, name, bucket)
