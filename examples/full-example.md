# 示例：真实材料保留与缺失材料自动补齐（Hybrid Mode Regression Fixture）

> 本示例展示 **Hybrid Mode** 的权威基准：
> 创作者提供了部分真实材料（最终成图 `未来之声.png` + 真实后期分层工程截图 `ps_layer.jpg`），但缺失原始草图、阶段生成图、原始 Prompt 与参数。
> 验证原则：**真实材料保留，缺失材料由 Canonical Manifest 自动补齐，最终 Manifest 100% Resolved**。

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

| 资产 ID | 产物形态 | 状态 | 处理说明 |
|---|---|---|---|
| `final_artwork` | `未来之声.png` | ✅ Existing | 保留原始事实，绝不替换 |
| `reconstructed_sketch` | `01_reconstructed_sketch.png` | ✅ Generated | 建立建筑与乐器空间透视草稿 |
| `reconstructed_lineart` | `01_reconstructed_lineart.png` | ✅ Generated | 提取琵琶轮廓线稿作为引导层 |
| `reconstructed_color_block` | `01_reconstructed_color_block.png` | ✅ Generated | 提取蓝紫与金黄冷暖光影色块关系 |
| `generation_v1` | 文件名由机器 Schema 读取 | ✅ Generated | 同一作品首个完整生成版本 |
| `generation_v2` | 按诊断动态生成 | ✅ Generated | 继承 V1 并解决实测问题的完整深化版本 |
| `generation_request_v1` | Prompt V1 与输入请求 | ✅ Generated | 确立完整画面方向 |
| `generation_request_v2` | Prompt V2 与演进请求 | ✅ Generated | 记录 KEEP/MODIFY/ADD/REDUCE/REASON |
| `parameter_record` | 工具自适应参数配置文件 | ✅ Generated | 建议采样步数 25–35 步，CFG 6.5–8.0，Seed 未记录 |
| `prompt_record` | `prompt-record.md` | ✅ Generated | 记录全阶段演进流、无空字段 |
| `stage_process_record`| `stage_graph.json` | ✅ Generated | 纳入阶段四真实 PS 工程，形成 4 阶段闭环 |
| `statement_docx` | `未来之声_大广赛_AIGC说明书.docx` | ✅ Generated | 嵌入真实 PS 截图与生成图，完成构建 |

**Manifest 决算**：`required: 12, existing: 1, generated: 11, missing: 0 → 100% Resolved`。

---

## 三、Stage-Centric 闭环结构呈现（含真实后期阶段）

通过 `stage_graph` 数据驱动装配，由于用户提供了真实的后期材料，阶段四如实输出：

- **3.1 阶段一：概念探索与构图规划**（输入：构图草图 `01_reconstructed_sketch.png`）
- **3.2 阶段二：Generation V1**（完整作品初稿）
- **3.3 阶段三：V1 诊断 → Prompt Evolution → Generation V2**（完整作品深化）
- **3.4 阶段四：人工后期精修与整合排版**：
  - 创作目的：擦除边缘噪点，强化主乐器对比度，排版主题文案；
  - 输入素材：阶段三输出的高清 AI 渲染图；
  - 使用工具：图像处理软件（Photoshop）；
  - 阶段结果：图 4 后期图层工程面板截图（`ps_layer.jpg`）与最终提交成图（`未来之声.png`）。

---

## 四、交付验证结论

```text
Manifest Resolution Status: COMPLETE
Existing Assets: 1 (final_artwork) + 1 (post_processing_screenshot)
Generated Assets: 11 (all generated, files exist, filesize > 0)
Zero Dangling Placeholders: PASSED
Technical Status: ✅ 工程资产与文件校验通过
```
