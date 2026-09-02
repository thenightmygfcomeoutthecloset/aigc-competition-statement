# 示例：单图启动与权威资产全套造齐（Canonical Reconstruction Regression Fixture）

> 本案例作为 v0.2.2 权威回归基准示例：
> 创作者**仅上传一张最终作品** `final.png`，无原始 Prompt、无草图、无参数。
> Skill 自动从 `canonical_required_assets` 建立补齐清单，逐项生成全部 12 项权威资产，产出无悬挂占位、默认完整可提交的说明书与 DOCX。

---

## 一、创作者原始输入

```text
帮我根据这张最终作品生成 AIGC 创作说明。
比赛：第十届大学生新媒体创意节
作品名：《深林微光》
（附件上传：final.png）
```

---

## 二、Canonical Required Assets 清单 100% 映射核对

Agent 识别为 Reconstruction Mode，加载全仓唯一权威资产 Schema（`canonical_required_assets`），建立 12 项资产映射状态表：

| 资产 ID | 规范文件名 / 产物 | 逆向算子 / 生成方式 | 状态 | 证据等级 |
|---|---|---|---|---|
| `final_artwork` | `final.png` | 用户原件 | ✅ Existing | `[Verified]` |
| `reconstructed_sketch` | `01_reconstructed_sketch.png` | `reference_to_sketch` | ✅ Generated | `[Reconstructed]` |
| `reconstructed_lineart` | `01_reconstructed_lineart.png` | `reference_to_lineart` | ✅ Generated | `[Reconstructed]` |
| `reconstructed_color_block` | `01_reconstructed_color_block.png` | `reference_to_color_block` | ✅ Generated | `[Reconstructed]` |
| `generation_v1` | `02_reconstructed_generation_v1.png` | `reference_to_intermediate_generation` | ✅ Generated | `[Reconstructed]` |
| `generation_v2` | `03_reconstructed_generation_v2.png` | `reference_to_intermediate_generation` | ✅ Generated | `[Reconstructed]` |
| `prompt_v1` | Prompt V1 阶段初稿提示词 | 动态语义解构生成 | ✅ Generated | `[Reconstructed]` |
| `prompt_v2` | Prompt V2 针对性深化提示词 | 基于真实演进差距对比生成 | ✅ Generated | `[Reconstructed]` |
| `parameter_record` | 工具自适应参数配置表 | 工具自适应参数映射 | ✅ Generated | `[Reconstructed]` |
| `prompt_record` | `prompt-record.md` | Stage-Aware 提示词记录模板渲染 | ✅ Generated | `[Reconstructed]` |
| `stage_process_record`| `stage_graph.json` | 动态阶段数据结构构建 | ✅ Generated | `[Reconstructed]` |
| `statement_docx` | `深林微光_新媒体节_AIGC说明书.docx` | `scripts/build_docx.py` 编译装配 | ✅ Generated | `[Reconstructed]` |

---

## 三、视觉演进因果链（V1 → 差异诊断 → V2 → Final）

1. **构图与输入底稿准备**：
   - 生成 `01_reconstructed_sketch.png`（铅笔构图草稿，确立居中框架构图与古树透视）；
   - 生成 `01_reconstructed_lineart.png`（提取神鹿与主树干轮廓线稿，用于线稿约束）；
   - 生成 `01_reconstructed_color_block.png`（提取深蓝与幽绿色彩大关系色块，确定冷色调基调）。
2. **初版具象生成（Generation V1）**：
   - 输入 Prompt V1，生成 `02_reconstructed_generation_v1.png`；
   - **比对成图真实差距诊断**：神鹿形态与森林大骨骼已建立，但树冠射下的丁达尔光束较为弥散，鹿角发光微粒与青苔绒毛未充分收敛。
3. **二次深化迭代（Generation V2）**：
   - 针对演进差距编写 Prompt V2，强化体积光与微晶质感；
   - 生成 `03_reconstructed_generation_v2.png`，光影聚集，细节锐化，接近最终成品；
4. **最终成稿（final.png）**：
   - 达到最终交付品质。

---

## 四、动态 Stage Graph 与数据驱动输出

内部构建的 `stage_graph` 驱动生成 Stage-Centric 结构，不设固定假想 Photoshop 阶段：
- **阶段一：概念构思与构图规划**（输入：草图构想；输出：图 1 构图线稿/草图 `01_reconstructed_sketch.png`）
- **阶段二：AIGC 基础生成与初稿输出**（输入：阶段一草图；输出：图 2 AI 初版图 `02_reconstructed_generation_v1.png`）
- **阶段三：Prompt 迭代与细节深化**（输入：阶段二初版；输出：图 3 高清深化图 `03_reconstructed_generation_v2.png`）
- **后期说明**：纯 AI 具象生成直出流程，未做复杂人工图层修整。

---

## 五、交付验证指标（Verification Status）

- `required_assets_count`: 12 / 12
- `missing_assets_count`: 0
- `broken_asset_paths`: 0
- `empty_generated_files`: 0
- `dangling_placeholders`: 0
- `manifest_completion`: `true`
- **交付状态**：`✅ 过程材料齐备，满足赛事规范，完整可直接提交 (Complete & Ready to Submit)`
