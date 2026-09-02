# Workflow — 详细阶段执行工作流（三模式驱动版）

> 本文档定义 Agent 执行 AIGC 说明书生成的核心状态机。全仓唯一权威资产清单直接引用 [skill/reconstruction.md](reconstruction.md) 中定义的 `canonical_required_assets`。

---

## 核心三工作模式路由

Agent 接收创作者需求后，根据材料完备度自动分流：

```text
                  用户提交材料
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 [Evidence Mode] [Hybrid Mode] [Reconstruction Mode]
 (原始证据充分)   (部分材料缺失)   (仅有最终作品图或材料严重不足)
```

1. **Evidence Mode（真实证据模式）**：
   - 原始 Prompt、输入素材/草图、参数与截图齐全；
   - 优先使用真实材料直接归档，严禁无故生成替代材料。
2. **Hybrid Mode（混合重构模式）**：
   - 用户提供部分材料（如工具名、口述思路或原始 Prompt，缺少草图或截图）；
   - 遵循 `Verified / User-reported 优先于 Reconstructed`，**仅对确实缺失的环节启动重构**，缺什么补什么。
3. **Reconstruction Mode（逆向重构模式）**：
   - **用户仅提供一张最终 AI 作品图**，或材料严重缺失；
   - **铁律：流程不中断、不逼问用户补齐材料！** 强制读取 [skill/reconstruction.md](reconstruction.md) 与 [skill/image-generation.md](image-generation.md)，全自动逆向造齐全部缺失的过程材料，确保无占位悬挂、文件真实落地。

---

## 八阶段详细执行流程

### Stage 1 — Competition Requirements Profile（解析赛事规则）
1. 在用户工作目录检索或联网查询当前赛事官方规则（如大广赛、新媒体节、学院奖等）。
2. 提取要件：是否要求阶段性过程（截图+文字）、输入垫图、Prompt、参数、以及匿名要求。
3. 若未指定具体赛事或找不到规则，自动加载 **Default Competition Requirements Profile（默认赛事通用规则配置）**：
   ```yaml
   requirements_profile:
     source: default
     profile_status: resolved
     mandatory_elements: [final_artwork, stage_process, visual_evidence, prompts, parameters, tool_matrix, ip_statement]
   ```
   流程继续顺畅执行，不设阻断拦截。

---

### Stage 2 — Canonical Manifest Loading & Missing Assets Checklist（清单映射）
1. **加载规范资产清单**：直接读取 [skill/reconstruction.md](reconstruction.md) 中的 `canonical_required_assets`；
2. **扫描当前输入**：对比用户上传的文件与信息，逐项标记状态（`existing` 或 `missing`）：
   - `final_artwork`（用户原件，`[Verified]`）
   - `reconstructed_sketch`（目标：`01_reconstructed_sketch.png`）
   - `reconstructed_lineart`（目标：`01_reconstructed_lineart.png`）
   - `reconstructed_color_block`（目标：`01_reconstructed_color_block.png`）
   - `generation_v1`（目标：`02_reconstructed_generation_v1.png`）
   - `generation_v2`（目标：`03_reconstructed_generation_v2.png`）
   - `prompt_v1`（阶段一/二提示词）
   - `prompt_v2`（经诊断深化的提示词）
   - `parameter_record`（适配工具的参数配置）
   - `prompt_record`（Stage-Aware 提示词记录表）
   - `stage_process_record`（动态 Stage Graph 数据结构）
   - `statement_docx`（最终 Word 说明书文档）
3. **闭环策略**：针对所有 `missing` 项，在后续阶段逐一调度对应算子生成，**严禁缺少任何一项，全部生成完毕后方可进入 Document Assembly**。

---

