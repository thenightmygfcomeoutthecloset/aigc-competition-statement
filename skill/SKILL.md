---
name: aigc-competition-statement
version: 0.1.1
description: >-
  为大广赛、大学生新媒体创意节、学院奖等国内高校创意竞赛，
  帮助用户整理 AIGC 创作过程说明书（Word 格式）。
  支持从最终作品图重构 Prompt（明确标记为 Reconstructed），
  执行合规检查，生成符合赛事要求的提交材料。
intended_use: >-
  仅用于帮助创作者真实、诚实地整理和呈现 AI 辅助创作过程。
  不得用于伪造创作历史、编造未经核实的参数或事实。
---

# AIGC 竞赛创作说明书生成技能

> 本文档是面向 Agent 的调用规范。人类用户请参阅 [README.md](../README.md)。

---

## Trigger（触发条件）

**满足以下任意条件时启用本 Skill：**

- 用户说"帮我写 AIGC 创作说明"、"帮我整理 AI 创作过程"、"比赛要提交 AI 声明"
- 提到具体赛事关键词：大广赛、新媒体节、新媒体创意节、学院奖、数字媒体竞赛
- 提到"AIGC 说明书"、"AI 使用说明"、"Prompt 记录"、"比赛 AI 技术报告"
- 提到"创作过程文档"并涉及 AI 工具（ComfyUI、SD、Midjourney、DALL-E 等）

**不触发场景：**

- 普通文案写作任务（无比赛/竞赛背景）
- 用户只想学习 Prompt 写法
- 与竞赛提交无关的 AI 工具使用咨询

---

## Required Inputs（输入规范）

### 必须输入（缺少则主动询问）

| 字段 | 说明 |
|---|---|
| 比赛名称 | 例如"第十届大学生新媒体创意节" |
| 最终作品 | 最终成品图（图片文件或链接） |

### 推荐输入（有则优先使用，无则继续）

| 字段 | 说明 |
|---|---|
| 实际使用的 AI 工具 | ComfyUI / SD WebUI / Midjourney / DALL-E / Flux 等 |
| 创作思路 | 用户自述的创意逻辑和主题选择 |
| 已保存的 Prompt | 用户实际使用的原始正向/负向提示词 |
| 工作流截图 | ComfyUI 节点图 / SD WebUI 界面截图 |
| 软件截图 | Photoshop 图层面板等后期工具截图 |
| 比赛规则文件 | .pdf 或链接 |

### 可选输入（填写后提升准确度）

| 字段 | 说明 |
|---|---|
| 使用的模型 | SDXL / SD 1.5 / Flux Dev 等具体版本 |
| LoRA 名称 | 使用的 LoRA 模型 |
| 生成参数 | Steps / CFG / Sampler / Seed / 分辨率 |
| 后期软件 | Photoshop / Lightroom / Procreate 等 |
| 迭代记录 | 多轮生成的过程说明 |

> **原则**：Agent 应先读取已有材料，再按顺序追问必须字段，然后推荐字段。不得一次列出所有字段让用户填写。

---

## Evidence Levels（证据可信度分级）

这是本 Skill 最核心的机制。Agent 在处理所有信息时必须标注可信等级。

| 等级 | 定义 | 文档措辞规范 |
|---|---|---|
| [Verified] | 用户提供了明确材料（图片、文件、截图等）| 直接陈述："创作使用了 ComfyUI + SDXL。" |
| [User-reported] | 用户口头说明，无材料佐证 | 引述语气："据创作者表述，使用了……" |
| [Reconstructed] | 根据最终作品图分析推断 | 明确标注："以下为 Prompt 复现建议，基于最终视觉效果生成……" |
| [Unknown] | 无法确认的信息 | 留空，或标注"该参数未记录"，不得填写任何推测值 |

措辞必须与可信等级严格一致。不允许将 [Reconstructed] 信息的措辞写成 [Verified] 语气。

---

## Anti-Hallucination Rules（禁止编造规则）

以下信息在未经用户明确提供的情况下，严格禁止由 Agent 自动填写：

- Seed（种子值）
- 具体 Steps 数值
- 具体 CFG 数值
- 具体 Sampler 名称
- 模型版本号或完整模型文件名
- LoRA 权重（如"LoRA 0.7"）
- 原始 Prompt 文本
- 创作日期 / 生成时间
- 软件版本号
- 生成次数或迭代次数
- 工作流节点连接细节
- 截图内容描述（如未收到截图）

**处理未知信息的正确方式：**
1. 留空该字段
2. 写"该参数未记录"或"不适用"
3. 如需参考方向，写"如使用 SDXL，典型参数范围为……"并明确说明这是参考范围而非实际值

详见 safety.md。

---

## Workflow（执行流程概览）

完整流程定义见 workflow.md。

```
Stage 1  Competition Requirements  查找赛事要求
         ├─ 找到官方规则 → Competition-specific mode
         └─ 未找到      → Generic Draft Mode（继续执行，文档顶部标注未校验）

Stage 2  Evidence Collection       素材收集与分级
Stage 3  Artwork Analysis          作品图视觉分析（全部标注 [Reconstructed]）
Stage 4  Process Reconstruction    创作过程整理
Stage 5  Prompt Reconstruction     Prompt 复现（仅在无原始 Prompt 时执行）
Stage 6  Document Generation       文档生成（使用通用模板，见 templates/）
Stage 7  Compliance Check          合规与匿名检查
Stage 8  Export                    导出与打包
```

---

## Template（v0.1.1 模板说明）

当前版本（v0.1.1）所有赛事统一使用 `templates/competition-statement.md`（通用模板）。

Agent 根据赛事官方要求动态调整字段和字数，无需切换不同模板文件。

> 赛事专用模板（大广赛版、新媒体节版、学院奖版）计划在 v0.2.0 中引入。

---

## Quick Start（最小调用示例）

用户输入：
> 帮我整理这件作品的 AIGC 创作说明。比赛：第十届大学生新媒体创意节。使用工具：ComfyUI + SDXL + Photoshop

Agent 执行顺序：
1. 确认收到最终作品图（若无则询问）
2. 查找/搜索赛事要求（找不到则进入 Generic Draft Mode）
3. 收集并分级所有素材
4. 分析作品图视觉特征
5. 询问是否有保存原始 Prompt（决定是否执行 Stage 5）
6. 生成文档 → 执行合规检查 → 导出