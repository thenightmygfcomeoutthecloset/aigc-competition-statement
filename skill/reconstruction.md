# Reconstruction Mode

## 规范来源

机器可读的 [`schema/canonical-assets.yaml`](../schema/canonical-assets.yaml) 是唯一权威资产定义。需要知道资产 ID、文件名、类型、是否必需、允许的证据等级或 DOCX 嵌入顺序时读取该文件，不在本文复制清单。

## 执行入口

使用 `scripts/run_pipeline.py`，输入最终图、输出目录、标题、赛事与分析 JSON。流水线负责：

1. 解码并规范化最终图；
2. 生成草图、线稿和色块三类前期视觉输入；
3. 在 Prompt/Request 已落盘后调用真实生成后端，产生一个或多个完整 generation versions；
4. 对每个实际版本与 Final 进行差异诊断，派生调整理由和下一轮 Prompt；
5. 从 Execution Records 写入 Prompt Record、Parameter Record 与动态 Stage Graph；
6. 构建严格 Manifest、装配 DOCX并完成文件与渲染验证。

任何门禁失败都必须非零退出，不得以缺图、空记录或悬挂路径交付。

## Reconstruction 的准确语义

`scripts/reconstruct_assets.py` 使用 OpenCV 与 Pillow 处理前期设计输入：

- 它不产生任何 `generation_vN`；
- 不得把 sketch、lineart、color block 重命名为 generation；
- 当前流程新生成的图和记录统一标记 `Artifact Provenance: Current Reconstruction Output`；
- 它们能使文档结构完整，但不证明创作当时已有这些历史文件。

`generation_vN` 只能由真实生成后端产生，并保存 request、execution、difference analysis 和 adjustment reason。

## Prompt 与 Stage Graph

V1/V2 不是固定轮数。根据实际收敛度采用满足说明需要的最少阶段，允许 V1→Final、V1→V2→Final 或继续到 V3/V4；达到 Schema 最大轮数必须停止。

## 真实性

从像素只能分析可见特征，不能确认版权、原创性或原始工具。没有用户确认及来源记录时统一写“未核验”与 `[Unknown]`。详细边界见 [`safety.md`](safety.md)。
