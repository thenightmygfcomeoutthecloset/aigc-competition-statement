# 示例：完整流程演示

> **声明：本示例为虚构演示（Fictional Demo）**
> 作品、作者、参数均为示意，不代表真实创作记录。

---

## 场景设定

| 字段 | 内容 |
|---|---|
| 比赛 | 第十届大学生新媒体创意节 |
| 作品名称 | 《未来之声》 |
| 工具 | ComfyUI + SDXL + Photoshop |
| 原始 Prompt | 已丢失 |
| 最终作品图 | ✅ 已上传（赛博朋克风格城市夜景海报） |

---

## Stage 1：核对赛事要求

Agent 查找赛事要求后提取：
- AIGC 作品需附创作过程说明 ✅
- 无严格格式要求，建议包含工具说明和 AI 参与说明
- 与作品一起压缩打包提交
- 不要求匿名

---

## Stage 2：素材收集与分级

| 素材 | Evidence Level |
|---|---|
| 最终作品（PNG，1920×1080） | [Verified] |
| 使用工具：ComfyUI + SDXL + PS | [User-reported] |
| 创作主题："未来城市中的音乐节文化" | [User-reported] |
| 原始 Prompt | [Unknown] — 已丢失 |
| 参数（Steps/CFG/Seed） | [Unknown] — 未记录 |
| 工作流截图 | [Unknown] — 未保存 |

---

## Stage 3：作品图视觉分析

**[Reconstructed] 视觉特征分析：**
- 主体：城市高楼夜景，前景音乐符号图形元素
- 风格：赛博朋克，高对比度蓝紫色调，霓虹灯效果
- 构图：竖版海报，中心构图，强烈景深层次
- AI 特征：光晕渲染质感、建筑细节精细度，疑似 SDXL 风格化生成特征

---

## Stage 4：创作过程整理

（基于 [Verified] + [User-reported] 信息）

> "本作品以'未来城市中的音乐节文化'为主题，使用 ComfyUI + SDXL 作为主要生成工具，
> 在 Photoshop 中完成音乐元素和文字排版的后期处理。"

---

## Stage 5：Prompt 复现建议

**[Reconstructed] — 基于视觉分析生成，非原始记录**

> "创作时使用的原始提示词已不可考。以下 Prompt 复现建议根据最终作品的视觉特征生成，
> 可帮助复现相近的视觉方向，并非当时实际使用的提示词。"

**正向 Prompt（复现参考）**：
```
(masterpiece, best quality:1.2), cyberpunk city skyline at night,
neon lights, purple and blue color palette, music festival atmosphere,
musical notes floating in air, cinematic lighting, vertical composition,
bokeh depth of field, ultra detailed architecture
```

**负向 Prompt（复现参考）**：
```
low quality, worst quality, text, watermark, signature,
flat, 2D, daytime, warm colors, blurry foreground
```

**参数说明**：
未记录创作时的具体参数。使用 SDXL 的典型参数范围供参考（不代表实际使用值）：
Steps 20–40，CFG 5–9，分辨率 1024×1024。

---

## Stage 6：生成文档（片段预览）

---

**《未来之声》AIGC 创作过程说明书**

**一、创意阐释与设计逻辑**

本作品以"未来城市中的音乐节文化"为主题，探索数字时代青年文化与城市空间的交融想象。
赛博朋克风格的视觉语言与音乐节的活力氛围相呼应，通过强烈的光影对比传递未来感与能量感。

视觉上选择高对比度蓝紫色调，以霓虹灯元素构建夜晚城市氛围，
音乐符号以漂浮状态嵌入城市背景，强调"声音穿透空间"的概念。

**二、AI 辅助创作说明**

1. 核心工具链

据创作者表述，本作品使用 ComfyUI 作为图像生成平台，
结合 Stable Diffusion XL 模型完成主画面生成。
最终在 Adobe Photoshop 中完成音乐元素嵌入、文字排版及色调微调。

| 工具 | 用途 |
|---|---|
| ComfyUI + SDXL | 主画面赛博朋克城市背景生成 |
| Adobe Photoshop | 音乐符号元素合成、文字排版、最终调色 |

2. Prompt 复现建议（Prompt Reconstruction）

创作时使用的原始提示词已不可考。以下内容基于最终作品视觉分析生成，
为复现参考，非创作时实际使用的原始提示词：

正向 Prompt（复现参考）：
(masterpiece, best quality:1.2), cyberpunk city skyline at night, ...

3. 参数记录

创作时未保存具体参数，不适用。

4. 人机协同说明

AI 负责：城市夜景背景画面的生成、光效与色调的基础渲染
人工负责：创意概念确定、Prompt 设计方向、音乐元素合成、文字排版、最终色调微调

---

## Stage 7：合规检查结果

✅ 无虚构模型参数
✅ Reconstructed Prompt 明确标注
✅ 无个人身份信息
✅ 区分了 AI 和人工环节
✅ 字数约 800 字，符合要求
✅ 至少包含创作过程叙述

**检查通过，可以导出。**

---

## Stage 8：导出

```
未来之声_新媒体节_提交包.zip
├── 未来之声_新媒体节_AIGC说明书.docx
└── 未来之声_最终作品.png
```