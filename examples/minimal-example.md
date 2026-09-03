# 示例：仅提供最终成品的最小调用回归基准（Minimal Regression Fixture）

> 本示例作为最严苛的自动化回归测试基准：
> **输入仅有单张最终成图 `final.png`**，不依赖创作者提供任何额外材料。
> 验证系统能否依靠全套逆向算子与本地兜底，自动造齐 12 项权威资产全集，完成从单图到全套提交材料的交付闭环。

---

## 一、创作者输入（Minimal Input）

```text
比赛：第十八届全国大学生广告艺术大赛
作品名：《未来共生》
附件：final.png (仅一张最终图，无任何其他文件)
```

---

## 二、自动资产构建与 Canonical Manifest 检验

Agent 启动 Reconstruction Mode，自动创建并解析权威资产清单：

1. `final_artwork` -> `final.png` [Verified]
2. `reconstructed_sketch` -> `01_reconstructed_sketch.png` (`reference_to_sketch`) [Reconstructed]
3. `reconstructed_lineart` -> `01_reconstructed_lineart.png` (`reference_to_lineart`) [Reconstructed]
4. `reconstructed_color_block` -> `01_reconstructed_color_block.png` (`reference_to_color_block`) [Reconstructed]
5. `generation_v1` -> 真实后端生成的同一作品完整初稿 [Reconstructed]
6. `generation_request_v1` / `generation_record_v1` -> 调用前请求与调用后执行证据
7. `difference_analysis_v1` / `adjustment_reason_v1` -> V1 与 Final 的实测诊断
8. 按停止条件选择直接进入 Final，或生成 `generation_v2/v3/...`
9. `parameter_record` -> 适配复现工具的参数配置表（Seed 标为未记录） [Reconstructed]
10. `prompt_record` -> `prompt-record.md` 阶段提示词记录表 [Reconstructed]
11. `stage_process_record` -> `stage_graph.json` 动态管线记录 [Reconstructed]
12. `statement_docx` -> `未来共生_大广赛_AIGC说明书.docx` 编译构建完成 [Reconstructed]

---

## 三、动态管线与参数自适应

- **无默认后期假设**：系统分析画面未见复杂矢量文字排版或分层拼接痕迹，确立三阶段纯生图演进管线，**不强行生成 Photoshop 阶段与工程截图**；
- **参数自适应工具**：根据推荐复现工具配置有效参数范围（如建议步数 25–35 步 [Reconstructed]，CFG 6.5–8.0 [Reconstructed]），Seed 严格注明“未记录（建议随机种子）”，绝不虚构具体数值；
- **全要素闭环**：所有生成的 PNG 文件真实存在且大小大于 0，Word 说明书内真实内嵌图片并附带规范学术图注，全文无模板占位符。
