---
name: aigc-competition-statement
description: 为高校赛事生成完整的 AIGC 作品创作过程说明，输出 Prompt、generation execution records、动态 Stage Graph、Manifest 与 DOCX。支持从最终图启动，自动补齐构图草图、轮廓线稿、色块稿与完整作品的连续版本演进，交付一份完整、自洽、可直接提交的创作说明文档。
---

# AIGC 竞赛创作说明书

根据材料完整度选择 Evidence、Hybrid 或 Reconstruction Mode。已有材料优先使用，缺失的创作过程环节自动补齐，交付一份完整、自洽、可直接提交的创作说明。

## 必须遵守

- 权威资产定义只读取 [`schema/canonical-assets.yaml`](schema/canonical-assets.yaml)，不得在说明、脚本或模板中复制维护另一份资产清单。
- Reconstruction Mode 必须阅读 [`skill/reconstruction.md`](skill/reconstruction.md)，并通过 `scripts/run_pipeline.py` 生成完整交付包。
- sketch、lineart、color block 属于前期视觉设计。`generation_v1/v2/...` 必须是同一幅完整作品的连续版本，不能代表人物、背景或其他局部。
- 每轮必须先持久化 Prompt 和 Generation Request，再调用 `scripts/image_generation_backend.py` 的真实后端；OpenCV/Pillow 只用于生成前期视觉设计。
- 没有可用生成后端时返回 `generation_backend_unavailable`，交由宿主 Agent 接管；不得用 Final 的模糊、混合、调色或降质结果伪造版本。
- 每轮实际结果必须经过 Difference Analysis 和 Adjustment Reason，下一 Prompt 由上一 Prompt 与真实诊断派生。轮次数由 `should_continue_iteration()` 动态决定并受 Schema 上限约束。
- Manifest 必须通过 `scripts/validate_manifest.py`；缺字段、空 Stage Graph、断链或损坏图片均不得交付。

## 开始前询问（一次性）

启动前询问用户一次：**「你使用什么工具生成的这幅作品？」**。用户提供了就记入 `analysis.json` 的 `confirmations.original_tool`（`confirmed: true`、`value` 与 `source`）；未提供则跳过，不再追问。

## 运行

```bash
python scripts/run_pipeline.py \
  --input final.png \
  --output-dir output \
  --title "作品名称" \
  --competition "赛事名称" \
  --analysis-json analysis.json
```

`analysis.json` 至少包含非空的 `subject`、`composition`、`palette` 和 `theme`。用户确认的创作工具使用 `confirmations.original_tool` 记录 `confirmed`、`value` 与 `source`。

## 按需读取

- 重构及 fallback 语义：[`skill/reconstruction.md`](skill/reconstruction.md)
- 工作流与失败门禁：[`skill/workflow.md`](skill/workflow.md)
- 创作过程呈现规范：[`skill/safety.md`](skill/safety.md)
- DOCX 装配规范：[`skill/output-spec.md`](skill/output-spec.md)
- 模板：[`templates/competition-statement.md`](templates/competition-statement.md)、[`templates/prompt-record.md`](templates/prompt-record.md)、[`templates/evidence-checklist.md`](templates/evidence-checklist.md)
