# 交付验证清单

资产全集必须从 [`schema/canonical-assets.yaml`](../schema/canonical-assets.yaml) 枚举，不在清单中复制文件名。

- [ ] 严格 JSON Schema 与 Pydantic 校验通过。
- [ ] Stage Graph 非空、Stage ID 唯一、资产引用有效。
- [ ] 每轮 Prompt 非空；V2+ 有上一轮 Difference Analysis、Adjustment Reason 与 Prompt Evolution。
- [ ] 每个 generation version 均有真实 request、execution record 和完整结果图，且 backend 不是 OpenCV/filter。
- [ ] generation 数量由停止条件动态决定，Stage Graph 与实际记录数量一致。
- [ ] 每个 Manifest 文件逐项通过 exists、size、decode（图片）和 SHA-256。
- [ ] 每个资产的证据等级符合 Schema。
- [ ] DOCX 媒体与 Schema 中的嵌图资产逐项对应。
- [ ] Prompt Record 和 Parameter Record 已在 DOCX 中实际渲染。
- [ ] 图片等比缩放，图与图注同页，表格列宽明确。
- [ ] LibreOffice 渲染全部页面后，无中文缺字、溢出或空白页。
- [ ] 版权、原创性与原始工具有用户确认来源，或明确标为“未核验”。
