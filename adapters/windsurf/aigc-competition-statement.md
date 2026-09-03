---
trigger: model_decision
description: 高校 AIGC 竞赛创作说明书技能。单图输入即可逆向造齐全部历史材料（草图、阶段稿、演进Prompt、参数表），自动满足赛事要求，输出无悬挂占位、完整可提交的参赛说明文档；亦支持真实证据整理。
---

# AIGC 竞赛创作说明

处理高校 AIGC 竞赛创作说明书时，严格遵循以下规范：
- 核心规范与三工作模式（Evidence / Hybrid / Reconstruction）：参见 [SKILL.md](../../SKILL.md)
- 逆向材料映射清单与重构规范：参见 [skill/reconstruction.md](../../skill/reconstruction.md)
- 图像生成与算子：参见 [skill/image-generation.md](../../skill/image-generation.md)
- 八阶段执行流程：参见 [skill/workflow.md](../../skill/workflow.md)
- 学术真实性与 IP 自查：参见 [skill/safety.md](../../skill/safety.md)
- 说明书主模板：参见 [templates/competition-statement.md](../../templates/competition-statement.md)

用户仅提供最终作品时自动启动 Reconstruction Mode，缺什么补什么，无占位悬挂，默认输出“完整可提交”文档。所有复现内容严格标记 [Reconstructed]，严禁伪造软件操作历史截屏。
