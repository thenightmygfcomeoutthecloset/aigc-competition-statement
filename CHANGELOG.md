# Changelog

All notable changes to this project will be documented in this file.
This project follows [Semantic Versioning](https://semver.org/).

---

## [0.2.1] — 2026-09-03

### Fixed & Closed-Loop Architecture

- **P0 根入口接入 Reconstruction Mode**：重构 `SKILL.md`，确立三模式分流路由（Evidence Mode / Hybrid Mode / Reconstruction Mode）。明确当用户仅提供单张最终成图时，不中断、不逼问补齐历史记录，强制跳转并阅读 `skill/reconstruction.md` 执行逆向推演。
- **P0 模式驱动工作流（Mode-Driven Workflow）**：重写 `skill/workflow.md`，将主干彻底切换为模式驱动架构，确保单图输入下全自动进入完整闭环。
- **P0 彻底清除模板中的“伪历史记录”与硬编码参数**：
  - 清理 `templates/competition-statement.md` 中的默认 Photoshop 图层修整、曲线调色等伪造操作；确立人工后期阶段的**条件性输出准则**（无证据时如实说明纯 AI 直出，严禁强加 PS 和假截图）。
  - 删除模板中写死的具体参数（Steps 30, CFG 7.0, Denoising 0.6 等），全面替换为建议复现范围（如 25–35 步 [Reconstructed]）或标注“未记录”。Seed 严禁编造具体数值。
- **P0 新增 `skill/image-generation.md` 逆向图像生成规范**：
  - 规范能力导向（Capability-Based）的图像生成算子（`reference_to_sketch`、`reference_to_color_block`、`reference_to_lineart`、`reference_to_intermediate_generation`）。
  - 强制要求复现垫图必须更早、更粗糙、更简化，严禁生成高保真最终成品克隆。
  - 阶段性 AI 中间稿必须包含合理阶段缺陷，为后续 Prompt 调整建立因果依据。
  - 明确 Fallback 降级：宿主缺少生图能力时，输出精细生图指令并标注占位，严禁凭空编造假图片文件路径，并在检查中标记 `Required Visual Evidence Missing`。
- **新增禁止生成假软件界面证据铁律**：在 `skill/safety.md` 中明令禁止利用 AI 生成 Photoshop 图层工程窗口、ComfyUI 节点截图、WebUI 历史界面等冒充真实操作证据。
- **新增单图启动实战案例**：新增 `examples/final-image-only.md`，完整演示从 `final.png` 自动化逆向推演、生成构图草图与阶段初稿、演进 Prompt 及 Stage-Centric 文档全过程。
- **多端适配器与安装器同步**：更新 Cursor、Codex、Windsurf 及 Claude 轻量适配层；安装脚本版本同步提升至 `0.2.1`。

---

## [0.2.0] — 2026-09-03

### Added

- 初始引入 Reconstruction Mode 与 Stage-Centric 阶段式架构。
- 引入知识产权（IP Check）与提交流程审查。

---

## [0.1.3] — 2026-09-02

### Changed

- Adapters 全面 Thin 化，确立 Single Source of Truth。
- 移除了 Danbooru 刻板语法，实现 Prompt 平台自适应。

---

## [0.1.2] — 2026-08-31

### Fixed

- SKILL.md 移至根目录，修复原生发现与各平台安装路径。
