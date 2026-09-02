# AIGC Competition Statement

> Provide only a final AI-generated artwork to automatically analyze the image, reverse-engineer a plausible creation workflow, reconstruct necessary input sketches/prompts/parameters, and generate a fully structured AIGC competition statement document.

[![version](https://img.shields.io/badge/version-0.2.0-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An Agent Skill for creating honest, reviewable AIGC creation statements for Chinese university creative competitions (大广赛, 新媒体创意节, 学院奖).

When authentic records are provided, it prioritizes verified evidence (Evidence Mode); when records are missing, it switches to Reconstruction Mode. All reconstructed materials are strictly flagged and disclaimed.

---

## Dual Modes

- **Reconstruction Mode**: User only provides a final artwork. The skill performs multi-dimensional visual analysis, infers a creation pipeline, reverse-engineers input drafts (sketches/lineart), visual stage progressions, evolving Prompts (V1/V2/V3), and suggested parameters.
- **Evidence Mode**: User has provided authentic prompts, sketches, screenshots, or parameters. Organizes verified evidence without unnecessary replacements.

---

## Stage-Centric Evidence Architecture

Organized around creation stages rather than isolated screenshots:

$$\text{Input (Reference / Sketch)} \longrightarrow \text{Tool} \longrightarrow \text{Prompt} \longrightarrow \text{Parameters} \longrightarrow \text{Output} \longrightarrow \text{Adjustment}$$

### Seven Standard Sections
1. Basic Artwork Information
2. Creative Rationale & Design Intent
3. Stage-by-Stage Creation Process (Stage 1 to Stage 4)
4. AIGC Toolchain & Human-AI Division
5. Master Summary Table (Input → Tool → Prompt → Parameters → Output)
6. Copyright, Source, and Originality Statements
7. Reconstructed Materials Disclaimer

---

## Evidence Levels

$$\text{[Verified]} > \text{[User-reported]} > \text{[Reconstructed]} > \text{[Unknown]}$$

- `[Verified]`: Direct material evidence (files, original sketches, metadata).
- `[User-reported]`: Verbal creator account.
- `[Reconstructed]`: Inferred from artwork analysis; explicitly noted as non-historical reproduction.
- `[Unknown]`: Unrecorded facts (left blank or explicitly marked "未记录").

---

## Install

```powershell
.\scripts\install.ps1 -Platform antigravity
.\scripts\install.ps1 -Platform codex
.\scripts\install.ps1 -Platform cursor
```

On macOS or Linux:

```bash
bash scripts/install.sh antigravity
bash scripts/install.sh codex
bash scripts/install.sh cursor
```

## License

MIT
