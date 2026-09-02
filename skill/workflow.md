# Workflow — 详细阶段说明

> 本文档是仓库根目录 `SKILL.md` 的展开版本，详细定义 Evidence Mode 与 Reconstruction Mode 下的八阶段执行标准。

---

## 阶段流程全景

```text
Stage 1: Competition Requirements（核对赛事要求）
                 │
Stage 2: Mode Detection & Evidence Collection（模式判定与素材分级）
       ┌─────────┴─────────┐
       ▼                   ▼
 [Evidence Mode]   [Reconstruction Mode]
 (整理已有真实材料)  (仅有成图/材料缺失)
       │                   │
       │                   ├─ Stage 3: Final Artwork Analysis（结构化画面深度分析）
       │                   ├─ Stage 4: Workflow Reconstruction（推导合理创作路径）
       │                   └─ Stage 5: Reverse Asset & Prompt Gen（逆向垫图、阶段结果与演进Prompt）
       └─────────┬─────────┘
                 ▼
Stage 6: Stage-Centric Document Generation（阶段证据链文档生成）
                 │
Stage 7: IP & Submission Compliance Check（版权确认与提交合规审查）
                 │
Stage 8: Export & Packaging（清空元数据并导出 Word）
```

---

## Stage 1 — Competition Requirements（核对赛事要求）

**输入**：比赛名称

**操作**：
1. 在用户工作目录查找 `参赛要求.pdf` / `规则.pdf` / `要求.pdf` / `征稿启事.pdf`
2. 若未找到，联网检索该赛事官方要求
3. 提取关键要素：
   - AIGC 说明文档是否有固定格式、字数或页数限制？
   - 是否明确要求“阶段性创作过程（截图+文字）”、“输入素材（垫图）”、“提示词（Prompts）”、“配置参数”及“工具结果说明”？
   - 是否要求匿名提交（隐去姓名、学号、指导老师、学校）？
   - 提交形式（Word/PDF/压缩包？在线填报？）

**找到规则时**：进入 Competition-specific mode，按具体规则配置章节与要求。
**未找到规则时**：进入 Generic Draft Mode，使用通用模板继续生成，文档顶部加入未校验警示。

---

## Stage 2 — Mode Detection & Evidence Collection（模式判定与素材分级）

**输入**：用户上传或提供的所有材料

**操作**：
1. **自动模式识别**：
   - 若用户仅上传了最终作品图（或明确表示没有原始过程记录）→ 进入 **Reconstruction Mode**（逆向重构模式）。
   - 若用户提供了原始 Prompt、输入垫图、工作流截图、参数等完整记录 → 进入 **Evidence Mode**（真实证据模式）。
   - 若材料部分缺失 → 进入 **Hybrid Mode**（已有材料保留真实证据，缺失环节逆向重构）。
2. **输入素材分类归档**：
   为所有输入素材分配严格数据属性与 Evidence Level：
   - `user-provided input`：用户上传的原始文件/素材（[Verified]）
   - `original reference`：创作者明确使用的参考素材（[Verified] / [User-reported]）
   - `original sketch`：创作者原创手绘线稿/草图（[Verified]）
   - `reconstructed sketch`：系统逆向推导的构图/线稿草图（[Reconstructed]）
   - `reconstructed reference`：系统逆向推导的风格/色彩参考图（[Reconstructed]）
   - `previous-stage output`：上一生成阶段输出的中间结果（[Reconstructed] 或 [Verified]）
3. 尝试从 PNG 元数据提取内嵌 Workflow / Prompt（如为 ComfyUI/SD 导出图）。

---

## Stage 3 — Final Artwork Analysis（最终作品结构化分析）

> **仅在 Reconstruction Mode 或需要画面反推时深入执行。**

**输入**：用户最终作品图（必须已收到）

**操作**：
全面拆解画面视觉与技术特征，生成内部标准结构：

```yaml
artwork_analysis:
  theme: "作品主题与立意"
  subject: "主体形态、动态、特征"
  composition: "构图方式（三分法/中心构图/对角线/向心式）"
  perspective: "镜头视角与景别（俯视/仰视/平视；特写/中景/远景）"
  depth_planes: "空间纵深（前中后景分布及虚实关系）"
  palette: "色彩体系（主色、辅助色、强调色、明度与纯度分布）"
  lighting: "光影设计（主光源、环境光、边缘轮廓光、阴影过渡）"
  materials_textures: "主要材质细节（金属/皮质/布料/水汽/毛发/手绘质感）"
  visual_style: "风格定位（概念设计/3D渲染/国风插画/赛博朋克/超写实）"
  atmosphere: "整体氛围与情绪"
  text_ui_elements: "文字排版、Logo、图层修饰等人工后期痕迹"
  possible_generation_method: "技术路径推断（如文生图迭代、垫图图生图、分层拼贴）"
  possible_input_assets: "逆向合理的垫图类型（如铅笔构图草稿、黑白线稿、色块大关系）"
```

---

## Stage 4 — Workflow Reconstruction（创作流程推导）

**操作**：根据 Stage 3 分析结果，量身推导一条合乎逻辑、有说服力的创作管线，严禁套用千篇一律模板：

- **管线 1（线稿草图约束型）**：适合人物造型严谨、国风插画、构图精细的作品。
  `手绘构图草图 → 线稿控制图生图 (初稿V1) → 提示词与光影优化 (二轮V2) → PS精修与文字排版`
