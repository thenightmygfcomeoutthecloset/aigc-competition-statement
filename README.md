# AIGC Competition Statement

> **单图输入 → 逆向造齐全部历史材料 → 自动满足赛事材料要求**
> 用户只需提供一张最终 AI 作品，即可自动逆向推导合理管线，逐项补齐缺失的构图草图、阶段初稿、演进 Prompt 与参数配置，输出无悬挂占位、默认“完整可提交”的 AIGC 创作说明文档。

[![version](https://img.shields.io/badge/version-0.2.2-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

面向大广赛、大学生新媒体创意节、学院奖等高校创意竞赛的 AIGC 创作说明书 Agent Skill。

---

## 核心三工作模式

Agent 接收作品后根据已有材料自动分流：

| 模式 | 适用场景 | 核心机制 |
|---|---|---|
| **Reconstruction Mode（逆向重构模式）** | **用户仅提供一张最终作品**，或创作过程材料严重缺失 | **缺什么补什么，自动造齐**：自动将赛事材料要求映射为待补清单，逐项生成构图草图、阶段初稿、演进 Prompt（V1/V2，自然演进无刻板剧本）与工具自适应参数，装配无占位悬挂、默认“完整可提交”的 Stage-Centric 说明书。**全程不中断、不逼问补材料。** |
| **Hybrid Mode（混合重构模式）** | 用户提供了部分真实材料（如仅有工具名或口述思路，缺少草图或Prompt） | 真实材料归为 `[Verified]` / `[User-reported]`；**仅对缺失环节启动重构**，绝不生成冗余替代品覆盖真实证据。 |
| **Evidence Mode（真实证据模式）** | 用户已保存完整原始 Prompt、垫图、截图与参数 | 直接归档整理真实材料，严格证据分级，不生成任何替代性材料。 |

---

## 赛事材料要求 → 逆向材料清单自动映射

针对高校竞赛普遍要求的材料要件，Skill 建立 1:1 的逆向生成能力映射：

| 赛事材料要求项 | 逆向目标资产 | 对应逆向算子 / 方式 |
|---|---|---|
| **构图规划 / 早期草图** | `01_reconstructed_sketch.png` | `reference_to_sketch`（铅笔线条、透视大关系） |
| **轮廓线稿 / 垫图输入** | `01_reconstructed_lineart.png` | `reference_to_lineart`（黑白轮廓稿、引导输入） |
| **色彩氛围 / 大关系稿** | `01_reconstructed_color_block.png` | `reference_to_color_block`（大笔刷平涂、色彩倾向） |
| **阶段生成初稿 (V1)** | `02_reconstructed_generation_v1.png` | `reference_to_intermediate_generation`（体现自然阶段差距） |
| **迭代深化稿 (V2)** | `03_reconstructed_generation_v2.png` | `reference_to_intermediate_generation`（针对差距深化细节） |
| **演进提示词 (Prompts)** | Prompt V1 / Prompt V2 | 动态因果演进（比对初稿与成图，针对性深化） |
| **生成参数配置** | 建议参数配置表 | 工具自适应参数映射（仅输出当前工具真正支持项） |
| **创作过程说明书** | Stage-Centric 七大章节 DOCX | 自动装配生成，无悬挂占位，图文闭环 |

---

## 自然可信的逆向演进（拒绝刻板剧本）

1. **真实差距诊断**：拒绝预先写死“V1 背景空洞、光影不足”套路台词。采用真实流程：生成初稿 V1 → 视觉比对最终成图 → 诊断实际存在的演进差距 → 针对性改写 Prompt/参数 → 迭代深化；
2. **阶段管线动态化（Dynamic Stage Graph）**：根据作品特征动态推导管线（文生图迭代、线稿引导生图、多元素分层合成），阶段数量做到 Minimal but Sufficient；
3. **参数适配工具**：严禁对所有工具无脑套用 SD 的 Steps/CFG/Denoising。工具若无负向词项（如 DALL-E）绝不硬造 Negative Prompt；Seed 统一标为“未记录（建议随机）”，严禁捏造具体数值；
4. **严格区分工具**：明确区分“原始创作工具（未记录 / 基于特征推断）”与“本次复现工具（宿主环境能力 / 推荐平台）”，绝不将复现工具冒充为原始创作工具；
5. **条件性后期**：无后期证据时客观表述为纯 AI 直出，严禁凭空强加 Photoshop 图层修整与假工程截图。

---

## 阶段证据链架构（Stage-Centric）

$$\text{Input (输入素材/垫图)} \longrightarrow \text{Tool (工具)} \longrightarrow \text{Prompt (提示词)} \longrightarrow \text{Parameters (参数)} \longrightarrow \text{Output (阶段结果)} \longrightarrow \text{Adjustment (调整说明)}$$

### 七大标准文档章节
1. **作品基本信息**（作品名、赛事、类型、主题、AIGC技术路径、工具环境说明）
2. **创作构思**（选题立意、视觉思路、设计目标、人机协同目的）
3. **阶段性创作过程**（核心证据链：动态阶段推进，无假 PS，图文呼应）
4. **AIGC 工具使用说明与人机协同分工**（工具矩阵与主观能动性分工）
5. **全流程 Prompt、输入素材与参数汇总表**（单层完整对照大表）
6. **版权、素材来源与原创性说明**（自主承诺合规，完成知识产权自查）
7. **复现材料特别说明**（明确复现材料用于完整展示创作逻辑与技术可复现性）

---

## 安装

### Google Antigravity（AGY）

```powershell
.\scripts\install.ps1 -Platform antigravity
```

安装到 `~/.gemini/config/skills/aigc-competition-statement/`。

### Codex

```powershell
.\scripts\install.ps1 -Platform codex
```

安装到 `~/.agents/skills/aigc-competition-statement/`。

### Cursor

```powershell
.\scripts\install.ps1 -Platform cursor
```

安装到 `~/.cursor/skills/aigc-competition-statement/`。

macOS / Linux：

```bash
bash scripts/install.sh antigravity
bash scripts/install.sh codex
bash scripts/install.sh cursor
```

---

## 调用方式

在 Codex 中输入：
```text
$aigc-competition-statement 帮我根据这张作品生成 AIGC 创作说明。
比赛：第十八届大广赛
（上传最终作品图）
```

在 Cursor 中通过 `/aigc-competition-statement` 调用；在 AGY 等平台中直接上传作品并提出参赛文案需求即可自动激活。

---

## 目录结构

```text
├── SKILL.md              # 规范入口（三工作模式路由与 Single Source of Truth）
├── skill/                # 核心下沉规范
│   ├── reconstruction.md # 逆向重构模式、材料映射清单与动态管线
│   ├── image-generation.md# 逆向图像生成算子与视觉链要求
│   ├── workflow.md       # 三模式驱动八阶段工作流
│   ├── safety.md         # 学术真实性底线、工具适配与 IP 自查
│   └── output-spec.md    # Stage-Centric Word 文档输出与排版标准
├── templates/            # competition-statement / prompt-record / evidence-checklist
├── adapters/             # Cursor / Codex / Windsurf / Claude 轻量适配层
├── examples/             # final-image-only / minimal-example / full-example
└── scripts/              # Windows 与 macOS/Linux 自动化安装器
```

## License

MIT
