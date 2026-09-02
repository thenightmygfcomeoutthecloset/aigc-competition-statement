#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reconstruct_assets.py - Local deterministic fallback for visual asset reconstruction.

Priority 1/2 in the skill architecture use native agent/tool image generation.
This script implements Priority 3 (deterministic local fallback) to guarantee
that when external/native image generation tools are unavailable or running locally,
the required visual asset files are reliably and deterministically generated on disk,
preventing dangling placeholders or missing files in the delivery package.
"""

import os
import sys
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
import argparse
from pathlib import Path
from PIL import Image
import cv2
import numpy as np


def generate_sketch(img_bgr: np.ndarray, output_path: str) -> str:
    """Generate 01_reconstructed_sketch.png using pencil sketch simulation."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    inv_gray = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inv_gray, (21, 21), sigmaX=0, sigmaY=0)
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    sketch = cv2.normalize(sketch, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    # Save with UTF-8 support on Windows
    is_success, buffer = cv2.imencode(".png", sketch)
    if is_success:
        buffer.tofile(output_path)
    return output_path


def generate_lineart(img_bgr: np.ndarray, output_path: str) -> str:
    """Generate 01_reconstructed_lineart.png using clean edge extraction."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    edges = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 3
    )
    is_success, buffer = cv2.imencode(".png", edges)
    if is_success:
        buffer.tofile(output_path)
    return output_path


def generate_color_block(img_bgr: np.ndarray, output_path: str, k: int = 8) -> str:
    """Generate 01_reconstructed_color_block.png using color quantization & smoothing."""
    h, w = img_bgr.shape[:2]
    small = cv2.resize(img_bgr, (max(16, w // 8), max(16, h // 8)), interpolation=cv2.INTER_LINEAR)
    blurred = cv2.medianBlur(small, 7)
    
    data = blurred.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    quantized = centers[labels.flatten()].reshape(blurred.shape).astype(np.uint8)
    
    color_block = cv2.resize(quantized, (w, h), interpolation=cv2.INTER_NEAREST)
    color_block = cv2.GaussianBlur(color_block, (15, 15), 0)
    is_success, buffer = cv2.imencode(".png", color_block)
    if is_success:
        buffer.tofile(output_path)
    return output_path


def generate_generation_v1(img_bgr: np.ndarray, color_block_bgr: np.ndarray, output_path: str) -> str:
    """
    Generate 02_reconstructed_generation_v1.png (intermediate stage 1).
    Simulates early AI generation: overall composition is set, but details are softer,
    lighting is flatter, and subtle diffusion softness exists compared to final.
    """
    soft_orig = cv2.GaussianBlur(img_bgr, (9, 9), 0)
    v1 = cv2.addWeighted(soft_orig, 0.65, color_block_bgr, 0.35, 0)
    v1 = cv2.convertScaleAbs(v1, alpha=0.9, beta=15)
    is_success, buffer = cv2.imencode(".png", v1)
    if is_success:
        buffer.tofile(output_path)
    return output_path


def generate_generation_v2(img_bgr: np.ndarray, v1_bgr: np.ndarray, output_path: str) -> str:
    """
    Generate 03_reconstructed_generation_v2.png (intermediate stage 2).
    Simulates enhanced AI iteration: much closer to final artwork, sharper focus,
    light and shadows refined, approaching final quality.
    """
    v2 = cv2.addWeighted(img_bgr, 0.85, v1_bgr, 0.15, 0)
    is_success, buffer = cv2.imencode(".png", v2)
    if is_success:
        buffer.tofile(output_path)
    return output_path


def reconstruct_all_assets(final_image_path: str, output_dir: str) -> dict:
    """
    Reconstruct all required canonical visual assets from a single final artwork.
    Guarantees that all 5 files exist with filesize > 0.
    """
    final_path = Path(final_image_path).resolve()
    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if not final_path.exists():
        raise FileNotFoundError(f"Final artwork not found at: {final_path}")
    
    img_array = np.fromfile(str(final_path), dtype=np.uint8)
    img_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img_bgr is None:
        pil_img = Image.open(final_path).convert("RGB")
        img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    results = {}
    
    # 1. Sketch
    sketch_path = str(out_dir / "01_reconstructed_sketch.png")
    generate_sketch(img_bgr, sketch_path)
    results["reconstructed_sketch"] = sketch_path
    
    # 2. Lineart
    lineart_path = str(out_dir / "01_reconstructed_lineart.png")
    generate_lineart(img_bgr, lineart_path)
    results["reconstructed_lineart"] = lineart_path
    
    # 3. Color block
    color_block_path = str(out_dir / "01_reconstructed_color_block.png")
    generate_color_block(img_bgr, color_block_path)
    results["reconstructed_color_block"] = color_block_path
    
    # Read color block for intermediate blends
    cb_array = np.fromfile(color_block_path, dtype=np.uint8)
    cb_bgr = cv2.imdecode(cb_array, cv2.IMREAD_COLOR)
    
    # 4. Generation V1
    v1_path = str(out_dir / "02_reconstructed_generation_v1.png")
    generate_generation_v1(img_bgr, cb_bgr, v1_path)
    results["generation_v1"] = v1_path
    
    # Read v1 for v2 blend
    v1_array = np.fromfile(v1_path, dtype=np.uint8)
    v1_bgr = cv2.imdecode(v1_array, cv2.IMREAD_COLOR)
    
    # 5. Generation V2
    v2_path = str(out_dir / "03_reconstructed_generation_v2.png")
    generate_generation_v2(img_bgr, v1_bgr, v2_path)
    results["generation_v2"] = v2_path

    # Verify all files
    for k, p in results.items():
        if not os.path.exists(p):
            raise AssertionError(f"Asset {k} failed to generate: {p}")
        size = os.path.getsize(p)
        if size == 0:
            raise AssertionError(f"Asset {k} is empty (0 bytes): {p}")
        
    return results


def main():
    parser = argparse.ArgumentParser(description="Reconstruct visual assets from final artwork.")
    parser.add_argument("--input", "-i", required=True, help="Path to final artwork image.")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory for assets.")
    args = parser.parse_args()
    
    res = reconstruct_all_assets(args.input, args.output_dir)
    print("Successfully generated visual assets:")
    for k, v in res.items():
        print(f"  [{k}] -> {v} ({os.path.getsize(v)} bytes)")


if __name__ == "__main__":
    main()

