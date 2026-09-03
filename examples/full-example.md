# 示例：真实材料保留与缺失资产自动补齐（Hybrid Mode Regression Fixture）

> 本示例展示 **Hybrid Mode（混合重构模式）** 的权威基准：
> 创作者提供了部分真实材料（最终成图 `未来之声.png` + 真实后期分层工程截图 `ps_layer.jpg`），但缺失原始草图、阶段生成图、原始 Prompt 与参数。
> 验证原则：**真实材料保留为 `[Verified]`，缺失资产由 Canonical Manifest 自动补齐为 `[Reconstructed]`，最终 Manifest 100% Resolved**。

---

## 一、创作者原始输入（Partial Evidence Input）

```text
比赛：第十八届全国大学生广告艺术大赛（大广赛）
作品名：《未来之声》
附件上传：
  1. 最终成稿图：未来之声.png
  2. 真实后期工程截图：ps_layer.jpg (证明做过 Photoshop 最终图层调色与文字排版)
（未保存原始草图垫图、未记录原始 Prompt 与生成参数）
```

---

## 二、Canonical Manifest 状态与全资产 Resolve 过程

系统进入 **Hybrid Mode**，比对 Canonical Required Assets 清单并全量补齐：

| 资产 ID | 产物形态 | 状态 | 来源与证据等级 | 处理说明 |
|---|---|---|---|---|
| `final_artwork` | `未来之声.png` | ✅ Existing | User 原件 `[Verified]` | 保留原始事实，绝不替换 |
| `reconstructed_sketch` | `01_reconstructed_sketch.png` | ✅ Generated | `reference_to_sketch` `[Reconstructed]` | 逆向推演建筑与乐器空间透视草稿 |
| `reconstructed_lineart` | `01_reconstructed_lineart.png` | ✅ Generated | `reference_to_lineart` `[Reconstructed]` | 逆向提取琵琶轮廓线稿作为引导层 |
| `reconstructed_color_block` | `01_reconstructed_color_block.png` | ✅ Generated | `reference_to_color_block` `[Reconstructed]` | 提取蓝紫与金黄冷暖光影色块关系 |
| `generation_v1` | 文件名由机器 Schema 读取 | ✅ Generated | 真实后端 `[Reconstructed]` | 同一作品首个完整生成版本 |
| `generation_v2` | 按诊断动态生成 | ✅ Generated | 真实后端 `[Reconstructed]` | 继承 V1 并解决实测问题的完整深化版本 |
| `generation_request_v1` | Prompt V1 与输入请求 | ✅ Generated | 调用前持久化 `[Reconstructed]` | 确立完整画面方向 |
| `generation_request_v2` | Prompt V2 与演进请求 | ✅ Generated | 基于 V1 实测诊断 `[Reconstructed]` | 记录 KEEP/MODIFY/ADD/REDUCE/REASON |
| `parameter_record` | 工具自适应参数配置文件 | ✅ Generated | Tool Parameter Profile 映射 `[Reconstructed]` | 建议采样步数 25–35 步，CFG 6.5–8.0，Seed 未记录 |
| `prompt_record` | `prompt-record.md` | ✅ Generated | Stage-Aware 模板渲染 `[Reconstructed]` | 记录全阶段演进流、无空字段 |
| `stage_process_record`| `stage_graph.json` | ✅ Generated | 动态管线构建 `[Reconstructed]` | 纳入阶段四真实 PS 工程，形成 4 阶段闭环 |
| `statement_docx` | `未来之声_大广赛_AIGC说明书.docx` | ✅ Generated | `scripts/build_docx.py` 编译 `[Reconstructed]` | 嵌入真实 PS 截图与逆向生成图，完成构建 |

**Manifest 决算**：`required: 12, existing: 1, generated: 11, missing: 0 → 100% Resolved`。

---

## 三、Stage-Centric 闭环结构呈现（含真实后期阶段）

通过 `stage_graph` 数据驱动装配，由于用户提供了真实的后期材料，阶段四如实输出为 `[Verified]`：

- **3.1 阶段一：概念探索与构图规划**（输入：逆向草图 `01_reconstructed_sketch.png`，[Reconstructed]）
- **3.2 阶段二：Generation V1**（完整作品初稿，[Reconstructed]）
- **3.3 阶段三：V1 诊断 → Prompt Evolution → Generation V2**（完整作品深化，[Reconstructed]）
- **3.4 阶段四：人工后期精修与整合排版（真实证据呈现）**：
  - 创作目的：擦除边缘噪点，强化主乐器对比度，排版主题文案；
  - 输入素材：阶段三输出的高清 AI 渲染图；
  - 使用工具：图像处理软件（Photoshop）；
  - 阶段结果：图 4 后期图层工程面板截图（`ps_layer.jpg`，`[Verified]`）与最终提交成图（`未来之声.png`，`[Verified]`）。

---

## 四、交付验证结论

```text
Manifest Resolution Status: COMPLETE
Existing Verified Assets: 1 (final_artwork) + 1 (post_processing_screenshot)
Reconstructed Assets: 11 (all generated, files exist, filesize > 0)
Zero Dangling Placeholders: PASSED
Technical Status: ✅ 工程资产与文件校验通过；版权、原创性和参赛资格仍以用户确认及赛事审核为准
```
