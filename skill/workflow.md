# Workflow — 详细阶段说明（模式驱动版）

> 本文档详细定义在 **Evidence Mode**、**Hybrid Mode** 与 **Reconstruction Mode** 下的执行逻辑。

---

## 核心模式路由驱动（Mode-Driven Architecture）

Agent 在收到用户需求后，必须首先依据材料的完备度确立工作模式：

```text
                  用户提交材料
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 [Evidence Mode] [Hybrid Mode] [Reconstruction Mode]
 (原始证据充分)   (部分材料缺失)   (仅有最终作品图或材料严重不足)
```

### 1. Evidence Mode（真实证据模式）
- **触发条件**：创作者提供了真实的原始 Prompt、输入素材/草图、生成参数、工作流截图或软件工程截图。
- **执行准则**：优先使用真实材料；客观整理与分级，**绝不生成任何非必要的替代性复现材料**。

### 2. Hybrid Mode（混合重构模式）
- **触发条件**：创作者提供了部分真实材料（例如：告知了工具和创意想法，甚至有原始 Prompt，但没有保存草图垫图与中间过程截图）。
- **执行准则**：
  - `Verified / User-reported` 材料永远优先于 `Reconstructed`；
  - **仅对确实缺失的环节启动逆向重构**；
  - 严禁用复现材料覆盖或替换已有的真实证据。

### 3. Reconstruction Mode（逆向重构模式）
- **触发条件**：**创作者仅上传了一张最终 AI 作品图**，或明确告知未保存任何过程材料。
- **执行铁律**：
  - **只有最终图片时，严禁停止流程，严禁强行要求用户先补齐历史材料！**
  - **自动进入 Reconstruction Mode，必须阅读并严格遵循 [skill/reconstruction.md](reconstruction.md) 与 [skill/image-generation.md](image-generation.md)**；
  - 自动完成：画面分析 → 管线推导 → 逆向垫图与阶段图实际渲染 → 演进 Prompt 重构 → 建议参数推算 → Stage-Centric 文档生成 → DOCX 交付。

---

## 详细八阶段执行标准

### Stage 1 — Competition Requirements（核对赛事要求）
1. 检索用户工作目录下的赛事要求文件，或联网检索官方规则。
2. 提取要件：是否必须提供阶段性过程（截图+文字）、输入垫图、Prompt、参数、以及匿名要求。
3. 找不到官方规则时自动进入 Generic Draft Mode，保留未校验警示并继续执行，不阻断流程。

---

### Stage 2 — Evidence Collection & Mode Routing（模式判定与素材分级）
1. 扫描输入材料，自动判定进入 **Evidence Mode**、**Hybrid Mode** 还是 **Reconstruction Mode**。
2. 对所有信息与素材严格定级：
   - `user-provided input`（用户原件，[Verified]）
   - `original sketch`（原创草图，[Verified]）
   - `original reference`（参考图，[Verified] / [User-reported]）
   - `reconstructed sketch`（系统逆向构图稿，[Reconstructed]）
   - `reconstructed reference`（系统逆向色块/氛围稿，[Reconstructed]）
   - `previous-stage output`（上一阶段生成的中间稿，[Reconstructed] 或 [Verified]）

---

### Stage 3 — Final Artwork Analysis（最终作品结构化分析）
> Reconstruction Mode 与 Hybrid Mode 必走步骤。

对最终作品进行多维度深度解构，生成内部标准结构：
```yaml
artwork_analysis:
  theme: "作品核心立意与题材"
  subject: "画面主体形态、动态与空间位置"
  composition: "构图方式（三分法/中心构图/对角线/向心聚焦）"
  perspective: "镜头透视与景别（特写/中景/全景；俯视/仰视/平视）"
  depth_planes: "空间层次与景深虚实（前景/中景/远景）"
  palette: "色彩体系（主色、辅助色、强调色、明暗色温）"
  lighting: "光影设计（主光、轮廓光、体积光、阴影过渡）"
  materials_textures: "核心材质细节（金属、毛发、布料、微晶、流体等）"
  visual_style: "艺术风格定位"
  possible_generation_method: "技术路径推断（草图引导图生图 / 概念文生图迭代 / 多主体分层合成）"
  possible_input_assets: "合理的早期垫图类型（如铅笔构图草图、色彩大关系色块稿、轮廓线稿）"
```

