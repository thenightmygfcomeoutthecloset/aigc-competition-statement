---
name: aigc-competition-statement
description: 面向大广赛、新媒体创意节、学院奖等高校赛事的 AIGC 创作说明书 Agent Skill。用户仅需提供一张最终 AI 作品，即可自动逆向推导合理创作流程、生成复现垫图、阶段结果与演进 Prompt，并输出结构完整且符合学术规范的提交文案；同时也支持整理用户提供的真实证据。
---

# AIGC 竞赛创作说明书

用户只需提供一张最终 AI 生成作品，即可自动分析作品、逆向重建合理的创作流程、生成必要的复现过程材料，并最终输出结构完整、可用于竞赛提交的 AIGC 创作说明文档；同时也原生支持整理创作者保留的真实过程材料。

## 模式路由与执行分流

用户提交作品后，Agent 根据材料完备度自动分流：

```text
用户提交作品
↓
检查现有创作材料
↓
├── 原始过程材料充分 (Prompt/垫图/参数/截图齐全)
│   → 启动 Evidence Mode (优先使用真实证据，不生成多余替代品)
│
├── 材料部分缺失 (如仅有工具名或口述思路，缺少草图或Prompt)
│   → 启动 Hybrid Mode (真实材料标注 Verified/User-reported，仅对缺失环节进行重构)
│
└── 只有最终作品或过程材料严重缺失
    → 启动 Reconstruction Mode (自动逆向推演全流程)
    → MUST READ skill/reconstruction.md
```

## 证据等级与优先级

`[Verified]` > `[User-reported]` > `[Reconstructed]` > `[Unknown]`

- `[Verified]`：文件、截图、草图原件、元数据直接证明，直接客观陈述。
- `[User-reported]`：创作者口头表述，使用引述语气。
- `[Reconstructed]`：基于最终作品逆向分析与复现生成，明确标为复现内容，非原始历史记录。
- `[Unknown]`：无法确认，如实留空或标为“未记录”。严禁脑补 Seed 或历史实测参数。

## 按需读取索引

- **逆向重构模式核心规范**：[skill/reconstruction.md](skill/reconstruction.md)
- **逆向图像生成与 Fallback 规范**：[skill/image-generation.md](skill/image-generation.md)
- **八阶段详细工作流与模式驱动**：[skill/workflow.md](skill/workflow.md)
- **真实性底线、反伪造与 IP 审查**：[skill/safety.md](skill/safety.md)
- **Stage-Centric Word 排版标准**：[skill/output-spec.md](skill/output-spec.md)
- **竞赛说明书标准模板**：[templates/competition-statement.md](templates/competition-statement.md)
