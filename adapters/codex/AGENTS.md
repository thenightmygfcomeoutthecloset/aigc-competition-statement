# AGENTS.md — AIGC Competition Statement Skill

This file instructs Codex on how to use the AIGC Competition Statement skill within this repository.

## Skill: aigc-competition-statement

**Core Capability**:
Users only need to provide a single final AI-generated artwork. The skill will automatically analyze the artwork, reverse-engineer a plausible AIGC workflow, generate necessary reconstructed assets (sketches/composition drafts/intermediate results), reconstruct evolving Prompts and parameter suggestions, and generate a fully structured, stage-by-stage competition statement document. It also natively supports organizing authentic user-provided evidence in Evidence Mode.

**Activate when**:
- User mentions: AIGC 说明书 / AI 创作说明 / 比赛过程文案 / 比赛 AI 声明 / 大广赛 / 新媒体节 / 学院奖
- User uploads an AI artwork and asks to generate competition submission documentation
- User wants to reconstruct workflows, prompts, sketches/垫图, or parameter suggestions for an AIGC piece

**Do NOT activate for**: General copywriting, unrelated tool support.

## Instructions

Follow the single source of truth in this repository:
- Main entry & Dual Modes: [SKILL.md](../../SKILL.md)
- Reconstruction Mode & Reverse-engineering: [skill/reconstruction.md](../../skill/reconstruction.md)
- Detailed 8-stage workflow: [skill/workflow.md](../../skill/workflow.md)
- Authenticity, IP check & anti-hallucination rules: [skill/safety.md](../../skill/safety.md)
- Stage-Centric Word document formatting: [skill/output-spec.md](../../skill/output-spec.md)
- Output templates: [templates/competition-statement.md](../../templates/competition-statement.md)

Never fabricate historical facts. Clearly demarcate `[Reconstructed]` content from `[Verified]` records.