### Stage 3 — Final Artwork Multi-Dimensional Analysis（多维画面解构）
对最终作品进行多维度深度解构，输出内部结构化分析报告：
```yaml
artwork_analysis:
  theme: "作品核心立意与题材"
  subject: "画面核心主体形态、动态与空间位置"
  composition: "构图法则（三分法/中心构图/对角线/框架式引导）"
  perspective: "镜头透视与景别（特写/中景/全景；俯视/仰视/平视）"
  depth_planes: "空间层次与景深虚实（前景/中景/远景）"
  palette: "色彩体系（主色、辅助色、强调色、冷暖倾向）"
  lighting: "光影设计（主光源、轮廓光、漫射光、体积光）"
  materials_textures: "核心材质肌理细节"
  visual_style: "艺术风格定位"
  possible_generation_method: "技术路径推断（文生图迭代 / 构图引导图生图 / 分层合成）"
  inferred_creation_tool: "未记录（基于画面特征推断为具备特定渲染能力的图像生成工作流）"
```

---

### Stage 4 — Dynamic Stage Graph Derivation（动态管线构建）
根据 Stage 3 分析结果，构建当前作品专属的 `stage_graph` 数据结构（详见 [skill/reconstruction.md](reconstruction.md) 第四节）：
- 确立各个阶段的 `id`、`title`、`purpose`、`inputs`、`tool`、`prompt`、`parameters`、`outputs` 及 `adjustment`；
- 确保 Canonical Required Assets 在 `stage_graph` 中合理分布并被明确引用。

---

### Stage 5 — Capability Router & Asset Generation（全资产实际生成）

#### 1. 图像资产真实渲染（遵循 Capability Router）
系统按三级优先级调度生图能力，**严禁输出“让用户后续自行生图”的方案**：
- **Priority 1**：宿主原生生图能力（最高质量实出）；
- **Priority 2**：外部图像生成 MCP 工具；
- **Priority 3**：本地确定性兜底脚本：
  ```bash
  python scripts/reconstruct_assets.py --input <final_image_path> --output-dir <output_dir>
  ```
- **文件强校验**：生成的 `01_sketch`、`01_lineart`、`01_color_block`、`02_v1`、`03_v2` 必须均存在且 `filesize > 0`。

#### 2. 自然可信的 Prompt 演进与参数生成
- 生成初稿 V1 提示词（Prompt V1）；
- 比对初稿与成图的真实差距，撰写针对性调整理由（Adjustment Reason）；
- 生成深化提示词（Prompt V2，若工具支持负向词则包含，不支持则省略）；
- 输出工具自适应参数配置（Seed 统一标为未记录，严禁编造假数字）；
- 渲染并保存 `prompt-record.md`（引用 [templates/prompt-record.md](templates/prompt-record.md)）。

---

### Stage 6 — Document Assembly & Build（Word 说明书真实编译）
1. 将 `artwork_analysis`、`stage_graph`、`prompt_record` 及生成的图片路径组装为 `submission_manifest.json`；
2. 调用文档编译引擎（Document Builder）：
   ```bash
   python scripts/build_docx.py --manifest submission_manifest.json --output "{作品名}_{赛事简称}_AIGC说明书.docx"
   ```
3. 引擎自动完成：A4 排版、章节写入、动态阶段渲染、PNG 图片内嵌、学术图注生成、单层汇总表格生成、元数据清空与文件有效性核验。

---

### Stage 7 — Verification & Zero-Placeholder Scan（提交流程自查与占位扫描）
1. **占位符扫描**：运行扫描器确保交付文档无任何残留占位符：
   ```bash
   python scripts/scan_placeholders.py <output_directory>
   ```
2. **构建完整性校验**（引用 [templates/evidence-checklist.md](templates/evidence-checklist.md)）：
   - `required_assets_count == 12`
   - `missing_assets_count == 0`
   - `docx_file_exists == true` 且 `filesize > 0`
   - `placeholder_count == 0`
3. 状态自动确立为：`✅ 过程材料齐备，满足赛事规范，完整可直接提交 (Complete & Ready to Submit)`。

---

### Stage 8 — Packaging & Delivery（交付成果打包）
1. 交付标准目录：
   - 最终作品原件 (`final.png`)
   - 逆向全套过程图片 (`01_sketch.png`, `01_lineart.png`, `01_color_block.png`, `02_v1.png`, `03_v2.png`)
   - 提示词演进记录 (`prompt-record.md`)
   - 提交清单 (`submission_manifest.json`)
   - 最终提交说明书 (`{作品名}_{赛事简称}_AIGC说明书.docx`)
2. 向用户呈现交付报告与各阶段核心成果。
