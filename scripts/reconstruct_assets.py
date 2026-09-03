#!/usr/bin/env python3
"""Reconstruct only pre-generation visual inputs from a final artwork."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

from canonical_schema import filename_for

MAX_INPUT_PIXELS = 50_000_000
MAX_PROCESSING_EDGE = 4096

for stream in (sys.stdout, sys.stderr):
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


def _decode_rgb(path: Path) -> np.ndarray:
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"Input image is missing or empty: {path}")
    try:
        with Image.open(path) as source:
            source.verify()
        with Image.open(path) as source:
            width, height = source.size
            if width * height > MAX_INPUT_PIXELS:
                raise ValueError(f"Input image exceeds {MAX_INPUT_PIXELS} pixels: {width}x{height}")
            source.thumbnail((MAX_PROCESSING_EDGE, MAX_PROCESSING_EDGE), Image.Resampling.LANCZOS)
            rgb = source.convert("RGB")
            return cv2.cvtColor(np.asarray(rgb), cv2.COLOR_RGB2BGR)
    except (OSError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        raise ValueError(f"Input image cannot be decoded: {path}") from exc


def _write_png(image: np.ndarray, output_path: Path) -> Path:
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError(f"Could not encode PNG: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    buffer.tofile(str(output_path))
    with Image.open(output_path) as check:
        check.verify()
    return output_path


def generate_sketch(image: np.ndarray, output_path: Path) -> Path:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(cv2.bitwise_not(gray), (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    return _write_png(cv2.normalize(sketch, None, 0, 255, cv2.NORM_MINMAX), output_path)


def generate_lineart(image: np.ndarray, output_path: Path) -> Path:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    lineart = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 3)
    return _write_png(lineart, output_path)


def generate_color_block(image: np.ndarray, output_path: Path, colors: int = 8) -> Path:
    height, width = image.shape[:2]
    small = cv2.resize(image, (max(16, width // 8), max(16, height // 8)), interpolation=cv2.INTER_AREA)
    if min(small.shape[:2]) >= 7:
        small = cv2.medianBlur(small, 7)
    data = small.reshape((-1, 3)).astype(np.float32)
    cv2.setRNGSeed(20260903)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5)
    _, labels, centers = cv2.kmeans(data, colors, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
    quantized = centers[labels.ravel()].reshape(small.shape).astype(np.uint8)
    result = cv2.resize(quantized, (width, height), interpolation=cv2.INTER_NEAREST)
    return _write_png(cv2.GaussianBlur(result, (15, 15), 0), output_path)


def reconstruct_all_assets(final_image_path: str, output_dir: str) -> dict[str, str]:
    source = Path(final_image_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    image = _decode_rgb(source)
    paths = {
        asset_id: output / filename_for(asset_id)
        for asset_id in ("reconstructed_sketch", "reconstructed_lineart", "reconstructed_color_block")
    }
    generate_sketch(image, paths["reconstructed_sketch"])
    generate_lineart(image, paths["reconstructed_lineart"])
    generate_color_block(image, paths["reconstructed_color_block"])
    for asset_id, path in paths.items():
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Pre-generation reconstruction failed: {asset_id}: {path}")
    return {asset_id: str(path) for asset_id, path in paths.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconstruct sketch, lineart, and color-block inputs")
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output-dir", "-o", required=True)
    args = parser.parse_args()
    assets = reconstruct_all_assets(args.input, args.output_dir)
    for asset_id, path in assets.items():
        print(f"{asset_id}: {path} ({os.path.getsize(path)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
