# AIGC Competition Statement

> **Turn your final AIGC artwork into a competition-ready creation statement.**
> For Chinese university competitions (大广赛, 新媒体节, 学院奖, etc.)

[![version](https://img.shields.io/badge/version-0.1.0-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## What is this

An Agent Skill that helps university students in China create AIGC creation statements for competitions like 大广赛, 大学生新媒体创意节, and 学院奖.

**You provide**:
- Your final artwork
- The competition name
- The AI tools you used (however much you remember)

**The Agent handles**:
- Creative statement and design rationale
- AI tool usage documentation
- Prompt reconstruction (clearly marked as reconstruction, not original)
- Anonymity check + format validation
- Word document export + zip packaging

---

## Quick Start

Tell your agent:

```
Help me write an AIGC creation statement for this artwork.
Competition: 第十届大学生新媒体创意节
Tools used: ComfyUI + SDXL + Photoshop
```

Then upload your artwork. The agent will guide you through the rest.

---

## Key Design Principle: Evidence Levels

This skill explicitly distinguishes four types of information:

| Level | Meaning | How it appears in the document |
|---|---|---|
| **Verified** | You provided a file or screenshot | Stated directly |
| **User-reported** | You told the agent (no file) | "According to the creator..." |
| **Reconstructed** | Inferred from the artwork | "The following is a Prompt Reconstruction based on visual analysis..." |
| **Unknown** | Cannot be confirmed | Left blank or marked "not recorded" |

**Prompts reconstructed from the final artwork are clearly labeled as "Prompt Reconstruction", not "Original Prompt".**

Details: [`skill/safety.md`](skill/safety.md)

---

## Supported Platforms

| Platform | Support type | How to install |
|---|---|---|
| **Google Antigravity (AGY)** | ✅ Native Skill | Run install script |
| **Cursor** | ✅ Project Rule (.mdc) | Run install script |
| **Windsurf** | ✅ Project Rule | Run install script |
| **Claude** | ⚙️ Project Instructions | Paste adapter content (manual) |
| **Codex** | ⚙️ Setup Instructions | Paste adapter content (manual) |

---

## Installation

### macOS / Linux

```bash
git clone https://github.com/thenightmygfcomeoutthecloset/aigc-competition-statement.git
cd aigc-competition-statement
bash scripts/install.sh
```

### Windows

```powershell
git clone https://github.com/thenightmygfcomeoutthecloset/aigc-competition-statement.git
cd aigc-competition-statement
.\scripts\install.ps1
```

The installer will ask which platform you're using and place the right file automatically.

---

## Workflow

```
Stage 1  Check competition requirements
Stage 2  Collect and classify evidence
Stage 3  Analyze the artwork visually
Stage 4  Reconstruct the creation process
Stage 5  Generate Prompt Reconstruction (if no original Prompt)
Stage 6  Generate Word document
Stage 7  Compliance check (anonymity + authenticity)
Stage 8  Export and package
```

---

## Anti-hallucination

The agent will never automatically invent:
Seed / Steps values / CFG values / Sampler names / model versions /
LoRA weights / original Prompts / creation dates / software versions

---

## License

MIT