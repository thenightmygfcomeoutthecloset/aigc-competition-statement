# Stage-Aware Prompt Record — 提示词全流程演进记录表

> 本模板用于记录全流程提示词演进、参数适配、输入输出资产与调整因果。
> 权威资产清单直接引用 [skill/reconstruction.md](skill/reconstruction.md)。
> 在 Reconstruction Mode 下，所有字段由系统根据画面解构与比对诊断自动填充，不留空字段；不适用项明确标注为 N/A。

---

## 一、作品基本信息

- **作品名称**：{artwork.title}
- **参赛赛事**：{artwork.competition}
- **技术路径**：{artwork.pipeline}
- **工具环境**：{artwork.tool_environment}

---

## 二、阶段提示词演进记录（Stage-Aware Progression）

<!-- REPEATABLE_PROMPT_STAGE_BLOCK: 遍历各个演进阶段 -->
### 阶段记录：{record.stage_id}（{record.stage_title}）

| 属性项 | 配置与记录详情 | 状态说明 |
|---|---|---|
| **Stage ID** | {record.stage_id} | 阶段标识 |
| **Prompt Version** | {record.prompt_version} (如 Prompt V1 / Prompt V2) | 演进版本 |
| **Input Asset** | {record.input_asset} | 输入素材/垫图 |
| **Positive Prompt** | {record.positive_prompt} | 正向描述词 |
| **Negative Prompt** | {record.negative_prompt}（工具不支持时标为 N/A） | 排除描述词 |
| **Generation Tool** | {record.generation_tool} | 使用工具 |
| **Parameter Profile** | {record.parameter_profile} | 适配参数配置 |
| **Output Asset** | {record.output_asset} | 阶段输出文件 |
| **Adjustment Reason** | {record.adjustment_reason} | 针对演进差距的优化理由 |
| **Next Stage** | {record.next_stage} | 后续流向 |
<!-- END_REPEATABLE_PROMPT_STAGE_BLOCK -->

---

## 三、提示词演进因果逻辑说明

1. **V1 阶段设计逻辑**：基于画面核心主题、空间构图与环境基调生成基础描述词，确立画面骨骼与主色调。
2. **V1 与成图演进差距诊断**：首版生成后比对最终成图，诊断出光影层次、体积光漫射或细部肌理上的演进差距。
3. **V2 针对性深化策略**：根据诊断差距，在 Prompt V2 中精确补充主光源漫射、微晶细节材质，并在工具支持时配置负向排除词，驱动画面收敛至最终品质。
