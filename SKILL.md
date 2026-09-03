---
name: aigc-competition-statement
description: 为高校赛事整理可审计的 AIGC 完整作品版本演进，生成 Prompt、真实 generation execution records、动态 Stage Graph、Manifest 与 DOCX。适用于有原始过程证据，或从最终图启动明确标注的当前 Reconstruction 工作流；不会把前期素材、滤镜结果或复现材料冒充原始历史证据。
---

# AIGC 竞赛创作说明书

根据材料完整度选择 Evidence、Hybrid 或 Reconstruction Mode。真实材料优先；复现材料统一标记 `[Reconstructed]`，不能写成创作当时的历史记录。

## 必须遵守

- 权威资产定义只读取 [`schema/canonical-assets.yaml`](schema/canonical-assets.yaml)，不得在说明、脚本或模板中复制维护另一份资产清单。
- Reconstruction Mode 必须阅读 [`skill/reconstruction.md`](skill/reconstruction.md)，并通过 `scripts/run_pipeline.py` 生成完整交付包。
- sketch、lineart、color block 只属于前期视觉输入。`generation_v1/v2/...` 必须是同一幅完整作品的连续生成快照，不能代表人物、背景或其他局部。
- 每轮必须先持久化 Prompt 和 Generation Request，再调用 `scripts/image_generation_backend.py` 的真实后端；OpenCV/Pillow 只允许生成前期输入。
- 没有可用生成后端时返回 `generation_backend_unavailable`，交由宿主 Agent 接管；不得用 Final 的模糊、混合、调色或降质结果伪造版本。
- 每轮实际结果必须经过 Difference Analysis 和 Adjustment Reason，下一 Prompt 由上一 Prompt 与真实诊断派生。轮次数由 `should_continue_iteration()` 动态决定并受 Schema 上限约束。
- 版权、原创性与原始创作工具不能从像素确认。只有用户明确确认并记录来源时才写 `[User-reported]`；否则写“未核验”与 `[Unknown]`。
- Manifest 必须通过 `scripts/validate_manifest.py`；缺字段、空 Stage Graph、断链或损坏图片均不得交付。

## 运行

```bash
python scripts/run_pipeline.py \
  --input final.png \
  --output-dir output \
  --title "作品名称" \
  --competition "赛事名称" \
  --analysis-json analysis.json
```

`analysis.json` 至少包含非空的 `subject`、`composition`、`palette` 和 `theme`。用户确认项使用 `confirmations` 记录 `confirmed`、`value` 与 `source`；省略时自动标为未核验。

## 按需读取

- 重构及 fallback 语义：[`skill/reconstruction.md`](skill/reconstruction.md)
- 工作流与失败门禁：[`skill/workflow.md`](skill/workflow.md)
- 真实性和版权边界：[`skill/safety.md`](skill/safety.md)
- DOCX 装配规范：[`skill/output-spec.md`](skill/output-spec.md)
- 模板：[`templates/competition-statement.md`](templates/competition-statement.md)、[`templates/prompt-record.md`](templates/prompt-record.md)、[`templates/evidence-checklist.md`](templates/evidence-checklist.md)
