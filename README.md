# AIGC Competition Statement

面向大广赛、大学生新媒体创意节、学院奖等高校创意竞赛的 AIGC 创作说明书 Agent Skill。

[![version](https://img.shields.io/badge/version-0.1.2-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 能做什么

- 整理创意阐释、AI 工具链、人机协同过程和证明材料
- 使用用户保存的原始 Prompt，或明确标注为“复现建议”
- 检查匿名、真实性、格式和 Word 元数据
- 找不到官方规则时进入 Generic Draft Mode，不冒充已符合官方要求

## 真实性原则

| 等级 | 含义 | 使用方式 |
|---|---|---|
| `Verified` | 文件、截图或元数据直接证明 | 直接陈述 |
| `User-reported` | 用户口头说明 | 使用引述语气 |
| `Reconstructed` | 根据成品推断 | 明确标为复现建议 |
| `Unknown` | 无法确认 | 留空或写“未记录” |

Skill 不会擅自填写 Seed、Steps、CFG、Sampler、模型精确版本、LoRA 权重、原始 Prompt、日期或生成次数。

## 安装

### Codex

```powershell
.\scripts\install.ps1 -Platform codex
```

安装到 `~/.agents/skills/aigc-competition-statement/`。这是当前 OpenAI 文档规定的个人 Skill 位置。

### Cursor

```powershell
.\scripts\install.ps1 -Platform cursor
```

安装到 `~/.cursor/skills/aigc-competition-statement/`。项目级备用 Rule 位于 `adapters/cursor/`。

macOS / Linux 使用：

```bash
bash scripts/install.sh codex
bash scripts/install.sh cursor
```

安装器支持 `-DryRun` / `--dry-run` 和可恢复卸载：

```powershell
.\scripts\install.ps1 -Platform codex -DryRun
.\scripts\install.ps1 -Platform codex -Uninstall
```

## 调用

在 Codex 中输入：

```text
$aigc-competition-statement 帮我整理这件作品的 AIGC 创作说明。
比赛：第十届大学生新媒体创意节
```

Cursor 可通过 `/aigc-competition-statement` 调用，也可以由 Agent 根据任务描述自动选择。

## 结构

```text
├── SKILL.md              # 真正的 Skill 入口
├── skill/                # workflow / safety / output-spec
├── templates/            # 通用说明书、Prompt、报告和检查清单
├── adapters/             # Cursor / Codex / Windsurf / Claude
└── scripts/              # Windows 与 macOS/Linux 安装器
```

Codex 技能位置依据 [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)，Cursor 技能位置依据 [Cursor Agent Skills](https://cursor.com/docs/skills)。

## License

MIT
