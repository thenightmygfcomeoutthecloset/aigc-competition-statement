# 工作流与失败门禁

资产集合始终读取 [`schema/canonical-assets.yaml`](../schema/canonical-assets.yaml)。

## 模式

- Evidence Mode：只整理可核验的原始文件与记录。
- Hybrid Mode：保留真实材料，仅对缺失环节生成明确标注的复现研究。
- Reconstruction Mode：从最终图和分析 JSON 重建前期输入，并通过真实后端生成当前复现流程的完整版本、记录、Manifest 与 DOCX。

## Reconstruction Mode

运行 `scripts/run_pipeline.py`，不得由测试或调用者手写一份特定作品 Manifest 来替代端到端执行。流水线必须连续完成图像解码、资产处理、Prompt/参数记录、Stage Graph、Manifest、DOCX 与最终验证。

## 强制失败条件

下列任一情况均非零退出：生成后端不可用；空 Manifest/Stage Graph；必填字段缺失；重复 Stage ID；版本不连续；Prompt 缺失或未进入对应 request；V2+ 未引用上一完整版本；execution record 与 Prompt/Parameter/Stage Graph 不一致；使用 OpenCV/filter backend；非法证据等级；路径越界；文件缺失、空白、损坏或 hash 不一致；DOCX 未嵌入全部动态版本。

只有所有门禁通过后才能报告“技术验证通过”。这不等于版权、原创性或参赛资格已经核验。
