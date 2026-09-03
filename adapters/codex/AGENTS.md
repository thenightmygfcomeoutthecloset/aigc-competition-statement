# AGENTS.md — AIGC Competition Statement Skill

This file instructs Codex on how to use the AIGC Competition Statement skill within this repository.

## Skill: aigc-competition-statement

**Core Mission (v0.3.1)**:
Single Image Input → Automatically Build Complete Process Materials → Satisfy Competition Requirements.
When a user provides only a final AI artwork, automatically build all process materials (sketches, intermediate generations, evolving Prompts, tool-adapted parameters) without blocking or interrogating the user. Output a complete, ready-to-submit stage-centric statement with zero dangling placeholders. Also supports Evidence Mode and Hybrid Mode.

## Instructions

Follow the single source of truth in this repository:
- Main Entry & Mode Routing: [SKILL.md](../../SKILL.md)
- Reconstruction & Asset Mapping: [skill/reconstruction.md](../../skill/reconstruction.md)
- Image Generation Standards: [skill/image-generation.md](../../skill/image-generation.md)
- Workflow: [skill/workflow.md](../../skill/workflow.md)
- Creation Presentation Standards: [skill/safety.md](../../skill/safety.md)
- Stage-Centric Word Output: [skill/output-spec.md](../../skill/output-spec.md)
- Output Templates: [templates/competition-statement.md](../../templates/competition-statement.md)

Ask the user once up front which tool created the artwork; record it if provided, otherwise omit it.
