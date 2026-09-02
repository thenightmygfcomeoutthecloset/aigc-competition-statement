# Reconstruction Mode — 逆向重构模式与权威资产规范 (Single Source of Truth)

> 本文档定义在用户**仅提供一张最终作品**或**过程材料严重缺失**时，全仓唯一的权威资产 Schema（Canonical Required Assets Manifest）、三级图像能力路由（Capability Router）以及动态管线推导标准。
> 全仓所有模块（`workflow.md`、`image-generation.md`、`output-spec.md`、`templates/`、`examples/` 及 `README.md`）均以本文档定义的 Schema 为单一真实来源（Single Source of Truth）。

---

## 一、权威资产规范（Canonical Required Assets Schema）

当进入 Reconstruction Mode 时，系统必须自动将最终作品逆向推演为一套完整的、满足高校赛事（大广赛、新媒体节、学院奖等）要求的材料全集。
全套材料必须全部生成并落地为真实有效的文件，**严禁缺少任何一项，严禁以“外部建议”或“占位符”终结流程**。

```yaml
canonical_required_assets:
  final_artwork:
    id: final_artwork
    type: image
    source: user_provided
    required: true
    evidence_level: "[Verified]"
    description: "用户上传的最终 AI 作品原件"

  reconstructed_sketch:
    id: reconstructed_sketch
    filename: 01_reconstructed_sketch.png
    type: image
    operator: reference_to_sketch
    required: true
    evidence_level: "[Reconstructed]"
    description: "构图草稿/透视骨架图，剥离细节，呈现结构规划"

  reconstructed_lineart:
    id: reconstructed_lineart
    filename: 01_reconstructed_lineart.png
    type: image
    operator: reference_to_lineart
    required: true
    evidence_level: "[Reconstructed]"
    description: "纯净轮廓线稿，作为垫图或 ControlNet 线稿引导素材"

  reconstructed_color_block:
    id: reconstructed_color_block
    filename: 01_reconstructed_color_block.png
    type: image
    operator: reference_to_color_block
    required: true
    evidence_level: "[Reconstructed]"
    description: "色彩大关系稿，大笔刷平涂色块，呈现早期色彩与氛围探索"

  generation_v1:
    id: generation_v1
    filename: 02_reconstructed_generation_v1.png
    type: image
    operator: reference_to_intermediate_generation
    required: true
    evidence_level: "[Reconstructed]"
    description: "阶段初稿 V1，基础具象成型，体现与最终成图的自然演进差距"

  generation_v2:
    id: generation_v2
    filename: 03_reconstructed_generation_v2.png
    type: image
    operator: reference_to_intermediate_generation
    required: true
    evidence_level: "[Reconstructed]"
    description: "迭代深化稿 V2，针对初稿差距针对性优化，贴近最终成品"

  prompt_v1:
    id: prompt_v1
    type: text
    required: true
    evidence_level: "[Reconstructed]"
    description: "阶段初版正向提示词（及环境基调描述）"

  prompt_v2:
    id: prompt_v2
    type: text
    required: true
    evidence_level: "[Reconstructed]"
    description: "经初稿诊断后针对性深化的提示词（含工具支持时的负向词）"

  parameter_record:
    id: parameter_record
    type: structured_table
    required: true
    evidence_level: "[Reconstructed]"
    description: "严格适配当前选用工具的参数配置文件与建议范围（Seed 标为未记录）"

  prompt_record:
    id: prompt_record
    filename: prompt-record.md
    type: document
    template: templates/prompt-record.md
    required: true
    evidence_level: "[Reconstructed]"
    description: "Stage-Aware 提示词全流程演进归档记录表"

  stage_process_record:
    id: stage_process_record
    type: structured_graph
    schema: stage_graph
    required: true
    evidence_level: "[Reconstructed]"
    description: "数据驱动的动态阶段创作记录（Stage Graph）"

  statement_docx:
    id: statement_docx
    filename_pattern: "{作品名称}_{赛事简称}_AIGC说明书.docx"
    type: document
    builder: scripts/build_docx.py
    required: true
    evidence_level: "[Reconstructed]"
    description: "符合学术与排版规范的 Stage-Centric Word 创作说明书完整交付文件"
```

---

## 二、图像生成能力路由（Capability Router）

Reconstruction Mode 的唯一目标是产出**真实存在、非空的文件级视觉资产**。系统按以下三级优先级自动调度图像能力：

```text
               ┌── Priority 1: 宿主原生图像生成/编辑能力 (最高质量生成)
               │
调度决策 ─────┼── Priority 2: 外部挂载图像生成工具 / MCP 能力
               │
               └── Priority 3: 仓库内确定性本地兜底脚本 (scripts/reconstruct_assets.py)
                               (确保文件必定生成、filesize > 0、无悬挂占位)
```

1. **Priority 1（宿主原生图像生成能力）**：
   - 宿主具备生图/修图工具（如 Antigravity `generate_image` 等）时，优先以此作为主生成路径；
   - 依据标准算子提示词，生成高质量的构图草图、线稿、色块大关系稿及中间生成稿（V1/V2）。
2. **Priority 2（外部挂载生图能力）**：
   - 若原生能力不可用，自动调用已挂载的第三方图像生成 MCP 服务。
