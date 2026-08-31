# Workflow — 详细阶段说明

> 本文档是 skill/SKILL.md 中流程概览的展开版本。

---

## Stage 1 — Competition Requirements（核对赛事要求）

**输入**：比赛名称

**操作**：
1. 在用户工作目录查找 `参赛要求.pdf` / `规则.pdf` / `要求.pdf` / `征稿启事.pdf`
2. 若未找到，联网搜索该赛事最新官方要求
3. 提取关键信息：
   - AIGC 作品是否需要单独提交创作说明？
   - 说明文档是否有格式、字数或页数限制？
   - 是否需要匿名提交（不得出现姓名、学校等）？
   - 提交形式（压缩包？在线上传？）
   - AIGC 参与度是否需要标注？

**不允许**：
- 假设赛事要求
- 未找到要求时继续生成文档（必须告知用户）

**输出**：赛事要求摘要，供后续所有阶段参考

---

## Stage 2 — Evidence Collection（素材收集与分级）

**输入**：用户上传或提供的所有材料

**操作**：
1. 扫描并识别所有材料类型（图片、PDF、JSON、截图、文字描述）
2. 尝试从 PNG 元数据提取 ComfyUI 内嵌 workflow/prompt：
   ```python
   from PIL import Image
   img = Image.open("作品.png")
   workflow = img.info.get("workflow")  # ComfyUI 工作流 JSON
   prompt = img.info.get("prompt")     # ComfyUI 任务配置 JSON
   ```
3. 对每条信息打上 Evidence Level：
   - 用户上传的文件/截图 → [Verified]
   - 用户口头说明 → [User-reported]
   - 从作品推断 → [Reconstructed]
   - 未提及 → [Unknown]
4. 列出缺失的推荐输入，一次询问不超过 3 个问题

**不允许**：对缺失信息做任何假设或填充

**输出**：带 Evidence Level 标注的材料清单

---

## Stage 3 — Artwork Analysis（作品图视觉分析）

**输入**：最终作品图（必须已收到，否则停止并询问用户）

**操作**：
1. 分析以下视觉特征（全部标注为 [Reconstructed]）：
   - **主体内容**：画面中有什么（人物、角色、场景、物品）
   - **风格与材质**：平面插画 / 3D 渲染 / 写实摄影 / 水彩 / 像素风等
   - **色彩体系**：主色调、辅助色、光影方向
   - **构图方式**：竖版/横版、居中/三分法、景深层次
   - **AI 工具痕迹**：潮玩质感、特定光晕风格、生成模型特征
2. 分析结果仅用于 Stage 5 Prompt 复现，不得直接写入文档正文作为已知事实

**不允许**：把分析结论措辞为已确认事实

**输出**：视觉分析报告（内部使用）

---

## Stage 4 — Process Reconstruction（创作过程整理）

**输入**：Stage 2 材料清单 + 用户自述

**操作**：
1. 整理所有 [Verified] 和 [User-reported] 信息
2. 生成创作流程叙述，覆盖：
   - 创作背景与选题动机
   - 工具选择与组合逻辑
   - AI 生成环节
   - 人工后期环节
   - 迭代过程（如有记录）
3. 明确区分"AI 负责的部分"和"人工负责的部分"
4. 人机协同比例仅在用户明确说明时才写入

**不允许**：
- 把 [Reconstructed] 内容混入流程叙述而不加标注
- 自动给出人机协同百分比（除非用户告知）

**输出**：创作过程草稿

---

## Stage 5 — Prompt Reconstruction（Prompt 复现）

> **注意**：本阶段生成的是 **Prompt 复现建议（Reconstructed Prompt）**，
> 用于帮助复现相似视觉方向，**不是恢复原始 Prompt**。

**执行条件**：用户未提供原始 Prompt，OR 明确请求 Prompt 复现建议

**输入**：Stage 3 视觉分析 + 用户确认的工具信息

**操作**：
1. 根据画面特征生成正向 Prompt 框架：
   ```
   (masterpiece, best quality:1.2), [风格], [主体], [场景], [光影], [色彩], [构图约束]
   ```
2. 根据画面排除元素生成负向 Prompt
3. 仅在用户确认了具体工具后，提供典型参数**范围**作为参考（不写入文档）

**工具参数参考范围（仅供参考，不填入文档）**：

| 工具 | 参数范围 |
|---|---|
| SDXL (ComfyUI/WebUI) | Steps: 20–40, CFG: 5–9, 分辨率: 1024×1024 |
| SD 1.5 | Steps: 20–35, CFG: 6–9, 分辨率: 512×768 |
| Midjourney | --ar 2:3 或 1:1, --stylize 50–300 |
| Flux | Steps: 15–30, CFG: 1–4 |
| ChatGPT DALL-E | 无外露参数 |

**不允许**：
- 把复现 Prompt 写成"原始 Prompt"
- 填写具体 Seed / Steps / CFG 数值（除非用户提供）
- 编造 LoRA 名称或模型版本

**输出**：Prompt 复现建议（明确标注"基于最终作品视觉分析生成，非原始 Prompt"）

---

## Stage 6 — Document Generation（文档生成）

**输入**：前五阶段所有输出 + 选定模板

**模板选择**：
- 大广赛 → `templates/competition-statement.md`（大广赛版本）
- 新媒体节 → `templates/competition-statement.md`（新媒体节版本）
- 学院奖 → `templates/competition-statement.md`（学院奖版本）
- 其他 → `templates/competition-statement.md`（通用版本）

**操作**：
1. 按模板结构填充内容
2. 严格遵守 Evidence Level 措辞规范
3. 生成 python-docx Word 文档

**格式要求**：
- 所有文字使用 Word 标准正文样式，标题手动加粗
- 禁止：灰色背景代码块 / 蓝色超链接字体 / 英文样式名出现在中文正文 / 边框阴影
- 图注简洁，每张图下方一行说明

**不允许**：
- 在文档中出现"当时使用的原始 Prompt 为……"（除非 [Verified]）
- 填写任何 [Unknown] 字段而不标注

**输出**：Word 文档草稿（.docx）

---

## Stage 7 — Compliance Check（合规检查）

**输入**：Stage 6 生成的文档

**操作**：逐条执行 `templates/evidence-checklist.md` 中的检查清单

**发现问题时**：
- 轻微问题（措辞）→ 自动修正并告知用户
- 重大问题（虚构数据、匿名违规）→ 停止，向用户报告，等待确认后再修正

**输出**：检查报告 + 修正后的最终文档

---

## Stage 8 — Export（导出与打包）

**输入**：通过合规检查的最终文档

**操作**：
1. 导出 Word 文件，命名：`{作品名}_{赛事简称}_AIGC说明书.docx`
2. 清空 Word 文件 `core_properties`（作者、公司、修订记录等元数据）
3. 检查是否需要打包：
   - 按赛事要求决定是否打 ZIP
   - ZIP 内容：说明书 + 作品原图 + 赛事要求的其他文件
4. 最终输出文件列表给用户确认

**不允许**：未通过 Stage 7 检查直接导出

**输出**：最终提交包