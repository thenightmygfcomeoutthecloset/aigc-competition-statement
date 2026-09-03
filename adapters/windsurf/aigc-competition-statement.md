---
trigger: model_decision
description: 高校 AIGC 竞赛创作说明书技能。单图输入即可自动造齐全部创作过程材料（草图、阶段稿、演进Prompt、参数表），满足赛事要求，输出无悬挂占位、完整可提交的参赛说明文档；亦支持真实材料整理。
---

# AIGC 竞赛创作说明

处理高校 AIGC 竞赛创作说明书时，严格遵循以下规范：
- 核心规范与三工作模式（Evidence / Hybrid / Reconstruction）：参见 [SKILL.md](../../SKILL.md)
- 材料清单映射与重构规范：参见 [skill/reconstruction.md](../../skill/reconstruction.md)
- 图像生成与算子：参见 [skill/image-generation.md](../../skill/image-generation.md)
- 执行流程：参见 [skill/workflow.md](../../skill/workflow.md)
- 创作过程呈现规范：参见 [skill/safety.md](../../skill/safety.md)
- 说明书主模板：参见 [templates/competition-statement.md](../../templates/competition-statement.md)

用户仅提供最终作品时自动启动 Reconstruction Mode，缺什么补什么，无占位悬挂，默认输出「完整可提交」文档。启动时询问用户一次「用什么工具生成」，有则记入，无则省略。
