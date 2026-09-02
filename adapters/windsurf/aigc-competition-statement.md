---
trigger: model_decision
description: 高校 AIGC 竞赛创作说明书技能。用户仅需提供一张最终作品，即可自动分析画面、逆向重建合理创作流程与复现材料（垫图/阶段图/Prompt/参数），并输出结构完整的参赛说明文档；亦支持真实证据整理。
---

# AIGC 竞赛创作说明

处理高校 AIGC 竞赛创作说明书时，严格遵循以下规范：
- 核心规范与双模式（Evidence / Reconstruction）：参见 [SKILL.md](../../SKILL.md)
- 逆向重构流程与垫图/阶段生成：参见 [skill/reconstruction.md](../../skill/reconstruction.md)
- 八阶段执行流程：参见 [skill/workflow.md](../../skill/workflow.md)
- 真实性底线与版权审查：参见 [skill/safety.md](../../skill/safety.md)
- Stage-Centric 说明书模板：参见 [templates/competition-statement.md](../../templates/competition-statement.md)

用户仅提供最终作品时自动启动 Reconstruction Mode；有真实记录时优先使用 Evidence Mode。所有复现内容严格标记 [Reconstructed]，严禁虚构历史事实。
