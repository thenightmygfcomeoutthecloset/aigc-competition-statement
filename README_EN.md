# AIGC Competition Statement

> **Provide only a final AI-generated artwork to automatically analyze the image, reverse-engineer a plausible creation workflow, generate necessary reconstructed input sketches and stage results, and output a fully structured AIGC competition statement document.**

[![version](https://img.shields.io/badge/version-0.2.1-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An Agent Skill for creating honest, reviewable AIGC creation statements for Chinese university creative competitions (大广赛, 新媒体创意节, 学院奖).

---

## Three Core Modes

- **Reconstruction Mode**: Activated when the user provides ONLY a final artwork. Performs multi-dimensional visual analysis, infers a creation pipeline, invokes image generation capabilities to render reconstructed sketches and intermediate stages, reconstructs evolving Prompts with causal adjustment reasons, and builds a stage-centric statement. Never stops to force the user for historical records.
- **Hybrid Mode**: Activated when partial authentic materials are provided. Authentic materials are preserved as Verified/User-reported; only missing stages are reconstructed.
- **Evidence Mode**: Activated when full authentic evidence is provided. Directly organizes authentic materials without unnecessary substitutions.

---

## Stage-Centric Evidence Architecture

Organized strictly around creation stages rather than isolated screenshot categories:

$$\text{Input (Reference / Sketch)} \longrightarrow \text{Tool} \longrightarrow \text{Prompt} \longrightarrow \text{Parameters} \longrightarrow \text{Output} \longrightarrow \text{Adjustment}$$

### Seven Standard Sections
1. Basic Artwork Information
2. Creative Rationale & Design Intent
3. Stage-by-Stage Creation Process (Conditional post-processing: no fake Photoshop defaults)
4. AIGC Toolchain & Human-AI Division
5. Master Summary Table (Input → Tool → Prompt → Parameters → Output)
6. Copyright, Source, and Originality Statements (IP check)
7. Reconstructed Materials Disclaimer

---

## Evidence Levels & Anti-Hallucination

$$\text{[Verified]} > \text{[User-reported]} > \text{[Reconstructed]} > \text{[Unknown]}$$

- Never fabricate historical Prompts.
- Never fabricate historical parameters (Seed is always noted as unrecorded).
- Strictly forbid generating fake software UI screenshots (Photoshop, ComfyUI, WebUI, etc.) and claiming them as authentic evidence.
- Never claim unverified IP as dispute-free (flag as `Requires User Confirmation`).
- If host image tools are missing and images cannot be rendered, flag `Required Visual Evidence Missing`.

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
