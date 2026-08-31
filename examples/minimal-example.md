# 示例：最简调用

> 这是最简单的使用场景——用户只说明了比赛和工具，然后上传作品图。
> 以下展示 Agent 会如何响应。

---

## 用户输入

```
帮我整理这件作品的 AIGC 创作说明。
比赛：第十届大学生新媒体创意节
使用工具：ComfyUI + SDXL + Photoshop
```
（同时上传了最终成品 PNG 图）

---

## Agent 响应（示例）

**已收到**：
- ✅ 最终作品图（PNG）
- ✅ 比赛：第十届大学生新媒体创意节
- ✅ 使用工具：ComfyUI + SDXL + Photoshop

**正在查找赛事要求**……  
已找到：新媒体创意节要求附 AIGC 创作说明，无严格格式限制，与作品一起打包提交。

**有两个问题需要确认：**
1. 你有没有保存当时的原始 Prompt（Txt 文件或 ComfyUI 截图）？
2. 大概记得你的创作主题或作品的核心想法吗？（写进创意说明部分）

---

## Agent 内部分级（不展示给用户，仅供说明）

| 信息 | Evidence Level |
|---|---|
| 使用 ComfyUI + SDXL + Photoshop | [User-reported] |
| 最终作品图 | [Verified] |
| 作品视觉特征分析 | [Reconstructed] |
| 原始 Prompt | [Unknown]（待确认） |
| 参数（Steps/CFG/Seed）| [Unknown] |

---

## 生成结果预览（片段）

```
二、AI 辅助创作说明

1. 核心工具链

据创作者表述，本作品使用 ComfyUI 作为节点式工作流平台，
以 Stable Diffusion XL 模型完成图像生成，最终在 Adobe Photoshop 中完成后期处理。

2. 提示词复现建议（Prompt Reconstruction）

创作时使用的原始提示词未作记录。以下为基于最终作品视觉特征生成的
Prompt 复现建议，用于帮助复现相似视觉方向，非创作时实际使用的提示词：

正向 Prompt（复现参考）：
(masterpiece, best quality:1.2), cinematic lighting, [主体描述], ...

3. 参数记录

创作参数未作记录，不适用。
```