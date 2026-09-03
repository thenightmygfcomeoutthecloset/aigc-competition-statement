# 示例：单图启动与完整创作过程材料生成（Canonical Regression Fixture）

> 创作者仅上传一张最终作品 `final.png`，无原始 Prompt、无草图、无参数。
> Skill 从 `schema/canonical-assets.yaml` 读取资产规范，自动生成完整的创作过程材料、记录、Manifest 与 DOCX。

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

Agent 识别为 Reconstruction Mode，加载机器 Schema，并按其中定义动态建立资产状态表：

| 资产 ID | 规范文件名 / 产物 | 生成方式 | 状态 |
|---|---|---|---|
| `final_artwork` | `final.png` | 用户原件 | ✅ Existing |
| `reconstructed_sketch` | `01_reconstructed_sketch.png` | `reference_to_sketch` | ✅ Generated |
| `reconstructed_lineart` | `01_reconstructed_lineart.png` | `reference_to_lineart` | ✅ Generated |
| `reconstructed_color_block` | `01_reconstructed_color_block.png` | `reference_to_color_block` | ✅ Generated |
| `generation_v1` | 文件名由机器 Schema 读取 | 真实 generation backend | ✅ Generated |
| `generation_v2` | 按实际诊断需要动态出现 | 真实 generation backend | ✅ Generated |
| `generation_request_v1` | Prompt V1 与输入在调用前落盘 | 动态语义解构生成 | ✅ Generated |
| `generation_request_v2` | Prompt V2 与 Prompt Evolution 在第二次调用前落盘 | 基于 V1 实测差异生成 | ✅ Generated |
| `parameter_record` | 工具自适应参数配置表 | 工具自适应参数映射 | ✅ Generated |
| `prompt_record` | `prompt-record.md` | Stage-Aware 提示词记录模板渲染 | ✅ Generated |
| `stage_process_record`| `stage_graph.json` | 动态阶段数据结构构建 | ✅ Generated |
| `statement_docx` | `深林微光_新媒体节_AIGC说明书.docx` | `scripts/build_docx.py` 编译装配 | ✅ Generated |

---

## 三、视觉演进因果链（V1 → 差异诊断 → V2 → Final）

1. **构图与输入底稿**：
   - 生成 `01_reconstructed_sketch.png`（铅笔构图草稿，确立居中框架构图与古树透视）；
   - 生成 `01_reconstructed_lineart.png`（提取神鹿与主树干轮廓线稿，用于线稿约束）；
   - 生成 `01_reconstructed_color_block.png`（提取深蓝与幽绿色彩大关系色块，确定冷色调基调）。
2. **初版生成（Generation V1）**：
   - 先保存 Prompt/Request V1，再执行真实后端并生成完整 Generation V1；
   - **成图实际差距诊断**：神鹿形态与森林大骨骼已建立，但树冠射下的丁达尔光束较为弥散，鹿角发光微粒与青苔绒毛未充分收敛。
3. **二次深化迭代（Generation V2）**：
   - 针对演进差距编写 Prompt V2，强化体积光与微晶质感；
   - 基于 V1 与 Final 的实测差异派生 Prompt V2，再次执行真实后端生成完整 Generation V2；
4. **最终成稿（final.png）**：
   - 达到最终交付品质。

---

## 四、动态 Stage Graph 与数据驱动输出

内部构建的 `stage_graph` 驱动生成 Stage-Centric 结构：
- **阶段一：概念构思与构图规划**（输出：图 1 构图线稿/草图 `01_reconstructed_sketch.png`）
- **阶段二：Generation V1**（完整作品版本）
- **阶段三：Generation V2**（由 V1 实际诊断推动的完整深化版本；仅在需要时出现）

---

## 五、交付验证指标（Verification Status）

- `required_assets_count`: 12 / 12
- `missing_assets_count`: 0
- `broken_asset_paths`: 0
- `empty_generated_files`: 0
- `dangling_placeholders`: 0
- `manifest_completion`: `true`
- **工程状态**：`✅ 文件与结构校验通过`
