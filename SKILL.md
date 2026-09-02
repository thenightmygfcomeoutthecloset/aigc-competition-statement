---
name: aigc-competition-statement
description: 面向大广赛、新媒体创意节、学院奖等高校赛事的 AIGC 创作说明书 Agent Skill。用户仅需提供一张最终 AI 作品，即可自动逆向推演全流程，缺什么补什么、造齐全部缺失的过程材料（草图垫图、中间初稿、演进Prompt、参数表），输出无占位悬挂、结构完整且可直接提交的 AIGC 创作说明文案；同时也支持整理创作者已有真实材料。
---

# AIGC 竞赛创作说明书

核心使命：**单图输入 → 逆向造齐全部历史材料 → 自动满足赛事材料要求**。
用户只需提供一张最终 AI 生成作品，Skill 即可自主逆向推导合理管线，逐项补齐缺失的草图、线稿、阶段初稿、演进 Prompt 与参数配置，输出无悬挂占位、完整可直接提交的说明文档；同时也支持已有真实证据的整理归档。

## 三工作模式与自动分流

```text
用户提交作品
↓
检查现有创作材料
↓
├── 原始过程材料充分 (Prompt/垫图/参数/截图齐全)
│   → 启动 Evidence Mode (真实证据直接归档，不生成替代品)
│
├── 材料部分缺失 (如仅有工具名或口述思路，缺少草图或Prompt)
│   → 启动 Hybrid Mode (真实材料优先，仅对缺失环节重构补全)
│
└── 只有最终作品或过程材料严重缺失
    → 启动 Reconstruction Mode (缺什么补什么，自动造齐全套材料)
    → MUST READ skill/reconstruction.md
```

## 证据等级与真实性自洽

`[Verified]` > `[User-reported]` > `[Reconstructed]` > `[Unknown]`

- `[Verified]`：文件、截图、草图原件、元数据直接证明，直接陈述。
- `[User-reported]`：创作者口头表述，使用引述语气。
- `[Reconstructed]`：基于最终作品逆向推演与实际复现生成，明确标为复现内容，绝不伪充历史事实。
- `[Unknown]`：无法确认的信息如实标为“未记录”，严禁脑补虚假 Seed。

## 按需读取索引

- **逆向重构模式与材料映射清单**：[skill/reconstruction.md](skill/reconstruction.md)
- **逆向图像生成算子与执行标准**：[skill/image-generation.md](skill/image-generation.md)
- **模式驱动八阶段详细工作流**：[skill/workflow.md](skill/workflow.md)
- **学术真实性底线与 IP 审查**：[skill/safety.md](skill/safety.md)
- **Stage-Centric Word 排版标准**：[skill/output-spec.md](skill/output-spec.md)
- **竞赛说明书标准模板**：[templates/competition-statement.md](templates/competition-statement.md)
