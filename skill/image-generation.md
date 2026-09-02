# Image Generation — 逆向图像过程材料生成规范

> 本文档定义在 **Reconstruction Mode（逆向重构模式）** 下，Agent 如何通过能力导向（Capability-Based）的图像生成/编辑工具，实际渲染过程图片文件并建立自洽的演进闭环。

---

## 一、能力导向与“无占位悬挂”原则

1. **核心使命**：当用户仅提供一张最终作品时，自动调用生图能力，**造齐全部缺失的过程图片，不留任何空白悬挂占位**。
2. **能力导向设计（Capability-Based）**：
   - 不硬编码任何具体商业模型名称；
   - 规则定义为：`IF host supports image generation/editing: use available image capability`。
   - 宿主环境具备生图工具时，实际渲染生成文件（如 `01_reconstructed_sketch.png`、`02_reconstructed_generation_v1.png` 等），保存在项目目录并在说明文档中直接嵌入展示。

---

## 二、逆向图像算子定义与生成标准

### 1. `reference_to_sketch`（构图草图）
- **输入参考**：最终作品图
- **生成标准**：
  - 保留核心主体的大体形态、空间朝向与构图骨架；
  - 彻底剥离最终画面的高清材质、高光反射和精微纹理；
  - 呈现为具有前期构思感的铅笔手绘线条、透视大关系或结构辅助线状态；
  - **严禁** 直接在最终成图上简单叠加一层“素描滤镜”。

### 2. `reference_to_lineart`（轮廓线稿）
- **输入参考**：最终作品图
- **生成标准**：
  - 提取主体轮廓与关键边缘线条，背景适当简化；
  - 呈现为纯净的黑白轮廓稿，可作为线稿引导（如 ControlNet Lineart）的输入垫图。

### 3. `reference_to_color_block`（色彩氛围大关系稿）
- **输入参考**：最终作品图
- **生成标准**：
  - 提取画面的主色调、辅助色与冷暖光照倾向；
  - 简化细节形体为大笔刷涂抹色块，体现早期对画面色调与光影意境的概念探索。

### 4. `reference_to_composition_draft`（几何体块透视稿）
- **输入参考**：最终作品图
- **生成标准**：
  - 用简化的几何体块规划宏大场景、建筑物或透视空间中的主体占位。

### 5. `reference_to_intermediate_generation`（阶段性 AI 中间初稿）
- **输入参考**：前序草图 + 阶段 Prompt V1
- **生成标准**：
  - 与最终成图保持明确的视觉关联与题材一致性；
  - **完成度自然低于最终成图**（例如主体形态已具备，但边缘光感稍显平淡、特定细部肌理尚未深化）；
  - 该视觉差异将作为后续撰写 Prompt 调整理由（Adjustment Reason）的**真实比对依据**，拒绝刻板背台词。

---

## 三、动态视觉链规划（Minimal but Sufficient）

根据作品的技术路径与题材，动态选择最精简且足以自洽的图片组合（通常 2～4 张）：

```text
[构图草图 / 垫图] (01_reconstructed_sketch.png / 01_reconstructed_lineart.png)
       ↓
[阶段初稿 V1] (02_reconstructed_generation_v1.png)
       ↓
[迭代深化稿 V2] (03_reconstructed_generation_v2.png，若有必要)
       ↓
[最终作品] (final_artwork.png，创作者原件)
```

---

## 四、图像生成 Fallback 机制

若当前宿主 Agent 环境缺少图像生成工具（例如纯文本 CLI 模式）：
1. **绝不假装已生成**：严禁凭空编造不存在的本地图片路径欺骗用户；
2. **无缝输出完整生成方案**：
   - 在 Stage 3 和 Stage 5 中输出高精度的生图指令（Generation Prompts & Specs）；
   - 在文档图位中配以详尽的图意说明与生图参数提示，保证文本逻辑自洽完整，创作者在外部工具一键生成后即可无缝嵌入；
3. **交付状态提示**：在交付摘要中明确提示图片生成指令已就绪。

---

## 五、反伪造铁律（Anti-Hallucination）

1. **等级定级**：所有逆向生成的草图、线稿与阶段图，证据等级一律为 `[Reconstructed]`，严禁标记为 `[Verified]`。
2. **严禁生成假软件界面截图**：
   - 允许生成：构图草图、线稿、色块大关系图、阶段性 AI 画面初稿；
   - **绝对禁止利用生图能力生成假的 Photoshop 图层窗口、ComfyUI 节点连线截图、WebUI 任务历史等冒充真实操作截屏**！