---

### Stage 4 — Workflow Reconstruction（创作管线动态推导）
根据 Stage 3 分析结果，量身推导最适合该画面的合理管线，**严禁千篇一律套用死板模板**：
- **构图约束型**：`构图草图 → 线稿控制基础生图 (V1) → 光影优化 (V2) → 局部修整`
- **概念探索型**：`创意发散 → 文生图粗胚 (V1) → 负向剔除与材质深化 (V2) → 最终出图`
- **分层合成型**：`背景渲染 → 主体独立生成 → 元素合成拼贴 → 最终调整`

---

### Stage 5 — Reverse Assets & Prompt Generation（逆向资产与演进 Prompt 生成）

#### 1. 过程图像实际生成（遵循 [skill/image-generation.md](image-generation.md)）
- **有生图能力**：实际调用宿主生图工具，生成 `01_reconstructed_sketch.png`、`02_reconstructed_v1.png` 等文件，保存在项目目录中并在文档中真实嵌入。
  - 逆向垫图必须更早、更粗糙、更简化；
  - 阶段图必须包含合理的阶段性小瑕疵；
  - 严禁生成伪造的软件界面截图（如假的 PS 图层面板、假的 ComfyUI 截图）。
- **无生图能力（Fallback）**：输出精细生图指令，在文档中留出明确占位标注，严禁凭空写假路径欺骗用户，并在 Stage 7 标记 `Required Visual Evidence Missing`。

#### 2. Prompt 演进因果链构建
必须呈现演进逻辑与修改原因：
`Prompt V1 → Output V1（发现光影平淡/背景空洞）→ 调整原因 → Prompt V2 → Output V2（细节丰富）`。
全部标为 `[Reconstructed Prompt | 复现建议]`，严禁声称为原始 Prompt。

#### 3. 建议复现参数
提供适配该画面的建议参数范围（如建议步数 25–35 步 [Reconstructed]），Seed 必须标为“未记录（建议随机）”，严禁虚构具体数值。

---

### Stage 6 — Stage-Centric Document Generation（阶段证据链文档生成）

以 **创作阶段** 为核心单元组织七大标准章节：
- **一、作品基本信息**
- **二、创作构思**
- **三、阶段性创作过程**（核心证据链：`Input → Tool → Prompt → Parameters → Output → Adjustment`）
  - **重要原则：人工后期精修阶段必须条件性输出**：
    - IF 用户提供了真实后期材料 → 输出后期阶段，标记 `[Verified]`；
    - ELSE IF 用户口述进行过后期处理 → 输出该阶段，标记 `[User-reported]`；
    - ELSE → **绝不得声称使用了 Photoshop，绝不得伪造 PS 截图**，如实说明“本作为 AI 具象生成直出，未进行复杂人工图层修整”或直接省略该阶段。
  - **重要原则：参数表严禁默认写死具体数值**，未记录的一律写“建议复现范围”或“未记录”。
- **四、AIGC 工具使用说明与人机协同分工**
- **五、全流程 Prompt、输入素材与参数汇总表**
- **六、版权、素材来源与原创性说明**
- **七、复现材料特别说明**（存在 Reconstructed 时必带）

---

### Stage 7 — IP & Submission Compliance Check（版权与提交合规审查）
1. **版权自查（IP Check）**：排查第三方图片、Logo、未授权商用字体与角色 IP，未确认时客观标注 `Requires User Confirmation`。
2. **提交流程核查（Submission Check）**：
   - 若宿主无图像能力导致过程图未实际渲染，标记 `⚠️ Required Visual Evidence Missing`；
   - 若赛事强制要件空白且未重构，标记 `❌ Required Evidence Missing`；
   - 严禁在缺失要件时盲目显示“全部通过”。
3. **匿名检查**：清空正文及 Word 核心元数据中的个人和学校信息。

---

### Stage 8 — Export & Packaging（清空元数据并导出 Word）
1. 导出排版规范的 `{作品名}_{赛事简称}_AIGC说明书.docx`；
2. 清空 Word 核心元数据；
3. 给出交付成果与后续确认提示。
