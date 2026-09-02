# Image Generation — 逆向图像过程材料生成与能力路由规范

> 本文档规范在 **Reconstruction Mode（逆向重构模式）** 下，Agent 如何通过三级能力路由（Capability Router）实际渲染落地过程图片文件，杜绝悬挂占位。

---

## 一、三级能力路由（Capability Router）

Reconstruction Mode 的铁律是：**过程图片必须实际生成落地为磁盘文件，绝不允许以“提供 Prompt 让用户自行生成”终结流程**。

```text
               ┌── Priority 1: 宿主原生图像生成/编辑能力 (如 generate_image)
               │
调度决策 ─────┼── Priority 2: 外部挂载生图能力 / MCP 图像服务
               │
               └── Priority 3: 确定性本地兜底脚本 (scripts/reconstruct_assets.py)
                               (基于 Pillow/OpenCV 强保障文件真实生成、非空)
```

1. **Priority 1（宿主原生生图能力）**：
   - 宿主具备原生图像生成/编辑能力时，优先作为主生成渠道，生成高审美质量的草图与演进初稿。
2. **Priority 2（外部生图能力）**：
   - 调度环境内挂载的生图工具或 MCP 图像服务。
3. **Priority 3（确定性本地兜底技术保障，Local Fallback）**：
   - 当宿主缺少在线生图工具时，自动调用仓库内置脚本：
     ```bash
     python scripts/reconstruct_assets.py --input <final_artwork_path> --output-dir <output_dir>
     ```
   - 依赖本地 Pillow 与 OpenCV，通过图像算子保证 `01_reconstructed_sketch.png`、`01_reconstructed_lineart.png`、`01_reconstructed_color_block.png`、`02_reconstructed_generation_v1.png`、`03_reconstructed_generation_v2.png` 100% 写入磁盘且 `filesize > 0`；
   - 保证后续 `scripts/build_docx.py` 能够成功读取并嵌入真实图片，彻底杜绝悬挂占位。

---

## 二、标准逆向图像算子定义

全仓权威资产清单直接引用 [skill/reconstruction.md](reconstruction.md) 的定义，五个算子对应生成标准如下：

### 1. `reference_to_sketch`（构图草图）
- **目标产物**：`01_reconstructed_sketch.png`
- **生成标准**：
  - 保留主体轮廓骨架、空间朝向与构图引导线；
  - 彻底剥离最终画面的高清材质与细腻纹理；
  - 呈现为具有前期构思感的铅笔线条或透视大关系稿。

### 2. `reference_to_lineart`（轮廓线稿）
- **目标产物**：`01_reconstructed_lineart.png`
- **生成标准**：
  - 提取画面主要角色/主体轮廓线，背景适度简化；
  - 呈现为纯净的黑白轮廓稿，可作为线稿垫图或 ControlNet Lineart 引导底图。

### 3. `reference_to_color_block`（色彩氛围大关系稿）
- **目标产物**：`01_reconstructed_color_block.png`
- **生成标准**：
  - 提取画面的主色调、辅助色与环境冷暖倾向；
  - 极大简化形体为平涂色块，呈现早期对画面色调与光影意境的概念探索。

### 4. `reference_to_intermediate_generation` (V1 阶段初稿)
- **目标产物**：`02_reconstructed_generation_v1.png`
- **生成标准**：
  - 主体形态与大构图已具象确立，与最终成图保持明确题材关联；
  - 但光影层次较平淡，特定微晶/毛发等细节尚未深化，体现自然的早期生成阶段感。

### 5. `reference_to_intermediate_generation` (V2 迭代深化稿)
- **目标产物**：`03_reconstructed_generation_v2.png`
- **生成标准**：
  - 针对初稿比对中诊断出的演进差距进行针对性深化；
  - 细节与边缘光显著提升，贴近最终成品。

---

## 三、生成文件强校验铁律

每项图片生成后，系统必须执行真实性物理校验：
1. **文件存在校验**：`os.path.exists(filepath) == True`
2. **非空校验**：`os.path.getsize(filepath) > 0`
3. **格式合规**：必须为标准 PNG/JPG 图像文件；
4. 任何一项校验失败，必须自动重试或触发 Priority 3 本地兜底，**绝不允许带病进入下一阶段**。

---

## 四、反伪造红线

1. **证据等级铁律**：所有逆向生成的草图、线稿与阶段图，证据等级一律固定为 `[Reconstructed]`，严禁标记为 `[Verified]`。
2. **绝不伪造软件操作界面**：
   - 严禁利用生图能力生成假的 Photoshop 图层窗口截屏、ComfyUI 节点连线截图或 WebUI 历史记录页冒充真实操作证据！
