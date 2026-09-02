# AIGC Competition Statement

> **Single Image Input → Automatically Reconstruct Complete Historical Materials → Satisfy Competition Requirements**
> Given only a final AI-generated artwork, automatically reverse-engineer a dynamic pipeline, reconstruct composition sketches, lineart, color studies, intermediate drafts (V1/V2), evolving Prompts, and tool-adapted parameters, and output a complete, ready-to-submit Stage-Centric document with zero dangling placeholders.

[![version](https://img.shields.io/badge/version-0.2.2-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An Agent Skill for creating honest, reviewable AIGC creation statements for Chinese university creative competitions (大广赛, 新媒体创意节, 学院奖).

---

## Three Core Work Modes

- **Reconstruction Mode**: Activated when the user provides ONLY a final artwork. Automatically maps competition requirements to the Canonical Required Assets Manifest, executes reverse operators (`reference_to_sketch`, `reference_to_lineart`, `reference_to_color_block`, `reference_to_intermediate_generation`), constructs natural prompt evolutions without canned defect scripts, adapts parameters to the chosen tool, and outputs a complete, ready-to-submit document with zero dangling placeholders.
- **Hybrid Mode**: Activated when partial authentic materials are provided. Authentic materials are preserved as `[Verified]`; missing stages are reconstructed.
- **Evidence Mode**: Activated when full authentic evidence is provided. Directly organizes authentic materials without unnecessary substitutions.

---

## Canonical Required Assets Schema

Single Source of Truth defined in `skill/reconstruction.md`:

| Asset ID | Filename / Artifact | Operator / Source | Role |
|---|---|---|---|
| `final_artwork` | `final.png` | User Provided | Final AI artwork (`[Verified]`) |
| `reconstructed_sketch` | `01_reconstructed_sketch.png` | `reference_to_sketch` | Composition sketch & perspective skeleton |
| `reconstructed_lineart` | `01_reconstructed_lineart.png` | `reference_to_lineart` | Clean contour lineart for guidance |
| `reconstructed_color_block` | `01_reconstructed_color_block.png` | `reference_to_color_block` | Color & mood block-in study |
| `generation_v1` | `02_reconstructed_generation_v1.png` | `reference_to_intermediate_generation` | Intermediate stage 1 generation |
| `generation_v2` | `03_reconstructed_generation_v2.png` | `reference_to_intermediate_generation` | Iterative stage 2 refined generation |
| `prompt_v1` | Prompt V1 | Semantic extraction | Initial prompt formulation |
| `prompt_v2` | Prompt V2 | Real difference diagnosis | Enhanced prompt (with negative prompt if supported) |
| `parameter_record` | Parameter Profile | Tool-adapted mapping | Valid parameters for chosen tool (Seed unrecorded) |
| `prompt_record` | `prompt-record.md` | Template rendering | Stage-Aware prompt record table |
| `stage_process_record`| `stage_graph.json` | Dynamic pipeline | Data-driven stage graph structure |
| `statement_docx` | `{Title}_{Contest}_Statement.docx` | `scripts/build_docx.py` | Complete A4 Word document with embedded images |

---

## Directory Layout

### 1. Repository Layout
- `SKILL.md`: Main entrance & three-mode routing.
- `skill/`: Core downscaled specifications (`reconstruction.md`, `image-generation.md`, `workflow.md`, `safety.md`, `output-spec.md`).
- `templates/`: Presentation layer (`competition-statement.md`, `prompt-record.md`, `evidence-checklist.md`).
- `adapters/`: Thin wrappers for Cursor, Codex, Windsurf, and Claude.
- `scripts/`: Executable builders, fallback generators, placeholder scanners, consistency checkers, and installers.
- `examples/`: Regression fixtures (`final-image-only.md`, `minimal-example.md`, `full-example.md`).
- `tests/`: Automated regression test suite.

### 2. Installed Runtime Layout
Installed to `~/.gemini/config/skills/`, `~/.agents/skills/`, or `~/.cursor/skills/`:
- `SKILL.md`, `skill/`, `templates/`, `adapters/`, `scripts/`, `README.md`, `LICENSE`.

---

## Install

```powershell
.\scripts\install.ps1 -Platform antigravity
.\scripts\install.ps1 -Platform codex
.\scripts\install.ps1 -Platform cursor
```

## License

MIT
