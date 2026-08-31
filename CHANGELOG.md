# Changelog

All notable changes to this project will be documented in this file.
This project follows [Semantic Versioning](https://semver.org/).

---

## [0.1.0] — 2026-08-31

### Added

- `skill/SKILL.md` — Agent-callable skill with structured Trigger, Evidence Levels, Anti-hallucination rules, and 8-stage Workflow
- `skill/workflow.md` — Detailed stage-by-stage workflow specification
- `skill/output-spec.md` — Output format specification for Word documents
- `skill/safety.md` — Authenticity principles, Evidence Level definitions, Prompt Reconstruction spec, anonymity checks
- `templates/competition-statement.md` — Universal competition statement template
- `templates/prompt-record.md` — Prompt record template
- `templates/ai-process-report.md` — AI process report template (for competitions requiring technical reports)
- `templates/evidence-checklist.md` — Pre-export compliance checklist (12 items)
- `adapters/cursor/aigc-competition-statement.mdc` — Cursor project rule adapter
- `adapters/windsurf/aigc-competition-statement.md` — Windsurf project rule adapter
- `adapters/claude/project-instructions.md` — Claude Project Instructions adapter
- `adapters/codex/setup-instructions.md` — Codex Setup Instructions adapter
- `examples/minimal-example.md` — Minimal usage example
- `examples/full-example.md` — Full workflow example with fictional demo artwork
- `scripts/install.ps1` — Windows PowerShell installer (no admin required)
- `scripts/install.sh` — macOS/Linux bash installer
- `README.md` — Rewritten as product homepage
- `README_EN.md` — English version of README
- `CHANGELOG.md` — This file
- `LICENSE` — MIT License

### Changed

- Restructured from single `SKILL.md` into `skill/` + `templates/` + `adapters/` + `examples/` + `scripts/`
- Replaced "copy SKILL.md and delete YAML" instructions with platform-specific ready-to-use adapter files
- Clarified Prompt Reconstruction vs. Original Prompt throughout all documents
- README rewritten from installation guide to product homepage

### Principles Established

- Evidence Levels system: [Verified] / [User-reported] / [Reconstructed] / [Unknown]
- Anti-hallucination rule list (Seed, Steps, CFG, Sampler, model version, LoRA weight, original Prompt, etc.)
- Platform support tiers: Native / Adapter / Manual paste — no longer conflated