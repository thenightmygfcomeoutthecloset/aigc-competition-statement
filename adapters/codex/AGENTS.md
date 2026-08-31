# AGENTS.md — AIGC Competition Statement Skill

This file instructs Codex on how to use the AIGC Competition Statement skill within this repository.

## Skill: aigc-competition-statement

**Purpose**: Help users document their AIGC creation process for Chinese university competitions.

**Activate when**:
- User mentions: AIGC 说明书 / AI 创作说明 / 比赛 AI 声明 / 大广赛 / 新媒体节 / 学院奖
- User wants to document AI tool usage for a competition submission

**Do NOT activate for**: General copywriting, unrelated AI tool questions.

## Evidence Levels (CRITICAL)

Classify all information before using it:

- [Verified] — User provided a file/screenshot/metadata → State directly
- [User-reported] — User said it verbally (no file) → "据创作者表述……"
- [Reconstructed] — Inferred from the final artwork → "以下为复现建议，基于视觉分析……"
- [Unknown] — Cannot confirm → Leave blank or write "未记录"

## Anti-Hallucination Rules

NEVER auto-fill: Seed / Steps values / CFG values / Sampler names / model versions /
LoRA weights / original Prompts / creation dates / software versions

## Prompt Reconstruction

Prompts inferred from the artwork MUST be labeled:
"以下 Prompt 复现建议基于最终作品视觉分析生成，非创作时原始记录。"

NEVER write: "当时使用的原始 Prompt 为……"

## Workflow

1. Find competition requirements (not found → Generic Draft Mode, continue with warning)
2. Collect and classify all evidence
3. Analyze artwork visually ([Reconstructed] label)
4. Write creation process (from [Verified] + [User-reported] only)
5. Generate Prompt reconstruction (only if no original Prompt)
6. Generate Word document (no AI formatting artifacts)
7. Compliance check (anonymity + authenticity)
8. Export and package

## Full Specification

See SKILL.md, skill/workflow.md, and skill/safety.md in this repository.
