#!/usr/bin/env python3
"""Load and validate the repository's canonical asset schema."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any
import re

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA_PATH = REPO_ROOT / "schema" / "canonical-assets.yaml"


class CanonicalSchemaError(ValueError):
    pass


@lru_cache(maxsize=4)
def load_canonical_schema(schema_path: str | None = None) -> dict[str, Any]:
    path = Path(schema_path).resolve() if schema_path else DEFAULT_SCHEMA_PATH
    if not path.is_file():
        raise CanonicalSchemaError(f"Canonical asset schema not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("assets"), dict) or not isinstance(data.get("asset_families"), dict):
        raise CanonicalSchemaError("Canonical asset schema must contain assets and asset_families mappings")
    if not data["assets"]:
        raise CanonicalSchemaError("Canonical asset schema assets mapping must not be empty")
    allowed = set(data.get("evidence_levels", []))
    if not allowed:
        raise CanonicalSchemaError("Canonical asset schema must define evidence_levels")
    for asset_id, spec in data["assets"].items():
        if not isinstance(spec, dict) or not spec.get("type"):
            raise CanonicalSchemaError(f"Asset {asset_id!r} has no type")
        levels = set(spec.get("evidence_levels", []))
        if not levels or not levels <= allowed:
            raise CanonicalSchemaError(f"Asset {asset_id!r} has invalid evidence_levels")
        if spec.get("type") != "text" and not (spec.get("filename") or spec.get("filename_pattern")):
            raise CanonicalSchemaError(f"File asset {asset_id!r} has no filename")
    for family, spec in data["asset_families"].items():
        if not all(spec.get(key) for key in ("id_pattern", "filename_pattern", "type", "evidence_levels")):
            raise CanonicalSchemaError(f"Asset family {family!r} is incomplete")
    policy = data.get("generation_policy", {})
    if not 1 <= int(policy.get("minimum_versions", 0)) <= int(policy.get("absolute_max_versions", 0)):
        raise CanonicalSchemaError("generation_policy bounds are invalid")
    return data


def asset_specs(schema_path: str | None = None) -> dict[str, dict[str, Any]]:
    return load_canonical_schema(schema_path)["assets"]


def required_file_asset_ids(schema_path: str | None = None) -> list[str]:
    return [
        asset_id
        for asset_id, spec in asset_specs(schema_path).items()
        if spec.get("required") and spec.get("type") != "text"
    ]


def docx_image_asset_ids(schema_path: str | None = None, generation_versions: int = 0) -> list[str]:
    fixed = [
        asset_id
        for asset_id, spec in asset_specs(schema_path).items()
        if spec.get("type") == "image" and spec.get("embed_in_docx")
    ]
    dynamic = [versioned_asset("generation", version, schema_path)[0] for version in range(1, generation_versions + 1)]
    return fixed + dynamic


def asset_family_specs(schema_path: str | None = None) -> dict[str, dict[str, Any]]:
    return load_canonical_schema(schema_path)["asset_families"]


def versioned_asset(family: str, version: int, schema_path: str | None = None) -> tuple[str, str]:
    if version < 1:
        raise CanonicalSchemaError("Generation version must be positive")
    spec = asset_family_specs(schema_path).get(family)
    if spec is None:
        raise CanonicalSchemaError(f"Unknown asset family: {family}")
    values = {"version": version, "sequence": version + int(spec.get("sequence_offset", 0))}
    return str(spec["id_pattern"]).format(**values), str(spec["filename_pattern"]).format(**values)


def match_versioned_asset(asset_id: str, path: str, schema_path: str | None = None) -> tuple[str, int] | None:
    normalized = path.replace("\\", "/")
    for family, spec in asset_family_specs(schema_path).items():
        id_regex = "^" + re.escape(str(spec["id_pattern"])).replace(re.escape("{version}"), r"([1-9][0-9]*)") + "$"
        match = re.match(id_regex, asset_id)
        if match:
            version = int(match.group(1))
            expected_id, expected_path = versioned_asset(family, version, schema_path)
            if asset_id != expected_id or normalized != expected_path:
                raise CanonicalSchemaError(f"Asset {asset_id} must use canonical path {expected_path!r}")
            return family, version
    return None


def generation_policy(schema_path: str | None = None) -> dict[str, Any]:
    return load_canonical_schema(schema_path)["generation_policy"]


def filename_for(asset_id: str, schema_path: str | None = None) -> str:
    spec = asset_specs(schema_path).get(asset_id)
    if spec is None:
        raise CanonicalSchemaError(f"Unknown canonical asset id: {asset_id}")
    filename = spec.get("filename")
    if not filename:
        raise CanonicalSchemaError(f"Asset {asset_id!r} has no fixed filename")
    return str(filename)
