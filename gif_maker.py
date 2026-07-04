"""
gif_maker.py — Core GIF creation logic using Pillow.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

from PIL import Image

logger = logging.getLogger(__name__)

# Maximum dimensions for GIF output (keeps file size reasonable)
MAX_WIDTH = 800
MAX_HEIGHT = 800


def _open_and_normalise(path: str, target_size: tuple[int, int] | None) -> Image.Image:
    """
    Open an image, convert to RGBA, optionally resize, then convert to P (palette)
    mode for GIF compatibility while preserving quality.
    """
    img = Image.open(path).convert("RGBA")

    if target_size:
        img = img.resize(target_size, Image.LANCZOS)

    # Convert to palette mode (required for GIF)
    # Use a white background for transparent pixels
    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
    background.paste(img, mask=img.split()[3])  # paste using alpha channel as mask
    return background.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT)


def _compute_target_size(image_paths: Sequence[str]) -> tuple[int, int]:
    """
    Find the most common aspect ratio and pick a sensible output size.
    Uses the first image's aspect ratio and clamps to MAX dimensions.
    """
    with Image.open(image_paths[0]) as first:
        w, h = first.size

    scale = min(MAX_WIDTH / w, MAX_HEIGHT / h, 1.0)  # never upscale
    return (int(w * scale), int(h * scale))


def create_gif_from_images(
    image_paths: Sequence[str],
    output_path: str,
    duration_ms: int = 500,
    loop: int = 0,
) -> str:
    """
    Create an animated GIF from a list of image file paths.

    Args:
        image_paths:  Ordered list of image paths (at least 2).
        output_path:  Where to save the resulting .gif file.
        duration_ms:  Duration per frame in milliseconds.
        loop:         Number of loops (0 = infinite).

    Returns:
        The output path on success.

    Raises:
        ValueError: If fewer than 2 images are provided.
        RuntimeError: If GIF creation fails.
    """
    if len(image_paths) < 2:
        raise ValueError("At least 2 images are required to create a GIF.")

    logger.info(
        "Creating GIF: %d frames, %dms/frame → %s",
        len(image_paths),
        duration_ms,
        output_path,
    )

    target_size = _compute_target_size(image_paths)
    logger.info("Target size: %dx%d", *target_size)

    frames: list[Image.Image] = []
    for i, path in enumerate(image_paths):
        try:
            frame = _open_and_normalise(path, target_size)
            frames.append(frame)
            logger.debug("Loaded frame %d: %s", i + 1, path)
        except Exception as exc:
            logger.warning("Skipping frame %d (%s): %s", i + 1, path, exc)

    if len(frames) < 2:
        raise RuntimeError("Not enough valid frames to build a GIF (minimum 2).")

    try:
        frames[0].save(
            output_path,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=loop,
            optimize=True,
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to save GIF: {exc}") from exc

    size_kb = Path(output_path).stat().st_size / 1024
    logger.info("GIF saved — %.1f KB", size_kb)
    return output_path
