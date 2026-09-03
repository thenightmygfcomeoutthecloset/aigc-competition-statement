# Prompt Record 模板

资产 ID 与文件名读取 [`schema/canonical-assets.yaml`](../schema/canonical-assets.yaml)。

对 `generation_records` 动态循环，每轮渲染：版本、Prompt、source record、KEEP、MODIFY、ADD、REDUCE、REASON。

V2+ 必须引用上一轮 Difference Analysis 和 Adjustment Reason。Reconstruction Prompt 不得表述为原作历史 Prompt。
