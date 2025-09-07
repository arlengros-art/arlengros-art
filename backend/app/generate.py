from PIL import Image, ImageFilter


def inpaint(image: Image.Image, mask: Image.Image, prompt: str) -> Image.Image:
    """Simple placeholder inpainting using blur inside the masked area."""
    blurred = image.filter(ImageFilter.GaussianBlur(15))
    return Image.composite(image, blurred, mask)


def outpaint(image: Image.Image, mask: Image.Image, prompt: str) -> Image.Image:
    """Simple placeholder outpainting that fills masked area with white."""
    expanded = Image.new("RGB", image.size, (255, 255, 255))
    expanded.paste(image, (0, 0))
    return Image.composite(expanded, image, mask)
