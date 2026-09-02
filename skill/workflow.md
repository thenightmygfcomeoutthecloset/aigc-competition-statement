# Workflow — 详细阶段说明（三模式驱动版）

> 本文档详细定义在 **Evidence Mode**、**Hybrid Mode** 与 **Reconstruction Mode** 下的完整执行标准。

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
   - **铁律：流程不中断、不逼问用户补齐材料！** 强制读取 [skill/reconstruction.md](reconstruction.md) 与 [skill/image-generation.md](image-generation.md)，全自动逆向造齐全部缺失的过程材料（草图垫图、中间初稿、演进Prompt、参数表），输出无占位悬挂、完整可直接提交的全套文档。

---

## 八阶段执行全流程

### Stage 1 — Competition Requirements（核对赛事要求）
1. 在用户工作目录查找或联网检索当前赛事官方规则（如大广赛、新媒体节、学院奖）。
2. 提取要件：是否要求阶段性创作过程（截图+文字）、输入垫图、Prompt、参数、以及匿名要求。
3. 找不到官方规则时自动进入 Generic Draft Mode，保留未校验警示并继续执行，不阻断流程。

---

### Stage 2 — Mode Routing & Missing Assets Checklist（模式判定与缺失清单建立）
1. 扫描输入材料，自动确立模式（Evidence / Hybrid / Reconstruction）。
2. 在 Reconstruction Mode 下，自动将赛事材料要求映射为**待补齐的逆向材料清单**：
   - 构图草图 / 早期骨架（目标：`01_reconstructed_sketch.png`）
   - 阶段初稿（目标：`02_reconstructed_generation_v1.png`）
   - 演进提示词（目标：Prompt V1 / V2）
   - 工具自适应参数（目标：画幅比例、步数/CFG/质量模式建议）
   - 过程说明书与汇总表（目标：Stage-Centric 完整文档）

---

### Stage 3 — Final Artwork Analysis（最终作品多维深度解构）
对最终作品进行多维度深度解构，输出内部标准结构：
```yaml
artwork_analysis:
  theme: "作品核心立意与题材"
  subject: "画面核心主体形态、动态与空间位置"
  composition: "构图方式（三分法/中心构图/对角线/向心聚焦）"
  perspective: "镜头透视与景别（特写/中景/全景；俯视/仰视/平视）"
  depth_planes: "空间层次与景深虚实（前景/中景/远景）"
  palette: "色彩体系（主色、辅助色、强调色、明暗色温）"
  lighting: "光影设计（主光、轮廓光、体积光、阴影过渡）"
  materials_textures: "核心材质肌理细节"
  visual_style: "艺术风格定位"
  possible_generation_method: "技术路径推断（文生图迭代 / 构图垫图图生图 / 分层合成）"
  possible_input_assets: "合理的早期垫图类型（铅笔构图草稿、轮廓线稿、色彩大关系色块图）"
```

---

### Stage 4 — Dynamic Stage Graph Derivation（动态管线推导）
根据 Stage 3 分析结果，**动态生成 Stage Graph**，做到 Minimal but Sufficient，严禁套用死板固定格式：
- **文生图概念迭代管线**：`色彩氛围探索 → 基础具象生成 (V1) → 提示词深化迭代 (V2) → 最终成品`
- **线稿约束图生图管线**：`构图线稿规划 → 线稿引导初稿 (V1) → 光影细节深化 (V2) → 最终成稿`
- **分层多元素合成管线**：`背景基调生成 → 核心主体生成 → 要素统筹整合`

---

### Stage 5 — Asset & Prompt Reverse Generation（资产与演进 Prompt 逆向生成）

#### 1. 图像过程材料真实生成（遵循 [skill/image-generation.md](image-generation.md)）
- 宿主具备生图能力时：实际调用相应算子（`reference_to_sketch`、`reference_to_intermediate_generation` 等）生成图片文件，保存在项目目录并在文档中真实嵌入。
  - 草图垫图必须粗糙简化，体现早期探索；
  - 阶段中间稿体现真实的阶段演进感，严禁生成伪造的软件界面截屏（如假的 PS 图层面板、假的 ComfyUI 截图）。
- 宿主缺少生图能力时：输出高精度生图 Prompt 与技术规格，在文档中以规范说明自然过渡，杜绝突兀悬挂，交付完整自洽文本。

#### 2. 自然可信的 Prompt 演进因果
拒绝刻板缺陷剧本。采用真实比对：
`生成 V1 → 视觉检查 → 与最终成图对比 → 诊断实际存在的具体演进差距 → 针对性改写 Prompt/参数 → 生成 V2`。
所有演进 Prompt 统一标为 `[Reconstructed Prompt | 复现建议]`。

#### 3. 工具自适应参数与工具区分
- 参数严格匹配所选用工具的实际支持范围（MJ 输出 `--ar`、`--v`、`--stylize`；DALL-E/Flux 输出画幅与质量模式且不硬加负向词；SD 输出步数与 CFG 范围；Seed 统一标为未记录）；
- 严格区分：
  - `原始创作工具`：未记录（基于画面特征推断为生成式图像工作流）
  - `本次复现工具`：宿主环境图像能力 / 推荐复现平台
  - 严禁将复现工具冒充为创作者当时的原始历史工具。

---

### Stage 6 — Stage-Centric Document Assembly（无悬挂完整文档装配）
按创作阶段装配七大标准章节，**全文字段充实闭环，绝不留下“待补齐”、“待确认”等阻断性占位**：
- **一、作品基本信息**（区分原始创作推断与复现工具）
- **二、创作构思**（选题立意、视觉思路、设计目标、协同目的）
- **三、阶段性创作过程**（核心证据链：`Input → Tool → Prompt → Parameters → Output → Adjustment`）
  - **条件性后期输出**：有真实后期证据才输出后期阶段并标为 Verified/User-reported；无后期证据则如实说明纯 AI 直出，**严禁强加 Photoshop 图层操作与假截图**。
- **四、AIGC 工具使用说明与人机协同分工**
- **五、全流程 Prompt、输入素材与参数汇总表**（单层完整对照大表）
- **六、版权、素材来源与原创性说明**（自主承诺合规，完成知识产权自查）
- **七、复现材料特别说明**（声明复现材料用于完整展示创作演进逻辑）

---

### Stage 7 — Submission Check & Metadata Sanitization（提交检查与元数据清空）
1. 检查各要件是否齐备闭环（最终图、阶段草图、初稿图、演进Prompt、参数表、人机分工、版权声明与免责声明）。
2. 确认文档状态默认输出为：
   `✅ 过程材料齐备，满足赛事规范，完整可直接提交`。
3. 清空 Word 核心元数据（作者、公司、修改人）。

---

### Stage 8 — Export & Delivery（导出与完整包交付）
1. 导出规范 Word 文档：`{作品名}_{赛事简称}_AIGC说明书.docx`；
2. 连同生成的阶段图与最终成图打包为提交包；
3. 输出完整交付提示。
