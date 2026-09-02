# Evidence Checklist — 交付构建完整性工程核查表 (Build Verification)

> 本清单由系统在 Stage 7 执行工程级自动构建核查，直接依据 [skill/reconstruction.md](skill/reconstruction.md) 的 Canonical Required Assets Schema 验证交付包完整性。

---

## 一、权威资产构建核验（Canonical Assets Verification）

- [ ] **最终作品存在性**：`final_artwork` 存在且 `filesize > 0`
- [ ] **构图草图存在性**：`01_reconstructed_sketch.png` 存在且 `filesize > 0`
- [ ] **轮廓线稿存在性**：`01_reconstructed_lineart.png` 存在且 `filesize > 0`
- [ ] **色彩大关系稿存在性**：`01_reconstructed_color_block.png` 存在且 `filesize > 0`
- [ ] **阶段初稿 V1 存在性**：`02_reconstructed_generation_v1.png` 存在且 `filesize > 0`
- [ ] **迭代深化稿 V2 存在性**：`03_reconstructed_generation_v2.png` 存在且 `filesize > 0`
- [ ] **演进 Prompt V1 存在性**：Prompt V1 正向词已生成且非空
- [ ] **演进 Prompt V2 存在性**：Prompt V2 经诊断深化且非空（与 V1 差异明显）
- [ ] **参数配置表存在性**：工具自适应参数已生成且无捏造数值（Seed 标为未记录）
- [ ] **提示词记录表存在性**：`prompt-record.md` 真实渲染且无空字段
- [ ] **动态阶段管线完整性**：`stage_graph` 数据结构闭环无死循环
- [ ] **Word 说明书构建存在性**：`{作品名}_{赛事简称}_AIGC说明书.docx` 存在且 `filesize > 0`

---

## 二、文档构建与占位符扫描校验

- [ ] **DOCX 图片真实嵌入**：DOCX 文档内至少成功嵌入 3 张以上实际视觉成果图片
- [ ] **学术图注与章节排版**：标题、正文、表格及图注格式符合排版规范
- [ ] **零占位悬挂核查**：运行 `scripts/scan_placeholders.py` 确保全文占位符数量 `placeholder_count == 0`
- [ ] **元数据清理核查**：Word 核心元数据（作者、公司、修改人）已彻底清空

---

## 三、工程构建完成判定（Manifest Completion）

```text
IF required_assets_missing == 0
   AND broken_asset_paths == 0
   AND empty_generated_files == 0
   AND placeholder_count == 0
   AND docx_validation_passed == true:
       manifest.completion = true
       status = "✅ 材料齐备，完整可提交 (Complete & Ready to Submit)"
ELSE:
       manifest.completion = false
       status = "❌ 构建失败，需触发重试或本地兜底"
```
