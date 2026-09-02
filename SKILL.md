---
name: aigc-competition-statement
description: 面向大广赛、新媒体创意节、学院奖等高校赛事的 AIGC 创作说明书 Agent Skill。用户仅需提供一张最终 AI 作品，即可自动逆向推导合理创作流程、生成复现垫图、阶段结果与演进 Prompt，并输出结构完整且符合学术规范的提交文案；同时也支持整理用户提供的真实证据。
---

# AIGC 竞赛创作说明书

帮助创作者从一张最终 AI 作品自动逆向重构合理的创作全流程，或将已有真实材料整理为规范、可追溯的高校竞赛提交材料。

## 核心工作模式

- **Reconstruction Mode（逆向重构模式）**：用户仅提供一张最终作品图或材料严重缺失时自动启用。自动完成画面结构化分析、工作流推导、逆向生成复现垫图（如线稿/草图）、阶段视觉结果、演进 Prompt（V1/V2/V3）与参数建议，组织完整说明书。
- **Evidence Mode（真实证据模式）**：用户已提供原始 Prompt、垫图、工作流截图或参数时启用。直接整理真实证据，严禁无必要替代。

## 证据等级与优先级

`[Verified]` > `[User-reported]` > `[Reconstructed]` > `[Unknown]`

- `[Verified]`：文件、截图、元数据直接证明，直接陈述。
- `[User-reported]`：创作者口述，使用引述语气。
- `[Reconstructed]`：基于最终作品逆向分析与复现生成，明确标为复现内容，非原始历史记录。
- `[Unknown]`：无法确认，留空或标注“未记录”。严禁虚构 Seed 或历史参数。

## 核心工作流

`Final Artwork → Artwork Analysis → Workflow Reconstruction → Reconstructed Assets → Prompt Reconstruction → Parameter Suggestions → Creation Statement → DOCX`

## 按需读取索引

- **逆向重构与垫图/阶段生成**：阅读 [skill/reconstruction.md](skill/reconstruction.md)
- **执行完整 8 阶段详细流程**：阅读 [skill/workflow.md](skill/workflow.md)
- **真实性底线与版权/IP 审查**：阅读 [skill/safety.md](skill/safety.md)
- **Stage-Centric Word 输出规范**：阅读 [skill/output-spec.md](skill/output-spec.md)
- **说明书主模板**：使用 [templates/competition-statement.md](templates/competition-statement.md)
