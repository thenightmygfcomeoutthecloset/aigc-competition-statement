# Changelog

All notable changes to this project will be documented in this file.
This project follows [Semantic Versioning](https://semver.org/).

---

## [0.2.0] — 2026-09-03

### Added

- **核心定位全面升级（单图逆向重构）**：用户只需提供一张最终 AI 生成作品，Skill 即可自动深度分析画面特征、逆向推导合理的创作管线、生成早期复现垫图（如线稿/草图）、阶段视觉结果、演进 Prompt（V1/V2/V3）与参数建议，并输出符合高校竞赛要求的完整说明文档。
- **新增双模式路由（Dual Modes）**：
  - `Reconstruction Mode`：单图或过程材料严重缺失时启动，全流程逆向复现。
  - `Evidence Mode`：保留原有真实证据整理能力，真伪优先级明确（`Verified > User-reported > Reconstructed > Unknown`）。
- **新增 `skill/reconstruction.md`**：集中规范 Reconstruction Mode 的多维画面分析 Schema、流程推导范式、垫图生成算子及阶段视觉链规范。
- **新增能力导向逆向垫图（Capability-Based Assets）**：支持 `reference_to_sketch`、`reference_to_lineart`、`reference_to_composition_draft`、`reference_to_color_block`、`reference_to_grayscale_study`、`reference_to_simplified_input` 算子，强制要求复现垫图具备早期粗糙感，严禁生成高保真成品克隆。
- **新增素材资产分类管理（Asset Taxonomy）**：明确界定 `user-provided input`、`original reference`、`original sketch`、`reconstructed sketch`、`reconstructed reference`、`previous-stage output`。
- **新增知识产权审查模块（IP Check）**：自查第三方图片、Logo、字体、角色 IP 及专有模型，无法验证权属时严格标为 `Requires User Confirmation`。
- **新增提交流程完整度核查（Submission Check）**：逐项检查竞赛要素是否齐备；强制要求材料缺失时明确标为 `Required Evidence Missing`，严禁谎报完全通过。
- **新增复现材料免责声明（Reconstructed Disclaimer）**：在文档第七章强制加入标准化免责声明，严格区分复现技术分析与原始历史记录。

### Changed

- **文档架构重构为 Stage-Centric**：抛弃机械按“截图类型”罗列的旧结构，全面升级为以创作阶段为核心的七大标准章节，各阶段贯穿严密的 `Input → Tool → Prompt → Parameters → Output → Adjustment` 闭环证据链。
- **重构主说明书模板与清单**：`templates/competition-statement.md` 与 `templates/evidence-checklist.md` 全面支持 Stage-Centric 与双模式。
- **更新多平台适配器**：Codex `AGENTS.md`、Cursor `.mdc`、Windsurf 及 Claude 适配器统一更新以承载新的单图逆向重构能力。
- **更新示例与文档**：`examples/` 与 `README.md` 全面展示单图启动的执行流与 Stage-Centric 结构，版本同步提升至 `0.2.0`。
