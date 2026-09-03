#!/usr/bin/env python3
"""Measure image-specific differences between a generated version and target artwork."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


def _rgb(path: str | Path, size: tuple[int, int] | None = None) -> np.ndarray:
    with Image.open(path) as image:
        image = image.convert("RGB")
        if size is not None:
            image = image.resize(size, Image.Resampling.LANCZOS)
        return np.asarray(image, dtype=np.float32) / 255.0


def _edge_density(gray: np.ndarray) -> float:
    gx = np.abs(np.diff(gray, axis=1)).mean()
    gy = np.abs(np.diff(gray, axis=0)).mean()
    return float((gx + gy) / 2)


def _regions(array: np.ndarray) -> dict[str, np.ndarray]:
    h, w = array.shape[:2]
    return {
        "左侧": array[:, : w // 2], "右侧": array[:, w // 2 :],
        "上部": array[: h // 2, :], "下部": array[h // 2 :, :],
        "中心": array[h // 4 : 3 * h // 4, w // 4 : 3 * w // 4],
        "边缘": np.concatenate((array[: h // 4].reshape(-1, 3), array[3 * h // 4 :].reshape(-1, 3))),
    }


def analyze_generation_difference(
    generation_path: str | Path,
    final_artwork_path: str | Path,
    artwork_analysis: dict[str, Any],
) -> dict[str, Any]:
    target_image = Image.open(final_artwork_path)
    target_size = target_image.size
    target_image.close()
    generated = _rgb(generation_path, target_size)
    target = _rgb(final_artwork_path, target_size)
    gen_gray = generated.mean(axis=2)
    target_gray = target.mean(axis=2)
    mean_error = float(np.abs(generated - target).mean())
    color_error = float(np.linalg.norm(generated.mean(axis=(0, 1)) - target.mean(axis=(0, 1))))
    lighting_error = float(abs(gen_gray.mean() - target_gray.mean()))
    detail_error = float(abs(_edge_density(gen_gray) - _edge_density(target_gray)))
    region_deltas = {
        name: float(gen.mean() - tgt.mean())
        for (name, gen), tgt in zip(_regions(generated).items(), _regions(target).values())
    }
    worst_region = max(region_deltas, key=lambda key: abs(region_deltas[key]))
    convergence = max(0.0, min(1.0, 1.0 - mean_error))
    subject = str(artwork_analysis.get("subject", "核心主体"))
    palette = str(artwork_analysis.get("palette", "目标色彩"))
    composition = str(artwork_analysis.get("composition", "目标构图"))
    brighter = "偏亮" if lighting_error and gen_gray.mean() > target_gray.mean() else "偏暗"
    region_effect = "视觉重量偏高" if region_deltas[worst_region] > 0 else "视觉重量不足"
    result = {
        "inputs": {
            "generation": str(generation_path),
            "final_artwork": str(final_artwork_path),
            "artwork_analysis_sha256": hashlib.sha256(json.dumps(artwork_analysis, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest(),
        },
        "composition": [f"{worst_region}{region_effect}（区域亮度差 {region_deltas[worst_region]:+.3f}），偏离{composition}。"],
        "subject": [f"{subject}所在核心区域与目标的平均像素差为 {float(np.abs(_regions(generated)['中心'] - _regions(target)['中心']).mean()):.3f}。"],
        "spatial_relationship": [f"左右亮度平衡差为 {abs(region_deltas['左侧'] - region_deltas['右侧']):.3f}，需要按目标重新分配画面重量。"],
        "color": [f"当前全局色彩向量与{palette}目标的距离为 {color_error:.3f}。"],
        "lighting": [f"当前整体亮度相对目标{brighter}，亮度差为 {lighting_error:.3f}。"],
        "style": [f"整体像素关系收敛度为 {convergence:.3f}；保留已建立的主题和风格身份。"],
        "detail": [f"边缘密度差为 {detail_error:.3f}，据此调整局部结构和材质细节。"],
        "priority_adjustments": [
            f"优先校正{worst_region}的画面重量（{region_deltas[worst_region]:+.3f}）。",
            f"将整体色彩距离从 {color_error:.3f} 向目标收敛。",
            f"调整明暗关系，当前亮度差为 {lighting_error:.3f}。",
        ],
        "metrics": {
            "overall_convergence": round(convergence, 6),
            "composition_difference": round(abs(region_deltas["左侧"] - region_deltas["右侧"]), 6),
            "color_difference": round(color_error, 6),
            "lighting_difference": round(lighting_error, 6),
            "structural_difference": round(detail_error, 6),
            "subject_consistency_proxy": round(1.0 - float(np.abs(_regions(generated)["中心"] - _regions(target)["中心"]).mean()), 6),
            "style_similarity_proxy": round(convergence, 6),
        },
    }
    return result


def build_adjustment_reason(difference: dict[str, Any]) -> list[dict[str, str]]:
    categories = ("composition", "color", "lighting", "detail")
    reasons = []
    for category, priority in zip(categories, difference["priority_adjustments"] + [""]):
        observed = difference[category][0]
        reasons.append({
            "observed_issue": observed,
            "visual_effect": f"该差异降低了当前版本与目标作品在{category}维度的一致性。",
            "adjustment": priority or f"针对 {category} 差异进行定向修正。",
            "reason": "保留完整画面的既有方向，同时让下一版本解决实际观测到的主要差异。",
        })
    return reasons


def should_continue_iteration(difference: dict[str, Any], version: int, max_iterations: int, threshold: float = 0.86) -> bool:
    if version >= max_iterations:
        return False
    metrics = difference["metrics"]
    return bool(
        metrics["overall_convergence"] < threshold
        or metrics["composition_difference"] > 0.08
        or metrics["color_difference"] > 0.12
        or metrics["structural_difference"] > 0.04
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generation", required=True)
    parser.add_argument("--final-artwork", required=True)
    parser.add_argument("--artwork-analysis", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    analysis = json.loads(Path(args.artwork_analysis).read_text(encoding="utf-8"))
    result = analyze_generation_difference(args.generation, args.final_artwork, analysis)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
