# AIGC Competition Statement

> **Single Image Input → Automatically Reconstruct Complete Historical Materials → Satisfy Competition Requirements**
> Given only a final AI-generated artwork, automatically reverse-engineer a dynamic pipeline, reconstruct composition sketches, stage drafts, evolving Prompts, and tool-adapted parameters, and output a complete, ready-to-submit Stage-Centric document with zero dangling placeholders.

[![version](https://img.shields.io/badge/version-0.2.2-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An Agent Skill for creating honest, reviewable AIGC creation statements for Chinese university creative competitions (大广赛, 新媒体创意节, 学院奖).

---

## Three Core Work Modes

- **Reconstruction Mode**: Activated when the user provides ONLY a final artwork. Automatically maps competition requirements to a missing material checklist, executes reverse operators (`reference_to_sketch`, `reference_to_intermediate_generation`), constructs natural prompt evolutions without canned defect scripts, adapts parameters to the chosen tool, and outputs a complete, ready-to-submit document with zero dangling placeholders. Never blocks or interrogates the user.
- **Hybrid Mode**: Activated when partial authentic materials are provided. Authentic materials are preserved as `Verified` / `User-reported`; only missing stages are reconstructed.
- **Evidence Mode**: Activated when full authentic evidence is provided. Directly organizes authentic materials without unnecessary substitutions.

---

## Competition Requirements to Reverse Asset Mapping

| Requirement Item | Target Asset | Operator / Method |
|---|---|---|
| Composition Sketch / Draft | `01_reconstructed_sketch.png` | `reference_to_sketch` |
| Lineart / Input Reference | `01_reconstructed_lineart.png` | `reference_to_lineart` |
| Color / Mood Study | `01_reconstructed_color_block.png` | `reference_to_color_block` |
| Intermediate Stage Draft (V1) | `02_reconstructed_generation_v1.png` | `reference_to_intermediate_generation` |
| Iterative Enhancement Draft (V2) | `03_reconstructed_generation_v2.png` | `reference_to_intermediate_generation` |
| Evolving Prompts | Prompt V1 / V2 | Natural difference diagnosis (V1 vs final) |
| Tool-Adapted Parameters | Parameter Table | Adapted to specific tools (Seed noted as unrecorded) |
| Statement Document | 7-Section DOCX | Complete Stage-Centric document, zero placeholders |

---

## Natural & Believable Reverse Generation

1. **Natural Gap Diagnosis**: No artificial strawman scripts (e.g. "V1 must have empty background"). Generates V1, compares with final artwork, diagnoses real differences, and refines Prompt accordingly.
2. **Dynamic Stage Graph**: Derives appropriate stages dynamically (Text-to-Image, Img2img, Compositing); Minimal but Sufficient.
3. **Tool-Adapted Parameters**: Only outputs valid parameters for the chosen tool. No forced negative prompts if tool does not support it (e.g. DALL-E).
4. **Tool Demarcation**: Clearly separates original creation tool (unrecorded / visually inferred) from reproduction tool (host capability / recommended platform).
5. **Conditional Post-Processing**: No fake Photoshop assumptions without real evidence.

---

## Install

```powershell
.\scripts\install.ps1 -Platform antigravity
.\scripts\install.ps1 -Platform codex
.\scripts\install.ps1 -Platform cursor
```

## License

MIT
