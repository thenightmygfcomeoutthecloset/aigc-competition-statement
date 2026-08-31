---
trigger: model_decision
description: 整理高校 AIGC 竞赛创作说明、AI 使用声明和过程证明材料。
---

# AIGC 竞赛创作说明

先读取用户提供的赛事规则、最终作品、截图和元数据。将信息分为：

- `[Verified]`：材料直接证明。
- `[User-reported]`：用户口头说明，使用引述语气。
- `[Reconstructed]`：由成品推断，明确标为复现建议。
- `[Unknown]`：留空或写“未记录”。

不得擅自填写 Seed、Steps、CFG、Sampler、模型精确版本、LoRA 权重、原始 Prompt、日期或生成次数。找不到官方规则时继续生成通用草稿，但必须写明尚未校验。生成 Word 前检查匿名、真实性、图片图注和元数据。
