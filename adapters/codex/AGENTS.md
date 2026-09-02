# AGENTS.md — AIGC Competition Statement Skill

This file instructs Codex on how to use the AIGC Competition Statement skill within this repository.

## Skill: aigc-competition-statement

**Core Capabilities**:
- **Single-Image Autonomous Pipeline (Reconstruction Mode)**: When a user only provides a final AI-generated artwork (no prompts, parameters, or sketches), automatically analyze the artwork, reverse-engineer a plausible creation workflow, generate necessary reconstructed assets (sketches, intermediate generations) via available image capabilities, reconstruct evolving Prompts with causal adjustment reasons, and output a stage-centric competition statement. Do NOT stop or prompt the user for historical records.
- **Authentic Material Organization (Evidence Mode)**: When the user provides real prompts, sketches, or screenshots, organize authentic evidence directly.

## Instructions

Follow the single source of truth in this repository:
- Main Entry & Mode Routing: [SKILL.md](../../SKILL.md)
- Reconstruction Mode: [skill/reconstruction.md](../../skill/reconstruction.md)
- Image Generation & Fallback Rules: [skill/image-generation.md](../../skill/image-generation.md)
- 8-Stage Workflow: [skill/workflow.md](../../skill/workflow.md)
- Authenticity & Anti-Hallucination: [skill/safety.md](../../skill/safety.md)
- Stage-Centric Word Output: [skill/output-spec.md](../../skill/output-spec.md)
- Output Templates: [templates/competition-statement.md](../../templates/competition-statement.md)

Never fabricate historical facts. Reconstructed assets and prompts must be labeled `[Reconstructed]`. Never generate fake software UI screenshots.
