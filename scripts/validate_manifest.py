#!/usr/bin/env python3
"""Command-line entry point for strict manifest validation."""

from __future__ import annotations

import argparse
import sys

from manifest_schema import ManifestValidationError, validate_manifest_file

for stream in (sys.stdout, sys.stderr):
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a submission manifest and every referenced file")
    parser.add_argument("manifest", help="Path to submission_manifest.json")
    args = parser.parse_args()
    try:
        manifest = validate_manifest_file(args.manifest)
    except ManifestValidationError as exc:
        print(f"Manifest validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Manifest valid: {len(manifest.assets)} assets, {len(manifest.stage_graph)} stages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
