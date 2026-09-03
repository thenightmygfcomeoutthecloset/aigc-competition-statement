#!/usr/bin/env python3
"""Repository-wide consistency checks."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

from canonical_schema import DEFAULT_SCHEMA_PATH, asset_specs, load_canonical_schema

for stream in (sys.stdout, sys.stderr):
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_VERSION = str(load_canonical_schema()["manifest_version"])


def check_version_sync() -> list[str]:
    checks = {
        "README.md": f"version-{EXPECTED_VERSION}-blue",
        "README_EN.md": f"version-{EXPECTED_VERSION}-blue",
        "CHANGELOG.md": f"## [{EXPECTED_VERSION}]",
        "scripts/install.ps1": f'$SKILL_VERSION = "{EXPECTED_VERSION}"',
        "scripts/install.sh": f'SKILL_VERSION="{EXPECTED_VERSION}"',
    }
    errors = []
    for relative, expected in checks.items():
        path = REPO_ROOT / relative
        if not path.is_file() or expected not in path.read_text(encoding="utf-8"):
            errors.append(f"{relative} does not declare v{EXPECTED_VERSION}")
    return errors


def check_mode_names() -> list[str]:
    forbidden = ("Generic Draft Mode", "双模式", "双工作模式")
    errors = []
    for path in list(REPO_ROOT.glob("*.md")) + list((REPO_ROOT / "skill").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        errors.extend(f"Forbidden mode term {term!r} in {path.relative_to(REPO_ROOT)}" for term in forbidden if term in text)
    return errors


def check_orphan_templates() -> list[str]:
    core = [REPO_ROOT / "SKILL.md", *list((REPO_ROOT / "skill").glob("*.md"))]
    references = "\n".join(path.read_text(encoding="utf-8") for path in core)
    return [
        f"Orphan template: {path.name}"
        for path in (REPO_ROOT / "templates").glob("*.md")
        if path.name not in references
    ]


def check_canonical_schema() -> list[str]:
    errors = []
    schema = load_canonical_schema()
    if Path(DEFAULT_SCHEMA_PATH) != REPO_ROOT / "schema" / "canonical-assets.yaml":
        errors.append("Canonical schema path is not repository-relative")
    if len(schema["assets"]) != len(set(schema["assets"])):
        errors.append("Canonical schema contains duplicate asset ids")
    if not schema.get("asset_families", {}).get("generation"):
        errors.append("Canonical schema does not define the dynamic generation family")
    relevant_scripts = ("reconstruct_assets.py", "run_pipeline.py", "build_docx.py", "manifest_schema.py")
    filenames = [str(spec.get("filename")) for spec in asset_specs().values() if spec.get("filename")]
    for name in relevant_scripts:
        text = (REPO_ROOT / "scripts" / name).read_text(encoding="utf-8")
        if "canonical_schema" not in text:
            errors.append(f"{name} does not load canonical_schema")
        for filename in filenames:
            if filename in text:
                errors.append(f"{name} hard-codes canonical filename {filename}")
    reconstruction = (REPO_ROOT / "scripts" / "reconstruct_assets.py").read_text(encoding="utf-8")
    for forbidden in ("visual_study", "addWeighted", "generation_v1", "generation_v2"):
        if forbidden in reconstruction:
            errors.append(f"reconstruct_assets.py contains forbidden generation fallback logic: {forbidden}")
    return errors


def check_no_utf8_bom() -> list[str]:
    errors = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() in {".ttf", ".png", ".jpg", ".docx", ".pyc"}:
            continue
        if path.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"UTF-8 BOM found: {path.relative_to(REPO_ROOT)}")
    return errors


def check_font_bundle() -> list[str]:
    font = REPO_ROOT / "assets" / "fonts" / "NotoSansSC-Regular.ttf"
    sums = REPO_ROOT / "assets" / "fonts" / "SHA256SUMS"
    license_file = REPO_ROOT / "assets" / "fonts" / "OFL.txt"
    if not font.is_file() or not sums.is_file() or not license_file.is_file():
        return ["Redistributable Noto Sans SC font bundle is incomplete"]
    expected = sums.read_text(encoding="utf-8").split()[0]
    actual = hashlib.sha256(font.read_bytes()).hexdigest()
    return [] if expected == actual else ["Bundled font SHA-256 does not match SHA256SUMS"]


def main() -> int:
    groups = {
        "version synchronization": check_version_sync,
        "mode names": check_mode_names,
        "template references": check_orphan_templates,
        "canonical schema": check_canonical_schema,
        "UTF-8 BOM": check_no_utf8_bom,
        "font bundle": check_font_bundle,
    }
    errors: list[str] = []
    print(f"Running repository consistency checks for v{EXPECTED_VERSION}")
    for label, check in groups.items():
        found = check()
        if found:
            errors.extend(found)
            print(f"[FAIL] {label}")
        else:
            print(f"[OK] {label}")
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("All consistency checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
