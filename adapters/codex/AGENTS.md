# AGENTS.md — AIGC Competition Statement Skill

This file instructs Codex on how to use the AIGC Competition Statement skill within this repository.

## Skill: aigc-competition-statement

**Core Mission (v0.2.2)**:
Single Image Input → Automatically Reconstruct Complete Process Materials → Satisfy Competition Requirements.
When a user provides only a final AI artwork, automatically reverse-engineer all missing materials (sketches, intermediate generations, evolving Prompts, tool-adapted parameters) without blocking or interrogating the user. Output a complete, ready-to-submit stage-centric statement with zero dangling placeholders. Also supports Evidence Mode and Hybrid Mode.

## Instructions

Follow the single source of truth in this repository:
- Main Entry & Mode Routing: [SKILL.md](../../SKILL.md)
- Reconstruction & Asset Mapping: [skill/reconstruction.md](../../skill/reconstruction.md)
- Image Generation Standards: [skill/image-generation.md](../../skill/image-generation.md)
- Mode-Driven 8-Stage Workflow: [skill/workflow.md](../../skill/workflow.md)
- Safety, Anti-Hallucination & IP Check: [skill/safety.md](../../skill/safety.md)
- Stage-Centric Word Output: [skill/output-spec.md](../../skill/output-spec.md)
- Output Templates: [templates/competition-statement.md](../../templates/competition-statement.md)

Never fabricate historical facts. Reconstructed assets and prompts must be labeled `[Reconstructed]`. Never generate fake software UI screenshots.
