# DOCX 输出规范

`scripts/build_docx.py` 从严格 Manifest 与 [`schema/canonical-assets.yaml`](../schema/canonical-assets.yaml) 装配 A4 DOCX。

## 数据与媒体

- Stage Graph 必须动态渲染，不能依赖某个示例作品。
- Schema 中 `embed_in_docx: true` 的图片必须逐项、且恰好一次嵌入；缺失或损坏立即失败。
- Prompt Record 按 Execution Records 动态展示 V1…Vn，以及 keep/modify/add/reduce/reason。
- Parameter Record 按版本展示真实 backend、model、mode 和实际请求参数。
- 每个 generation section 展示输入、Prompt、工具、参数、完整结果图、实际差异与修改原因；轮数不得写死。
- 用户确认的创作工具渲染在第七章「创作工具说明」；未提供时省略该章。

## 版式

- A4 纵向，页边距和内容宽度显式设置。
- 中文字体统一使用随包提供的 Noto Sans SC。
- 图片按页面可用宽度与高度共同约束，保持原始宽高比。
- 图片段落设置 `keepNext`，图注设置 `keepLines`，避免图与图注跨页。
- 所有表格关闭自动适配，并显式写入 `tblW`、`tblGrid` 和每个 `tcW`。

## 验证

构建后比较 DOCX `word/media` 与 Schema 图片的 SHA-256 集合。存在 LibreOffice 时运行 `scripts/render_docx.py` 渲染全部页面，并检查页面非空和内容不触边；CI 应安装 LibreOffice 以启用完整回归门禁。