3. **Priority 3（本地确定性兜底保障，Local Fallback）**：
   - 调用仓库内置脚本：`python scripts/reconstruct_assets.py --input <final_image> --output-dir <dir>`；
   - 基于 OpenCV 与 Pillow 进行确定性图像处理，确保 `01_reconstructed_sketch.png`、`01_reconstructed_lineart.png`、`01_reconstructed_color_block.png`、`02_reconstructed_generation_v1.png`、`03_reconstructed_generation_v2.png` **100% 真实生成在磁盘上**；
   - 所有生成文件经过 `exists + filesize > 0` 强校验；
   - **绝不允许以“请用户去外部工具生成图片”终结流程**。

---

## 三、视觉演进因果链（V1 与 V2 均为必要资产）

在 Canonical Manifest 中，`generation_v1` 与 `generation_v2` 均为必须存在的正式资产。
视觉链的完整演进流为：

```text
最终作品 (final_artwork)
  ↓ 逆向画面分析
构图与输入素材准备 (01_sketch.png / 01_lineart.png / 01_color_block.png)
  ↓ Prompt V1 输入
阶段初稿生成 (02_reconstructed_generation_v1.png)
  ↓ 真实比对初稿与成图的演进差距 (Difference Diagnosis)
针对性优化 Prompt V2 (调整说明 Adjustment Reason)
  ↓ Prompt V2 输入
迭代深化稿生成 (03_reconstructed_generation_v2.png)
  ↓
最终提交成品 (final_artwork)
```

> **拒绝机械缺陷剧本**：初稿与最终图的比对诊断必须基于真实画面的演进距离（如主体结构已建立，但特定边缘轮廓光、发光微晶质感或景深层次在初稿中尚未充分收敛），针对真实差距修改 Prompt V2，确保逻辑自洽可信。

---

## 四、动态 Stage Graph 数据驱动结构

动态管线决定的是**资产在说明书章节中的组织与叙事方式**，而非资产本身是否存在。
内部统一定义 `stage_graph` 数据结构，驱动文档装配：

```yaml
stage_graph:
  - id: stage_1
    title: "阶段一：概念探索与构图规划"
    purpose: "明确画面透视、主体骨骼与构图引导"
    inputs:
      - name: "逆向构图草稿"
        filename: "01_reconstructed_sketch.png"
        evidence_level: "[Reconstructed]"
    tool: "概念构图设计工具"
    tool_type: "设计规划 / 概念手绘"
    prompt: "[Reconstructed Prompt | 复现建议] 构图引导描述"
    parameters: "画幅比例基准 16:9 / 3:4"
    outputs:
      - filename: "01_reconstructed_sketch.png"
        caption: "阶段一概念构思与构图规划草图"
        evidence_level: "[Reconstructed]"
    adjustment: "骨架确立，进入阶段二借助 AI 工具进行具象化生成"
    evidence_level: "[Reconstructed]"

  - id: stage_2
    title: "阶段二：AIGC 基础生成与初稿输出"
    purpose: "实现概念画面的色彩与基础光影具象呈现"
    inputs:
      - name: "阶段一构图草图"
        filename: "01_reconstructed_sketch.png"
    tool: "AI 图像生成模型"
    tool_type: "生成式 AI"
    prompt: "[Reconstructed Prompt | 复现建议] 基础主体与环境基调描述"
    parameters: "采样步数范围 25–35 步 [Reconstructed], CFG 6.5–8.0, Seed 未记录"
    outputs:
      - filename: "02_reconstructed_generation_v1.png"
        caption: "阶段二 AI 基础生成第一版初稿图像"
        evidence_level: "[Reconstructed]"
    adjustment: "比对最终成图，初版主体形态已立，但边缘体积光较弥散，需针对性优化"
    evidence_level: "[Reconstructed]"

  - id: stage_3
    title: "阶段三：Prompt 迭代与视觉深化"
    purpose: "修正初稿演进差距，强化光影细节与特定材质层次"
    inputs:
      - name: "阶段二初版成果"
        filename: "02_reconstructed_generation_v1.png"
    tool: "AI 迭代与优化工具"
    tool_type: "生成式 AI"
    prompt: "[Reconstructed Prompt | 复现建议] 深化光影与高精度材质描述"
    parameters: "建议重绘参数范围 0.55–0.65"
    outputs:
      - filename: "03_reconstructed_generation_v2.png"
        caption: "阶段三多轮提示词优化后的高清渲染成果"
        evidence_level: "[Reconstructed]"
    adjustment: "体积光与材质层次达到预期，完成具象生成"
    evidence_level: "[Reconstructed]"
```

---

## 五、参数适配工具与工具区分规范

1. **参数自适应工具**：
   - 若选用 Midjourney 风格：输出 `--ar`、`--v`、`--stylize`；无负向词项时绝不硬造；
   - 若选用 DALL-E / Flux 风格：输出画幅与质量模式，绝不硬造 Negative Prompt；
   - 若选用 SD / ComfyUI 风格：输出建议采样步数范围、CFG 范围；
   - **Seed 规范**：无物理记录一律注明“未记录（建议随机种子）”，严禁编造具体数字。
2. **工具严格区分**：
   - `原始创作工具`：未记录（基于画面特征推断）
   - `本次复现工具`：宿主生图能力 / 推荐复现平台
   - 绝不得把复现工具混同为原始创作工具。

---

## 六、交付闭环与 Submission Manifest

全流程生成完毕后，自动输出 `submission_manifest.json`，并由 `scripts/build_docx.py` 编译生成 `{作品名}_{赛事简称}_AIGC说明书.docx`。
只有当：
- 所有 Canonical Required Assets 文件均存在且 `filesize > 0`；
- DOCX 成功构建、图片成功嵌入且通过零占位扫描；
- 交付状态直接定为：`✅ 过程材料齐备，满足赛事规范，完整可直接提交`。
