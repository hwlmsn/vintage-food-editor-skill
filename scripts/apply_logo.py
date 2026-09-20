#!/usr/bin/env python3
"""Place an uploaded raster logo at the top-left of a finished food image."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


def percent(value: str) -> float:
    parsed = float(value)
    if not 0 <= parsed <= 100:
        raise argparse.ArgumentTypeError("must be between 0 and 100")
    return parsed


def ratio(value: str) -> float:
    parsed = float(value)
    if not 0 < parsed <= 1:
        raise argparse.ArgumentTypeError("must be greater than 0 and no more than 1")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Overlay a user-supplied logo at the top-left without redrawing it."
    )
    parser.add_argument("image", type=Path, help="finished food image")
    parser.add_argument("logo", type=Path, help="raster logo, preferably transparent PNG/WebP")
    parser.add_argument("output", type=Path, help="new output image path")
    parser.add_argument(
        "--transparency",
        type=percent,
        default=70.0,
        help="logo transparency percentage; 70 means 30%% opacity (default: 70)",
    )
    parser.add_argument(
        "--width-ratio",
        type=ratio,
        default=0.14,
        help="logo width as a fraction of canvas width (default: 0.14)",
    )
    parser.add_argument(
        "--margin-ratio",
        type=ratio,
        default=0.05,
        help="top and left margin as a fraction of canvas width (default: 0.05)",
    )
    parser.add_argument(
        "--max-height-ratio",
        type=ratio,
        default=0.12,
        help="maximum logo height as a fraction of canvas height (default: 0.12)",
    )
    parser.add_argument("--overwrite", action="store_true", help="allow replacing output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.image.is_file():
        raise SystemExit(f"image not found: {args.image}")
    if not args.logo.is_file():
        raise SystemExit(f"logo not found: {args.logo}")
    if args.output.exists() and not args.overwrite:
        raise SystemExit(f"output already exists: {args.output}")

    with Image.open(args.image) as source:
        base = ImageOps.exif_transpose(source).convert("RGBA")
    with Image.open(args.logo) as source_logo:
        logo = ImageOps.exif_transpose(source_logo).convert("RGBA")

    alpha_bbox = logo.getchannel("A").getbbox()
    if alpha_bbox is None:
        raise SystemExit("logo is fully transparent")
    logo = logo.crop(alpha_bbox)

    target_width = max(1, round(base.width * args.width_ratio))
    scale = target_width / logo.width
    target_height = max(1, round(logo.height * scale))
    max_height = max(1, round(base.height * args.max_height_ratio))
    if target_height > max_height:
        scale = max_height / logo.height
        target_width = max(1, round(logo.width * scale))
        target_height = max_height

    logo = logo.resize((target_width, target_height), Image.Resampling.LANCZOS)
    opacity = 1.0 - args.transparency / 100.0
    logo_alpha = logo.getchannel("A").point(lambda value: round(value * opacity))
    logo.putalpha(logo_alpha)

    margin = max(0, round(base.width * args.margin_ratio))
    x = min(margin, max(0, base.width - logo.width))
    y = min(margin, max(0, base.height - logo.height))
    base.alpha_composite(logo, (x, y))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    suffix = args.output.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        base.convert("RGB").save(args.output, quality=95, subsampling=0)
    else:
        base.save(args.output)


if __name__ == "__main__":
    main()
