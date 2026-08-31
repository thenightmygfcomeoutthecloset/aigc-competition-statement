# AIGC Competition Statement

An Agent Skill for creating honest, reviewable AIGC creation statements for Chinese university creative competitions.

[![version](https://img.shields.io/badge/version-0.1.2-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Install

```powershell
.\scripts\install.ps1 -Platform codex
.\scripts\install.ps1 -Platform cursor
```

Codex user skills install to `~/.agents/skills/aigc-competition-statement/`. Cursor user skills install to `~/.cursor/skills/aigc-competition-statement/`.

On macOS or Linux:

```bash
bash scripts/install.sh codex
bash scripts/install.sh cursor
```

## Invoke

Use `$aigc-competition-statement` in Codex or `/aigc-competition-statement` in Cursor. Both platforms may also select the skill automatically when the request matches its description.

The skill separates verified evidence, user-reported information, reconstructed suggestions, and unknown facts. It never presents a reconstructed prompt as an original record or invents missing generation parameters.

## License

MIT
