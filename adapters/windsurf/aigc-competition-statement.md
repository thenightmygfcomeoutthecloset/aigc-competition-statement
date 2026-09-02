---
trigger: model_decision
description: 高校 AIGC 竞赛创作说明书技能。用户仅需提供一张最终作品，自动进入 Reconstruction Mode 逆向重构合理创作流程、生成复现垫图、阶段图、演进 Prompt 与建议参数，输出完整参赛文档；亦支持真实证据整理。
---

# AIGC 竞赛创作说明

处理高校 AIGC 竞赛创作说明书时，严格遵循以下规范：
- 核心规范与三模式路由（Evidence / Hybrid / Reconstruction）：参见 [SKILL.md](../../SKILL.md)
- 逆向重构流程规范：参见 [skill/reconstruction.md](../../skill/reconstruction.md)
- 图像生成与 Fallback：参见 [skill/image-generation.md](../../skill/image-generation.md)
- 八阶段执行流程：参见 [skill/workflow.md](../../skill/workflow.md)
- 真实性底线与 IP 审查：参见 [skill/safety.md](../../skill/safety.md)
- 说明书标准模板：参见 [templates/competition-statement.md](../../templates/competition-statement.md)

用户仅提供最终作品时自动启动 Reconstruction Mode，严禁强制要求补齐材料。所有复现内容严格标记 [Reconstructed]，严禁伪造软件操作历史截屏。
