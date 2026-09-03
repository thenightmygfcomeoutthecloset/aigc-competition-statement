#!/usr/bin/env python3
"""Strict schema, causal-chain, and filesystem validation for manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Annotated, Any, Literal

from jsonschema import Draft202012Validator
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from canonical_schema import (
    asset_family_specs,
    asset_specs,
    match_versioned_asset,
    required_file_asset_ids,
    versioned_asset,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
JSON_SCHEMA_PATH = REPO_ROOT / "schema" / "submission-manifest.schema.json"
NonEmpty = Annotated[str, Field(min_length=1)]
EvidenceLevel = Literal["[Verified]", "[User-reported]", "[Reconstructed]", "[Unknown]"]
Scalar = str | int | float | bool


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)


class Artwork(StrictModel):
    title: NonEmpty
    competition: NonEmpty
    type: NonEmpty
    theme: NonEmpty
    pipeline: NonEmpty


class CreativeRationale(StrictModel):
    background: NonEmpty
    visual_concept: NonEmpty
    ai_collaboration: NonEmpty


class ProvenanceClaim(StrictModel):
    value: NonEmpty
    evidence_level: Literal["[User-reported]", "[Unknown]"]
    confirmation_source: str | None

    @model_validator(mode="after")
    def validate_source(self) -> "ProvenanceClaim":
        if self.evidence_level == "[User-reported]" and not (self.confirmation_source or "").strip():
            raise ValueError("User-reported provenance requires confirmation_source")
        if self.evidence_level == "[Unknown]" and "未核验" not in self.value:
            raise ValueError("Unknown provenance must be explicitly marked 未核验")
        return self


class Provenance(StrictModel):
    copyright: ProvenanceClaim
    originality: ProvenanceClaim
    original_tool: ProvenanceClaim


class AssetRecord(StrictModel):
    id: NonEmpty
    path: NonEmpty
    evidence_level: EvidenceLevel
    sha256: str | None
    size_bytes: int | None = Field(ge=1)
    provenance: Literal["provided_input", "current_reconstruction_output", "verified_historical_asset"]


class PromptEvolution(StrictModel):
    keep: list[NonEmpty]
    modify: list[NonEmpty]
    add: list[NonEmpty]
    reduce: list[NonEmpty]
    reason: list[NonEmpty] = Field(min_length=1)


class GenerationRecord(StrictModel):
    version: NonEmpty
    stage_id: NonEmpty
    backend: NonEmpty
    mode: NonEmpty
    model: NonEmpty
    input_assets: list[NonEmpty] = Field(min_length=1)
    prompt: NonEmpty
    negative_prompt: str
    parameters: dict[str, Scalar] = Field(min_length=1)
    output: NonEmpty
    status: Literal["success"]
    generated_at: NonEmpty
    request_asset_id: NonEmpty
    record_asset_id: NonEmpty
    difference_analysis_asset_id: NonEmpty
    adjustment_reason_asset_id: NonEmpty
    complete_artwork: Literal[True]
    artifact_provenance: Literal["current_reconstruction_output", "verified_historical_asset"]
    backend_metadata: dict[str, Any]


class PromptVersion(StrictModel):
    version: NonEmpty
    prompt: NonEmpty
    evolution: PromptEvolution
    source_record_asset_id: NonEmpty
    source_difference_asset_id: str | None
    source_adjustment_reason_asset_id: str | None


class ParameterVersion(StrictModel):
    version: NonEmpty
    backend: NonEmpty
    model: NonEmpty
    mode: NonEmpty
    parameters: dict[str, Scalar] = Field(min_length=1)
    source_record_asset_id: NonEmpty


class StageRef(StrictModel):
    asset_id: NonEmpty
    label: NonEmpty
    evidence_level: EvidenceLevel


class Stage(StrictModel):
    id: NonEmpty
    kind: Literal["input_design", "generation", "difference_analysis", "final"]
    title: NonEmpty
    purpose: NonEmpty
    version: int | None = Field(ge=1)
    inputs: list[StageRef] = Field(min_length=1)
    outputs: list[StageRef] = Field(min_length=1)
    source_record_asset_id: str | None
    evidence_level: EvidenceLevel


class Manifest(StrictModel):
    schema_version: Literal["0.3.0"]
    mode: Literal["Evidence Mode", "Hybrid Mode", "Reconstruction Mode"]
    artwork: Artwork
    creative_rationale: CreativeRationale
    provenance: Provenance
    assets: list[AssetRecord] = Field(min_length=1)
    generation_records: list[GenerationRecord] = Field(min_length=1)
    prompt_record: list[PromptVersion] = Field(min_length=1)
    parameter_record: list[ParameterVersion] = Field(min_length=1)
    stage_graph: list[Stage] = Field(min_length=1)
    disclaimer: NonEmpty

    @model_validator(mode="after")
    def validate_causal_chain(self) -> "Manifest":
        ids = [asset.id for asset in self.assets]
        if len(ids) != len(set(ids)):
            raise ValueError("Manifest contains duplicate asset ids")
        stages = [stage.id for stage in self.stage_graph]
        if len(stages) != len(set(stages)):
            raise ValueError("Stage ids must be unique")
        versions = list(range(1, len(self.generation_records) + 1))
        expected_versions = [f"v{number}" for number in versions]
        if [record.version for record in self.generation_records] != expected_versions:
            raise ValueError("Generation versions must be contiguous and ordered from v1")
        if [item.version for item in self.prompt_record] != expected_versions:
            raise ValueError("Prompt Record versions must match execution records")
        if [item.version for item in self.parameter_record] != expected_versions:
            raise ValueError("Parameter Record versions must match execution records")

        expected_ids = set(required_file_asset_ids())
        for number in versions:
            for family in asset_family_specs():
                expected_ids.add(versioned_asset(family, number)[0])
        if set(ids) != expected_ids:
            raise ValueError(f"Manifest asset ids do not match schema and execution versions; missing={sorted(expected_ids-set(ids))}, extra={sorted(set(ids)-expected_ids)}")
        by_id = {asset.id: asset for asset in self.assets}
        for asset in self.assets:
            fixed = asset_specs().get(asset.id, {}).get("filename")
            if fixed and asset.path.replace("\\", "/") != fixed:
                raise ValueError(f"Asset {asset.id} must use canonical path {fixed!r}")
            if asset.id not in asset_specs() and match_versioned_asset(asset.id, asset.path) is None:
                raise ValueError(f"Unknown dynamic asset: {asset.id}")
        if not by_id["statement_docx"].path.lower().endswith(".docx"):
            raise ValueError("statement_docx path must end in .docx")

        disallowed = {"opencv_filter", "deterministic_visual_study", "local_filter"}
        known = set(ids)
        for number, record in zip(versions, self.generation_records):
            version = f"v{number}"
            generation_id, generation_path = versioned_asset("generation", number)
            request_id, _ = versioned_asset("generation_request", number)
            record_id, _ = versioned_asset("generation_record", number)
            difference_id, _ = versioned_asset("difference_analysis", number)
            adjustment_id, _ = versioned_asset("adjustment_reason", number)
            if record.backend in disallowed:
                raise ValueError("Generation execution cannot use an OpenCV/filter backend")
            if record.stage_id != generation_id or record.output != generation_path:
                raise ValueError(f"{version} output does not match canonical generation asset")
            if (record.request_asset_id, record.record_asset_id, record.difference_analysis_asset_id, record.adjustment_reason_asset_id) != (request_id, record_id, difference_id, adjustment_id):
                raise ValueError(f"{version} execution record references incorrect evidence assets")
            prompt_item, parameter_item = self.prompt_record[number - 1], self.parameter_record[number - 1]
            if prompt_item.prompt != record.prompt or prompt_item.source_record_asset_id != record_id:
                raise ValueError(f"{version} Prompt Record is not derived from its execution record")
            if (parameter_item.backend, parameter_item.model, parameter_item.mode, parameter_item.parameters, parameter_item.source_record_asset_id) != (record.backend, record.model, record.mode, record.parameters, record_id):
                raise ValueError(f"{version} Parameter Record is not derived from its execution record")
            if number > 1:
                prior = self.generation_records[number - 2]
                evolution = prompt_item.evolution
                if not evolution.keep or not evolution.modify or not evolution.reason:
                    raise ValueError(f"{version} must contain traceable Prompt Evolution")
                if prior.stage_id not in record.input_assets:
                    raise ValueError(f"{version} must use the preceding complete generation as input")
                if record.prompt == prior.prompt:
                    raise ValueError(f"{version} prompt must evolve from the preceding prompt")
                expected_difference = prior.difference_analysis_asset_id
                expected_adjustment = prior.adjustment_reason_asset_id
                if (prompt_item.source_difference_asset_id, prompt_item.source_adjustment_reason_asset_id) != (expected_difference, expected_adjustment):
                    raise ValueError(f"{version} Prompt Evolution is not linked to the preceding diagnosis")
            elif prompt_item.source_difference_asset_id is not None or prompt_item.source_adjustment_reason_asset_id is not None:
                raise ValueError("v1 cannot claim a preceding Difference Analysis")
        levels = {asset.id: asset.evidence_level for asset in self.assets}
        for stage in self.stage_graph:
            refs = [*stage.inputs, *stage.outputs]
            if any(ref.asset_id not in known for ref in refs):
                raise ValueError(f"Stage {stage.id} references an unknown asset")
            if any(ref.evidence_level != levels[ref.asset_id] for ref in refs):
                raise ValueError(f"Stage {stage.id} evidence does not match its asset")
        generation_stages = [stage for stage in self.stage_graph if stage.kind == "generation"]
        diagnosis_stages = [stage for stage in self.stage_graph if stage.kind == "difference_analysis"]
        if len(generation_stages) != len(self.generation_records):
            raise ValueError("Stage Graph generation count must come from execution records")
        if len(diagnosis_stages) != len(self.generation_records):
            raise ValueError("Stage Graph diagnosis count must match execution records")
        for stage, record in zip(generation_stages, self.generation_records):
            if stage.id != record.stage_id or stage.source_record_asset_id != record.record_asset_id:
                raise ValueError("Stage Graph generation stage is not tied to its execution record")
        for stage, record in zip(diagnosis_stages, self.generation_records):
            output_ids = {item.asset_id for item in stage.outputs}
            if stage.source_record_asset_id != record.record_asset_id or output_ids != {record.difference_analysis_asset_id, record.adjustment_reason_asset_id}:
                raise ValueError("Stage Graph diagnosis stage is not tied to execution evidence")
        return self


class ManifestValidationError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_asset_path(base_dir: Path, relative_path: str) -> Path:
    candidate = Path(relative_path)
    if candidate.is_absolute():
        raise ManifestValidationError(f"Asset path must be relative to the manifest: {relative_path}")
    resolved = (base_dir / candidate).resolve()
    try:
        resolved.relative_to(base_dir.resolve())
    except ValueError as exc:
        raise ManifestValidationError(f"Asset path escapes manifest directory: {relative_path}") from exc
    return resolved


def validate_manifest_data(data: Any) -> Manifest:
    if not isinstance(data, dict) or not data:
        raise ManifestValidationError("Manifest must be a non-empty JSON object")
    schema = json.loads(JSON_SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda item: list(item.path))
    if errors:
        details = "; ".join(f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors[:8])
        raise ManifestValidationError(f"JSON Schema validation failed: {details}")
    try:
        return Manifest.model_validate(data)
    except ValidationError as exc:
        raise ManifestValidationError(f"Pydantic validation failed: {exc}") from exc


def validate_manifest_file(manifest_path: str | Path, *, verify_files: bool = True, allow_missing_asset_ids: set[str] | None = None) -> Manifest:
    path = Path(manifest_path)
    if not path.is_file() or path.stat().st_size == 0:
        raise ManifestValidationError(f"Manifest is missing or empty: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestValidationError(f"Manifest is not valid JSON: {path}: {exc}") from exc
    manifest = validate_manifest_data(data)
    if not verify_files:
        return manifest
    allowed_missing = allow_missing_asset_ids or set()
    base_dir = path.resolve().parent
    specs = asset_specs()
    families = asset_family_specs()
    for asset in manifest.assets:
        asset_path = _resolve_asset_path(base_dir, asset.path)
        if asset.id in allowed_missing:
            continue
        if not asset_path.is_file():
            raise ManifestValidationError(f"Asset does not exist: {asset.id}: {asset.path}")
        size = asset_path.stat().st_size
        if size == 0:
            raise ManifestValidationError(f"Asset is empty: {asset.id}: {asset.path}")
        if asset.size_bytes != size or asset.sha256 != sha256_file(asset_path):
            raise ManifestValidationError(f"Asset size or hash mismatch: {asset.id}")
        dynamic = match_versioned_asset(asset.id, asset.path) if asset.id not in specs else None
        spec = specs.get(asset.id) or families[dynamic[0]]
        if asset.evidence_level not in spec["evidence_levels"]:
            raise ManifestValidationError(f"Invalid evidence level for {asset.id}")
        if spec["type"] == "image":
            try:
                with Image.open(asset_path) as image:
                    image.verify()
            except (OSError, UnidentifiedImageError) as exc:
                raise ManifestValidationError(f"Image cannot be decoded: {asset.id}: {asset.path}") from exc

    paths = asset_path_map(manifest, path)
    for record in manifest.generation_records:
        record_data = json.loads(paths[record.record_asset_id].read_text(encoding="utf-8"))
        if record_data != record.model_dump(mode="json"):
            raise ManifestValidationError(f"Execution record file differs from Manifest: {record.version}")
        request = json.loads(paths[record.request_asset_id].read_text(encoding="utf-8"))
        prompt_item = manifest.prompt_record[int(record.version[1:]) - 1]
        request_projection = (
            request.get("stage_id"), request.get("backend"), request.get("mode"), request.get("model"),
            request.get("input_assets"), request.get("prompt"), request.get("negative_prompt"),
            request.get("parameters"), request.get("output"), request.get("status"),
            request.get("source_difference_asset_id"), request.get("source_adjustment_reason_asset_id"),
        )
        record_projection = (
            record.stage_id, record.backend, record.mode, record.model, record.input_assets, record.prompt,
            record.negative_prompt, record.parameters, record.output, "requested",
            prompt_item.source_difference_asset_id, prompt_item.source_adjustment_reason_asset_id,
        )
        if request_projection != record_projection:
            raise ManifestValidationError(f"Generation request does not prove pre-execution prompt use: {record.version}")
        difference = json.loads(paths[record.difference_analysis_asset_id].read_text(encoding="utf-8"))
        if difference.get("input_asset_ids") != [record.stage_id, "final_artwork"]:
            raise ManifestValidationError(f"Difference Analysis inputs are not traceable: {record.version}")
        required_difference_sections = ("composition", "subject", "spatial_relationship", "color", "lighting", "style", "detail", "priority_adjustments")
        if any(not isinstance(difference.get(key), list) or not difference[key] for key in required_difference_sections):
            raise ManifestValidationError(f"Difference Analysis is incomplete: {record.version}")
        adjustment = json.loads(paths[record.adjustment_reason_asset_id].read_text(encoding="utf-8"))
        if adjustment.get("source_difference_asset_id") != record.difference_analysis_asset_id:
            raise ManifestValidationError(f"Adjustment Reason is not derived from Difference Analysis: {record.version}")
        adjustment_items = adjustment.get("items")
        if not isinstance(adjustment_items, list) or not adjustment_items or any(not all(str(item.get(key, "")).strip() for key in ("observed_issue", "visual_effect", "adjustment", "reason")) for item in adjustment_items if isinstance(item, dict)) or any(not isinstance(item, dict) for item in adjustment_items):
            raise ManifestValidationError(f"Adjustment Reason is incomplete: {record.version}")
    stage_data = json.loads(paths["stage_process_record"].read_text(encoding="utf-8"))
    if stage_data != [stage.model_dump(mode="json") for stage in manifest.stage_graph]:
        raise ManifestValidationError("Stage Graph file does not match Manifest")
    prompt_text = paths["prompt_record"].read_text(encoding="utf-8")
    parameter_text = paths["parameter_record"].read_text(encoding="utf-8")
    for record in manifest.generation_records:
        if record.prompt not in prompt_text or record.backend not in parameter_text or record.model not in parameter_text:
            raise ManifestValidationError(f"Rendered records do not derive from execution record {record.version}")
    return manifest


def asset_path_map(manifest: Manifest, manifest_path: str | Path) -> dict[str, Path]:
    base_dir = Path(manifest_path).resolve().parent
    return {asset.id: _resolve_asset_path(base_dir, asset.path) for asset in manifest.assets}
