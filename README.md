# AIGC Competition Statement

> **Turn your final AIGC artwork into a competition-ready creation statement.**
> 上传最终作品，整理 Prompt、AI 工作流与创作说明。

[![version](https://img.shields.io/badge/version-0.1.1-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 这是什么

一个 Agent Skill，专门帮助国内高校学生为**大广赛、大学生新媒体创意节、学院奖**等竞赛整理 AIGC 创作说明书。

**你只需要提供**：

- 参赛作品的最终成品图
- 比赛名称
- 你用过的 AI 工具（记得多少说多少）

**Agent 帮你整理**：

- 创意阐释与设计逻辑
- AI 工具说明与工作流描述
- Prompt 记录（有原始记录就用原始的；没有就基于成品分析生成**复现建议**）
- 匿名检查 + 格式验收
- 导出 Word 文档 + 打包提交

---

## 快速开始

告诉你的 Agent：

```
帮我整理这件作品的 AIGC 创作说明。
比赛：第十届大学生新媒体创意节
使用工具：ComfyUI + SDXL + Photoshop
```

然后上传作品图。Agent 会自动进入流程，按需追问缺少的信息。

**找不到官方赛事规则时**，不会停止——会用通用模板生成草稿，并明确提示你在提交前对照官方要求核查。

---

## 一个重要的设计原则

本 Skill 明确区分四类信息：

| 等级 | 含义 | 文档措辞 |
|---|---|---|
| **Verified** | 你提供了材料（图片、截图、文件） | 直接陈述 |
| **User-reported** | 你口头告知，没有材料 | "据创作者表述……" |
| **Reconstructed** | 根据成品分析推断 | "以下为复现建议……" |
| **Unknown** | 无法确认 | 留空或标注"未记录" |

**从最终成品反推的 Prompt，会明确标注为「Prompt 复现建议」，而不是「原始 Prompt」。**

---

## 支持的 Agent 平台

| 平台 | 支持方式 | 安装方式 |
|---|---|---|
| **Google Antigravity (AGY)** | ✅ Native Skill | 运行安装脚本（自动复制到 `~/.gemini/config/skills/`） |
| **Cursor** | ✅ Native Skill | 运行安装脚本（自动复制到 `~/.cursor/skills/`） |
| **OpenAI Codex** | ✅ Native Skill + AGENTS.md | 运行安装脚本（自动复制到 `~/.codex/skills/`） |
| **Windsurf** | ⚙️ Project Rule | 运行安装脚本（自动复制 Rule 文件到当前项目） |
| **Claude** | 📋 Project Instructions | 安装脚本打开配置文件 → 手动粘贴到 claude.ai |

> **说明**：Antigravity、Cursor、Codex 支持**文件级 Skill 安装**（自动复制整个 Skill 目录到标准位置）。
> Windsurf 支持**文件级 Rule 安装**（复制单个 Rule 文件到项目目录）。
> Claude 需要在 web 界面手动粘贴，安装脚本会打开对应文件方便你复制。

---

## 安装

### Windows

```powershell
git clone https://github.com/thenightmygfcomeoutthecloset/aigc-competition-statement.git
cd aigc-competition-statement
.\scripts\install.ps1
```

### macOS / Linux

```bash
git clone https://github.com/thenightmygfcomeoutthecloset/aigc-competition-statement.git
cd aigc-competition-statement
bash scripts/install.sh
```

安装脚本会提示你选择平台，显示将要复制的源路径和目标路径，执行前备份已有文件。

### Dry Run（预览不执行）

```powershell
.\scripts\install.ps1 -DryRun
```
```bash
bash scripts/install.sh --dry-run
```

### 卸载

```powershell
# 卸载指定平台
.\scripts\install.ps1 -Platform cursor -Uninstall
```
```bash
bash scripts/install.sh cursor --uninstall
```

---

## 示例

查看 [`examples/minimal-example.md`](examples/minimal-example.md) — 最简用法演示

查看 [`examples/full-example.md`](examples/full-example.md) — 完整流程演示（虚构作品）

---

## 工作流程

```
Stage 1  查找赛事要求
         ├─ 找到规则  → Competition-specific mode
         └─ 未找到   → Generic Draft Mode（继续执行，标注未校验）

Stage 2  收集素材，打 Evidence Level 标签
Stage 3  分析作品图视觉特征
Stage 4  整理创作过程叙述
Stage 5  生成 Prompt 复现建议（仅在无原始 Prompt 时）
Stage 6  生成 Word 文档（无 AI 排版痕迹）
Stage 7  合规检查（匿名 + 真实性 + 格式）
Stage 8  导出与打包
```

---

## 真实性与反编造

以下信息在未经你明确提供的情况下，**Agent 不会自动填写**：

Seed / 具体 Steps 值 / 具体 CFG 值 / Sampler 名称 / 模型版本 /
LoRA 权重 / 原始 Prompt / 创作日期 / 软件版本

详细规范见 [`skill/safety.md`](skill/safety.md)。

---

## 项目结构

```
aigc-competition-statement/
├── skill/
│   ├── SKILL.md          # Agent 调用规范（核心）
│   ├── workflow.md       # 详细阶段说明
│   ├── output-spec.md    # 输出格式规范
│   └── safety.md         # 真实性与反幻觉规范
├── templates/
│   └── competition-statement.md   # 通用竞赛模板（v0.1.1）
│   └── prompt-record.md
│   └── ai-process-report.md
│   └── evidence-checklist.md
├── adapters/
│   ├── cursor/           # Cursor .mdc Rule 文件（项目级备用）
│   ├── windsurf/         # Windsurf Rule 文件
│   ├── claude/           # Claude Project Instructions
│   └── codex/            # Codex AGENTS.md 文件
├── examples/
│   ├── minimal-example.md
│   └── full-example.md
├── scripts/
│   ├── install.ps1       # Windows 安装脚本（含 -DryRun / -Uninstall）
│   └── install.sh        # macOS/Linux 安装脚本（含 --dry-run / --uninstall）
├── CHANGELOG.md
└── LICENSE
```

---

## 适用赛事

| 赛事 | 状态 |
|---|---|
| 大广赛（全国大学生广告艺术大赛） | ✅ 通用模板 |
| 大学生新媒体创意节 | ✅ 通用模板 |
| 学院奖 | ✅ 通用模板 |
| 全国大学生数字媒体科技作品竞赛 | ✅ 通用模板 |
| 其他创意竞赛 | ✅ 通用模板 |

> 赛事专用模板计划在 v0.2.0 中引入。

---

## Contributing

欢迎 PR：增加赛事专用模板、改进安装脚本、增加新平台适配。

---

## License

MIT License — 见 [LICENSE](LICENSE)