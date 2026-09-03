#!/usr/bin/env python3
"""Run a real, dynamically sized complete-artwork generation pipeline."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

from analyze_generation_difference import analyze_generation_difference, build_adjustment_reason, should_continue_iteration
from build_docx import build_docx_from_manifest
from canonical_schema import asset_specs, filename_for, generation_policy, required_file_asset_ids, versioned_asset
from image_generation_backend import GenerationBackendUnavailable, ImageGenerationBackend, generate_image, resolve_backend
from manifest_schema import sha256_file, validate_manifest_file
from reconstruct_assets import MAX_INPUT_PIXELS, reconstruct_all_assets
from render_docx import audit_rendered_pages, find_soffice, render_docx

for stream in (sys.stdout, sys.stderr):
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


def _required_text(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"analysis-json requires a non-empty {key!r} string")
    return value.strip()


def _safe_filename_part(value: str) -> str:
    return (re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value).strip(" .")[:80] or "未命名")


def _normalise_final(source: Path, target: Path) -> None:
    if not source.is_file() or source.stat().st_size == 0:
        raise ValueError(f"Input image is missing or empty: {source}")
    try:
        with Image.open(source) as image:
            if image.width * image.height > MAX_INPUT_PIXELS:
                raise ValueError(f"Input image exceeds {MAX_INPUT_PIXELS} pixels")
            image.load()
            image.convert("RGB").save(target, format="PNG", optimize=True)
    except (OSError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        raise ValueError(f"Input image cannot be decoded: {source}") from exc


def _original_tool(confirmations: dict[str, Any]) -> str | None:
    raw = confirmations.get("original_tool")
    if isinstance(raw, dict) and raw.get("confirmed") is True:
        value = str(raw.get("value", "")).strip()
        if value:
            return value
    return None


def _asset_record(asset_id: str, relative_path: str, output: Path, allow_missing: bool = False) -> dict[str, Any]:
    path = output / relative_path
    record: dict[str, Any] = {"id": asset_id, "path": relative_path, "sha256": None, "size_bytes": None}
    if path.is_file():
        record.update({"sha256": sha256_file(path), "size_bytes": path.stat().st_size})
    elif not allow_missing:
        raise ValueError(f"Required pipeline asset missing: {asset_id}: {path}")
    return record


def _build_prompt_v1(analysis: dict[str, Any]) -> tuple[str, dict[str, list[str]]]:
    fields = {
        "subject": _required_text(analysis, "subject"),
        "composition": _required_text(analysis, "composition"),
        "perspective": str(analysis.get("perspective", "符合主题的自然透视关系")).strip(),
        "environment": str(analysis.get("environment", "与主体形成完整叙事的场景环境")).strip(),
        "foreground": str(analysis.get("foreground", "具有引导作用的前景关系")).strip(),
        "middle_ground": str(analysis.get("middle_ground", "承载主体的中景层次")).strip(),
        "background": str(analysis.get("background_visual", "支撑空间深度的背景信息")).strip(),
        "palette": _required_text(analysis, "palette"),
        "lighting": str(analysis.get("lighting", "围绕视觉焦点组织主光与环境光")).strip(),
        "atmosphere": str(analysis.get("atmosphere", "与主题一致的整体氛围")).strip(),
        "visual_style": str(analysis.get("visual_style", "统一且完整的数字视觉风格")).strip(),
        "material": str(analysis.get("material", "可辨识的主体与环境材质")).strip(),
        "detail": str(analysis.get("detail", "中等细节，保留后续深化空间")).strip(),
    }
    prompt = "；".join(f"{key}: {value}" for key, value in fields.items()) + "；输出同一幅作品的完整画面，主体、背景、构图、色彩和空间关系均须成立。"
    evolution = {"keep": [], "modify": [], "add": list(fields.values()), "reduce": [], "reason": ["建立同一作品的首个完整视觉方向。"]}
    return prompt, evolution


def _evolve_prompt(previous_prompt: str, difference: dict[str, Any], reasons: list[dict[str, str]], analysis: dict[str, Any]) -> tuple[str, dict[str, list[str]]]:
    keep = [str(analysis.get("subject")), str(analysis.get("composition")), str(analysis.get("palette")), str(analysis.get("visual_style", "既有视觉风格"))]
    modify = [item["adjustment"] for item in reasons[:3]]
    add = [difference["detail"][0]]
    reduce = [item for item in difference["priority_adjustments"] if "偏高" in item or "亮" in item]
    reason = [item["reason"] for item in reasons[:3]]
    directives = "；".join([*(f"保留：{item}" for item in keep), *(f"修改：{item}" for item in modify), *(f"增加：{item}" for item in add), *(f"减少：{item}" for item in reduce)])
    prompt = f"{previous_prompt}；基于上一完整版本的实测诊断进行版本深化：{directives}；继续输出同一幅完整作品，不拆分主体或背景。"
    return prompt, {"keep": keep, "modify": modify, "add": add, "reduce": reduce, "reason": reason}


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _stage_ref(asset_id: str, label: str) -> dict[str, str]:
    return {"asset_id": asset_id, "label": label}


def _build_stage_graph(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stages: list[dict[str, Any]] = [{
        "id": "input_design", "kind": "input_design", "title": "构图与视觉关系建立", "purpose": "确立作品的构图、轮廓与色彩的前期视觉设计。", "version": None,
        "inputs": [_stage_ref("final_artwork", "最终作品")],
        "outputs": [_stage_ref("reconstructed_sketch", "构图草图"), _stage_ref("reconstructed_lineart", "结构线稿"), _stage_ref("reconstructed_color_block", "色块与氛围关系")],
        "source_record_asset_id": None,
    }]
    for number, record in enumerate(records, start=1):
        generation_id = record["stage_id"]
        inputs = [_stage_ref(asset_id, "上一完整版本" if asset_id.startswith("generation_v") else "前期视觉输入") for asset_id in record["input_assets"]]
        stages.append({
            "id": generation_id, "kind": "generation", "title": f"AIGC 完整作品 Generation V{number}", "purpose": "执行图像生成，产出同一作品的完整版本。", "version": number,
            "inputs": inputs, "outputs": [_stage_ref(generation_id, f"Generation V{number} 完整画面")],
            "source_record_asset_id": record["record_asset_id"],
        })
        stages.append({
            "id": f"diagnosis_v{number}", "kind": "difference_analysis", "title": f"V{number} 视觉诊断与调整依据", "purpose": "读取当前完整版本与最终作品，形成下一轮或最终稿的判断。", "version": number,
            "inputs": [_stage_ref(generation_id, f"Generation V{number}"), _stage_ref("final_artwork", "目标最终作品")],
            "outputs": [_stage_ref(record["difference_analysis_asset_id"], "Difference Analysis"), _stage_ref(record["adjustment_reason_asset_id"], "Adjustment Reason")],
            "source_record_asset_id": record["record_asset_id"],
        })
    stages.append({
        "id": "final", "kind": "final", "title": "最终完成", "purpose": "将最后一个完整版本衔接至最终细节、色彩统一与后期处理结果。", "version": None,
        "inputs": [_stage_ref(records[-1]["stage_id"], "最后一个完整版本")],
        "outputs": [_stage_ref("final_artwork", "Final Artwork")], "source_record_asset_id": records[-1]["record_asset_id"],
    })
    return stages


def _write_human_records(output: Path, records: list[dict[str, Any]], prompts: list[dict[str, Any]]) -> None:
    prompt_lines = ["# Prompt Record", "", "作品各版本 Prompt 演进记录。", ""]
    parameter_lines = ["# Parameter Record", "", "作品各版本生成参数记录。", ""]
    for record, prompt in zip(records, prompts):
        label = record["version"].upper()
        prompt_lines.extend([f"## Prompt {label}", record["prompt"], "", "### Prompt Evolution", json.dumps(prompt["evolution"], ensure_ascii=False, indent=2), ""])
        parameter_lines.extend([f"## {label}", f"- Backend: {record['backend']}", f"- Model: {record['model']}", f"- Mode: {record['mode']}", f"- Parameters: {json.dumps(record['parameters'], ensure_ascii=False, sort_keys=True)}", f"- Source Record: {record['record_asset_id']}", ""])
    (output / filename_for("prompt_record")).write_text("\n".join(prompt_lines), encoding="utf-8")
    (output / filename_for("parameter_record")).write_text("\n".join(parameter_lines), encoding="utf-8")


def run_pipeline(input_path: str, output_dir: str, title: str, competition: str, analysis_json: str, *, backend: ImageGenerationBackend | None = None, max_iterations: int | None = None) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    try:
        analysis = json.loads(Path(analysis_json).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"analysis-json is unreadable: {analysis_json}: {exc}") from exc
    if not isinstance(analysis, dict) or not analysis:
        raise ValueError("analysis-json must be a non-empty JSON object")
    for key in ("subject", "composition", "palette", "theme"):
        _required_text(analysis, key)

    final_path = output / filename_for("final_artwork")
    _normalise_final(Path(input_path), final_path)
    reconstruct_all_assets(str(final_path), str(output))
    artwork_analysis_path = output / filename_for("artwork_analysis")
    artwork_analysis = {**analysis, "source": "final_artwork"}
    _write_json(artwork_analysis_path, artwork_analysis)

    policy = generation_policy()
    maximum = int(max_iterations if max_iterations is not None else analysis.get("max_iterations", policy["default_max_versions"]))
    if maximum < int(policy["minimum_versions"]) or maximum > int(policy["absolute_max_versions"]):
        raise ValueError(f"max_iterations must be between {policy['minimum_versions']} and {policy['absolute_max_versions']}")
    threshold = float(analysis.get("convergence_threshold", 0.86))
    resolved_backend = resolve_backend(backend)
    prompt, evolution = _build_prompt_v1(analysis)
    base_parameters = analysis.get("generation_parameters", {"guidance": 7.0, "steps": 30, "seed": 20260903})
    if not isinstance(base_parameters, dict) or not base_parameters:
        raise ValueError("generation_parameters must be a non-empty object")

    records: list[dict[str, Any]] = []
    prompts: list[dict[str, Any]] = []
    source_difference_asset_id: str | None = None
    source_adjustment_reason_asset_id: str | None = None
    for version in range(1, maximum + 1):
        generation_id, generation_rel = versioned_asset("generation", version)
        request_id, request_rel = versioned_asset("generation_request", version)
        record_id, record_rel = versioned_asset("generation_record", version)
        difference_id, difference_rel = versioned_asset("difference_analysis", version)
        adjustment_id, adjustment_rel = versioned_asset("adjustment_reason", version)
        input_asset_ids = ["reconstructed_sketch", "reconstructed_lineart", "reconstructed_color_block"] if version == 1 else [f"generation_v{version - 1}", "reconstructed_sketch", "reconstructed_lineart", "reconstructed_color_block"]
        input_paths = [str(output / (asset_specs()[asset_id]["filename"] if asset_id in asset_specs() else versioned_asset("generation", version - 1)[1])) for asset_id in input_asset_ids]
        parameters = {**base_parameters, "iteration": version, "negative_prompt": str(analysis.get("negative_prompt", ""))}
        request = {
            "version": f"v{version}", "stage_id": generation_id, "backend": resolved_backend.name, "mode": resolved_backend.mode, "model": resolved_backend.model,
            "input_assets": input_asset_ids, "input_images": input_paths, "prompt": prompt, "prompt_evolution": evolution,
            "source_difference_asset_id": source_difference_asset_id, "source_adjustment_reason_asset_id": source_adjustment_reason_asset_id,
            "negative_prompt": parameters["negative_prompt"], "parameters": parameters, "output": generation_rel,
            "output_contract": "complete_artwork_version", "status": "requested", "requested_at": datetime.now(timezone.utc).isoformat(),
        }
        _write_json(output / request_rel, request)  # Prompt exists before the backend call.
        execution = generate_image(prompt, input_paths, parameters, str(output / generation_rel), generation_id, resolved_backend)
        difference = analyze_generation_difference(output / generation_rel, final_path, artwork_analysis)
        difference["input_asset_ids"] = [generation_id, "final_artwork"]
        reasons = build_adjustment_reason(difference)
        adjustment = {"version": f"v{version}", "source_difference_asset_id": difference_id, "items": reasons}
        _write_json(output / difference_rel, difference)
        _write_json(output / adjustment_rel, adjustment)
        record = {
            "version": f"v{version}", "stage_id": generation_id, "backend": execution["backend"], "mode": execution["mode"], "model": execution["model"],
            "input_assets": input_asset_ids, "prompt": prompt, "negative_prompt": parameters["negative_prompt"], "parameters": parameters,
            "output": generation_rel, "status": "success", "generated_at": datetime.now(timezone.utc).isoformat(),
            "request_asset_id": request_id, "record_asset_id": record_id, "difference_analysis_asset_id": difference_id, "adjustment_reason_asset_id": adjustment_id,
            "complete_artwork": bool(execution["complete_artwork"]), "backend_metadata": execution["backend_metadata"],
        }
        _write_json(output / record_rel, record)
        records.append(record)
        prompts.append({"version": f"v{version}", "prompt": prompt, "evolution": evolution, "source_record_asset_id": record_id, "source_difference_asset_id": source_difference_asset_id, "source_adjustment_reason_asset_id": source_adjustment_reason_asset_id})
        if not should_continue_iteration(difference, version, maximum, threshold):
            break
        prompt, evolution = _evolve_prompt(prompt, difference, reasons, analysis)
        source_difference_asset_id, source_adjustment_reason_asset_id = difference_id, adjustment_id

    parameters_record = [{"version": record["version"], "backend": record["backend"], "model": record["model"], "mode": record["mode"], "parameters": record["parameters"], "source_record_asset_id": record["record_asset_id"]} for record in records]
    stages = _build_stage_graph(records)
    _write_human_records(output, records, prompts)
    _write_json(output / filename_for("stage_process_record"), stages)

    confirmations = analysis.get("confirmations") if isinstance(analysis.get("confirmations"), dict) else {}
    manifest: dict[str, Any] = {
        "schema_version": "0.3.0", "mode": "Reconstruction Mode",
        "artwork": {"title": title.strip(), "competition": competition.strip(), "type": str(analysis.get("type", "数字图像")).strip(), "theme": analysis["theme"], "pipeline": f"Final Artwork → Analysis → Pre-generation Inputs → {' → '.join(record['stage_id'] for record in records)} → Final"},
        "creative_rationale": {"background": str(analysis.get("creative_background", f"围绕“{analysis['theme']}”整理作品的视觉表达。")), "visual_concept": f"主体：{analysis['subject']}；构图：{analysis['composition']}；色彩：{analysis['palette']}。", "ai_collaboration": "每个 generation_vN 都是同一幅完整作品的生成执行快照；轮次由实际收敛状态动态决定。"},
        "assets": [], "generation_records": records, "prompt_record": prompts, "parameter_record": parameters_record, "stage_graph": stages,
    }
    original_tool = _original_tool(confirmations)
    if original_tool:
        manifest["original_tool"] = original_tool
    docx_name = f"{_safe_filename_part(title)}_{_safe_filename_part(competition)}_AIGC说明书.docx"
    for asset_id in required_file_asset_ids():
        spec = asset_specs()[asset_id]
        relative = docx_name if asset_id == "statement_docx" else spec["filename"]
        manifest["assets"].append(_asset_record(asset_id, relative, output, asset_id == "statement_docx"))
    for version in range(1, len(records) + 1):
        for family in ("generation", "generation_request", "generation_record", "difference_analysis", "adjustment_reason"):
            asset_id, relative = versioned_asset(family, version)
            manifest["assets"].append(_asset_record(asset_id, relative, output))
    manifest_path = output / "submission_manifest.json"
    _write_json(manifest_path, manifest)
    docx_path = output / docx_name
    build_docx_from_manifest(str(manifest_path), str(docx_path))
    docx_record = next(item for item in manifest["assets"] if item["id"] == "statement_docx")
    docx_record.update({"sha256": sha256_file(docx_path), "size_bytes": docx_path.stat().st_size})
    _write_json(manifest_path, manifest)
    validate_manifest_file(manifest_path)
    if find_soffice() is not None:
        with tempfile.TemporaryDirectory(prefix="aigc_docx_render_") as render_dir:
            audit_rendered_pages(render_docx(docx_path, render_dir))
    else:
        print("Warning: LibreOffice unavailable; structural DOCX validation passed, render validation skipped", file=sys.stderr)
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the complete-artwork AIGC version-evolution pipeline")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--competition", required=True)
    parser.add_argument("--analysis-json", required=True)
    parser.add_argument("--max-iterations", type=int)
    args = parser.parse_args()
    try:
        manifest = run_pipeline(args.input, args.output_dir, args.title, args.competition, args.analysis_json, max_iterations=args.max_iterations)
    except GenerationBackendUnavailable as exc:
        print(json.dumps({"status": exc.status, "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 3
    print(f"Pipeline complete: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
