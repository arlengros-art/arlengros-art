#!/usr/bin/env python3
"""Generate simple social media banners with custom text."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def create_banner(text: str, output: Path, width: int = 1200, height: int = 630) -> None:
    """Create a banner image with centered text."""
    image = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 48)
    except OSError:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, font=font, fill=(255, 255, 255))

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a social banner")
    parser.add_argument("text", help="Text to place on the banner")
    parser.add_argument("output", type=Path, help="Output image path")
    args = parser.parse_args()

    create_banner(args.text, args.output)


if __name__ == "__main__":
    main()
