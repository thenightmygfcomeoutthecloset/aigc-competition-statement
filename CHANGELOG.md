# Changelog

All notable changes to this project will be documented in this file.
This project follows [Semantic Versioning](https://semver.org/).

---

## [0.1.2] — 2026-08-31

### Fixed

- 将 `SKILL.md` 移到技能目录根部，使 Codex 与 Cursor 能正确发现
- Codex 个人技能安装位置修正为 `~/.agents/skills/`
- 安装器只复制 Skill 入口、规范和模板，不再复制 `.git` 或整个仓库
- 修复 Codex、Cursor 与 Windsurf adapter 的入口引用和包装格式
- 更新中英文安装与调用说明

### Removed

- 删除已弃用的 Codex 手动 Setup Instructions adapter

---

## [0.1.1] — 2026-08-31

### Fixed

- **Cursor adapter**: `adapters/cursor/aigc-competition-statement.mdc` 现在是合法的 Cursor Rule 文件
  — YAML frontmatter 位于文件顶部，不再包含安装说明或 Markdown 代码围栏包装
- **Codex adapter**: 从"手动粘贴 Setup Instructions"升级为 Native Skill 安装
  — 新增 `adapters/codex/AGENTS.md`，提供项目级 Codex 上下文
  — 安装脚本现在将整个 Skill 目录复制到 `~/.codex/skills/`
- **Cursor 支持升级**: 从"Project Rule"升级为 Native Skill
  — 安装脚本现在将整个 Skill 目录复制到 `~/.cursor/skills/`
  — 同时保留 `.mdc` Rule 文件供项目级使用
- **卸载逻辑修复**: 安装脚本现在支持平台专属卸载
  — `install.ps1 -Platform cursor -Uninstall` 只卸载 Cursor，不影响其他平台
  — `install.sh cursor --uninstall` 同上
  — 每个平台的卸载逻辑独立，不再只删除 Antigravity 目录
- **新增 Dry Run 模式**: 运行前预览安装计划（不实际写入文件）
  — `install.ps1 -DryRun`
  — `install.sh --dry-run`
- **安装脚本显示明确信息**: 现在在执行前显示 Source / Target / Backup 路径和卸载命令
- **Workflow Stage 1 修复**: 找不到赛事官方规则时不再停止
  — 进入 Generic Draft Mode，使用通用模板继续生成
  — 在文档顶部加入未校验警示，提示用户提交前核查
- **README 平台描述修正**:
  — Codex / Cursor 升级为 Native Skill（不再是"手动粘贴"）
  — Windsurf 明确为 Project Rule
  — Claude 明确为手动粘贴（安装脚本提供文件）
  — 区分了"Skill 安装"和"手动粘贴"，不再混为一谈
- **SKILL.md 模板描述修正**: 明确 v0.1.1 所有赛事使用通用模板，不再暗示存在赛事专用模板

### Added

- `adapters/codex/AGENTS.md` — 用于 Codex 项目级 AGENTS.md 上下文注入

### Changed

- Platform support table updated in README.md and README_EN.md
- `scripts/install.ps1`: 重写，支持 `-Platform`、`-Uninstall`、`-DryRun` 参数
- `scripts/install.sh`: 重写，支持 `<platform>`、`--uninstall`、`--dry-run` 参数
- `skill/SKILL.md`: 版本更新至 0.1.1，修正模板描述
- `skill/workflow.md`: Stage 1 增加 Generic Draft Mode 逻辑

---

## [0.1.0] — 2026-08-31

### Added

- `skill/SKILL.md` — Agent-callable skill with structured Trigger, Evidence Levels, Anti-hallucination rules, and 8-stage Workflow
- `skill/workflow.md` — Detailed stage-by-stage workflow specification
- `skill/output-spec.md` — Output format specification for Word documents
- `skill/safety.md` — Authenticity principles, Evidence Level definitions, Prompt Reconstruction spec, anonymity checks
- `templates/competition-statement.md` — Universal competition statement template
- `templates/prompt-record.md` — Prompt record template
- `templates/ai-process-report.md` — AI process report template
- `templates/evidence-checklist.md` — Pre-export compliance checklist (12 items)
- `adapters/cursor/aigc-competition-statement.mdc` — Cursor project rule adapter
- `adapters/windsurf/aigc-competition-statement.md` — Windsurf project rule adapter
- `adapters/claude/project-instructions.md` — Claude Project Instructions adapter
- `adapters/codex/setup-instructions.md` — Codex Setup Instructions adapter (deprecated in v0.1.1)
- `examples/full-example.md` — Full workflow example with fictional demo artwork
- `examples/minimal-example.md` — Minimal usage example
- `scripts/install.ps1` — Windows PowerShell installer
- `scripts/install.sh` — macOS/Linux bash installer
- `README.md`, `README_EN.md`, `CHANGELOG.md`, `LICENSE`

### Principles Established

- Evidence Levels system: [Verified] / [User-reported] / [Reconstructed] / [Unknown]
- Anti-hallucination rule list
- Platform support tiers: Native / Rule Adapter / Manual paste
