# Changelog

All notable changes to this project will be documented in this file.
This project follows [Semantic Versioning](https://semver.org/).

---

## [0.2.2] — 2026-09-03

### Added & Focused

- **核心定位全面聚焦（单图造齐全部历史材料）**：确立“单图输入 → 逆向造齐全部历史材料 → 自动满足赛事材料要求”核心主线。面对单张最终作品，全自动走通全流程，缺什么补什么，无悬挂占位，输出默认状态即为“✅ 过程材料齐备，满足赛事规范，完整可直接提交”。
- **建立“赛事材料要求 → 逆向材料清单”自动映射机制**：
  - 构图规划 / 早期草图 ──→ `reference_to_sketch`
  - 轮廓线稿 / 引导垫图 ──→ `reference_to_lineart`
  - 色彩氛围 / 大关系稿 ──→ `reference_to_color_block`
  - 阶段生成初稿 (V1) ──→ `reference_to_intermediate_generation`
  - 迭代深化成果 (V2) ──→ `reference_to_intermediate_generation`
  - 演进提示词 ──→ 动态因果 Prompt 演进设计
  - 生成参数配置 ──→ 工具自适应参数映射
  - 创作说明文档 ──→ Stage-Centric 七大章节闭环 DOCX
- **消除机械缺陷剧本，改为自然可信的演进因果**：删除预先编造的“V1 一定背景空洞、光影不足”套路台词。改为真实对比流程：生成初稿 V1 → 视觉比对最终成图 → 诊断实际存在的演进差距 → 针对性调整 Prompt/参数 → 迭代深化。
- **阶段管线动态化（Dynamic Stage Graph）**：根据作品特征动态推导 Stage Graph（文生图概念迭代、线稿引导图生图、多元素分层合成），阶段数量做到 Minimal but Sufficient。
- **参数适配工具机制**：不再无脑套用 SD 的 Steps/CFG/Denoising。根据所选工具输出有效参数（如 MJ 输出 `--ar`/`--stylize`，DALL-E 等工具绝不硬造 Negative Prompt；Seed 统一标为未记录，严禁捏造具体数值）。
- **工具严格区分**：明确区分“原始创作工具（未记录 / 基于特征推断）”与“本次复现工具（宿主环境能力 / 推荐平台）”，绝不将复现工具冒充为创作者当时的原始历史工具。
- **命名与表述统一**：全仓库统一规范为“三工作模式”（Evidence Mode / Hybrid Mode / Reconstruction Mode），消除旧称谓混用。

---

## [0.2.1] — 2026-09-03

### Fixed & Closed-Loop Architecture

- 根入口接入 Reconstruction Mode，增加三模式分流路由。
- 彻底清理模板中的默认 Photoshop 伪操作与写死参数。
- 规范能力导向的图像生成与 Fallback 降级。
- 严禁生成假的软件操作界面截图。

---

## [0.2.0] — 2026-09-03

### Added

- 引入 Reconstruction Mode 与 Stage-Centric 架构初版。

---

## [0.1.3] — 2026-09-02

### Changed

- Adapters 全面 Thin 化，确立 Single Source of Truth。

