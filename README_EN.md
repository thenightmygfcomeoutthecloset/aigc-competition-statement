# AIGC Competition Statement

[![version](https://img.shields.io/badge/version-0.3.0-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Build an auditable competition-statement package from a final image, visual analysis, and explicit user confirmations.

## v0.3.0 complete-artwork version evolution

- `schema/canonical-assets.yaml` is the single machine-readable asset source used by the pipeline, validator, DOCX builder, and tests.
- `scripts/run_pipeline.py` performs actual asset processing, record creation, Stage Graph creation, Manifest generation, DOCX assembly, and final validation.
- Manifest validation combines JSON Schema, Pydantic, path containment, file size, image decoding, evidence-level, and SHA-256 checks.
- Every `generation_v1/v2/v3/...` is a complete snapshot of the same artwork, including subject, background, composition, color, and spatial relationships.
- Sketch, lineart, and color block are pre-generation visual inputs and never generation versions.
- Each prompt and request is persisted before a real backend call. Actual image differences then drive Adjustment Reason and the next Prompt Evolution.
- Iteration count is dynamic and minimal: V1, V1→V2, V1→V2→V3, or more within the schema safety limit.
- Without a real backend the CLI returns `generation_backend_unavailable`; it never filters or degrades Final to fabricate history.
- Copyright, originality, and original-tool claims require a recorded user confirmation. Otherwise they remain explicitly unverified.
- The DOCX embeds every canonical image and renders both Prompt Record and Parameter Record data.
- Installers include runtime scripts, schemas, requirements, and the OFL-licensed Noto Sans SC font.

## Run

```bash
python -m pip install -r requirements.txt
python scripts/run_pipeline.py --input final.png --output-dir output --title "Title" --competition "Competition" --analysis-json analysis.json
python scripts/validate_manifest.py output/submission_manifest.json
python -m pytest -q
```

LibreOffice is required for the full rendered-page regression gate.