- **管线 2（概念探索与多轮迭代型）**：适合宏大场景、概念场景设计、氛围主导的作品。
  `立意词发散 → 文生图粗胚生成 (初稿V1) → 负向词排除与材质深化 (二轮V2) → 局部重绘与后期合成`
- **管线 3（多主体分层合成型）**：适合复杂海报、视觉传达、商业展示作品。
  `背景生成 → 核心主体生成 → 素材分层扣取 → PS全局调色与图层排版`

---

## Stage 5 — Reverse Asset & Prompt Generation（逆向资产与演进 Prompt）

> 详见 [skill/reconstruction.md](reconstruction.md)。

**操作**：
1. **逆向生成复现垫图（Capability-Based）**：
   - 依赖宿主 Agent 可用的图像生成/编辑能力（如 `generate_image`），调用相应算子：
     `reference_to_sketch`（铅笔草图）、`reference_to_lineart`（轮廓线稿）、`reference_to_composition_draft`（构图块面）、`reference_to_color_block`（色彩大关系）、`reference_to_grayscale_study`（灰度光影稿）。
   - **铁律**：生成的垫图必须比最终作品更早、更粗糙、更简化，严禁生成高保真最终图复制品！全部标记 `[Reconstructed]`。
   - *环境降级*：若当前环境无图像生成工具，自动输出精确的垫图规格定义与提示词，指导用户按需生成。
2. **构建阶段性视觉链**：
   生成 `01_reconstructed_sketch` → `02_reconstructed_input` → `03_reconstructed_v1` → `04_reconstructed_v2` → `05_final_artwork`。
3. **阶段性 Prompt 演进设计**：
   - **Prompt V1**：确立主体与基本风格；
   - **Prompt V2**：强化光影与材质，解决 V1 视觉缺陷；
   - **Prompt V3**：加入负向提示词排除杂乱瑕疵，完成最终细节。
   - 必须注明每次调整的明确理由，且严格标为 `Reconstructed Prompt`。
4. **生成推荐复现参数**：
   - 给出用于复现的推荐模式、步数范围、CFG 范围、重绘幅度等；
   - 严禁虚构真实 Seed！

---

## Stage 6 — Stage-Centric Document Generation（阶段证据链文档生成）

不再机械按“截图类型”罗列，而是以 **创作阶段** 为核心骨架，建立完整的闭环证据链：

`Input（输入素材）→ Tool（工具）→ Prompt（提示词）→ Parameters（参数）→ Output（工具结果）→ Adjustment（调整说明）`

**文档标准七大章节**：
- **一、作品基本信息**（作品名、类型、主题、AIGC技术类型）
- **二、创作构思**（选题立意、视觉思路、设计目标、AI使用目的）
- **三、阶段性创作过程**（核心证据链：阶段1概念构思 → 阶段2初步生成 → 阶段3迭代优化 → 阶段4后期整合，每阶段均配齐输入、Prompt、参数、结果与图注）
- **四、AIGC 工具使用说明**（AI 负责环节 vs 人工负责环节）
- **五、Prompt、输入素材与参数汇总表**（全流程对照大表）
- **六、版权、素材来源与原创性说明**（素材版权合法性与原创承诺）
- **七、复现材料说明**（明确告知 Reconstructed 材料的逆向推导性质）

---

## Stage 7 — IP & Submission Compliance Check（版权与提交合规审查）

**输入**：Stage 6 生成的说明文档

**操作 1：版权与知识产权审查（IP Check）**
逐项排查是否存在版权争议风险：
- 是否使用第三方图片、网络实拍图、知名商业 Logo、非开源商用字体、知名动漫/影视角色 IP、未授权专有模型/LoRA？
- 若用户无法提供版权证明，文档中**严禁擅自声称“绝对无版权纠纷”**，统一标注为 `Requires User Confirmation（需创作者在提交前确认授权）`。

**操作 2：提交流程完整度审查（Submission Check）**
逐项比对比赛硬性要求是否齐备：
- [x] 最终作品已包含
- [x] 阶段性过程有清晰图文
- [x] 包含各环节工具生成结果
- [x] 提示词完整记录（真实或复现）
- [x] 输入素材/垫图已说明（真实或逆向）
- [x] 参数已如实记录或注明复现建议
- [x] AI 与人工职责分工明确
- [x] 版权状态已确认或提示确认
- [x] Reconstructed 内容已规范标识，附有复现说明
- [x] 匿名检查（正文及 Word 属性中无个人学校隐私）

> **红线原则**：若赛事强制要求的核心材料（如 Prompt 或阶段图）依然空白且未完成重构，**严禁显示“完全合规”**，必须明确标注 `Required Evidence Missing` 并提示用户。

---

## Stage 8 — Export & Packaging（清空元数据并导出 Word）

**操作**：
1. 导出规范 Word 文件：`{作品名}_{赛事简称}_AIGC说明书.docx`
2. 清空 Word 核心元数据（作者、公司、修改人、修订批注等）
3. 遵循 [skill/output-spec.md](output-spec.md) 页面与排版样式（禁止代码框底色、无蓝字超链接、单层清爽表格、标准图注）
4. 输出最终成果与复检提示清单给用户。
