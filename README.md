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
| **Reconstruction Mode（逆向重构模式）** | **用户仅提供一张最终作品**，或创作过程材料严重缺失 | **缺什么补什么，自动造齐**：自动将赛事材料要求映射为待补清单，逐项生成构图草图、线稿、色块大关系稿、阶段初稿(V1)、迭代深化稿(V2)、演进 Prompt（V1/V2）与工具自适应参数，装配无占位悬挂、默认“完整可提交”的 Stage-Centric 说明书与完整交付包。**全程不中断、不逼问补材料。** |
| **Hybrid Mode（混合重构模式）** | 用户提供了部分真实材料（如仅有工具名或口述思路，缺少草图或Prompt） | 真实材料归为 `[Verified]` / `[User-reported]`；**仅对缺失环节启动重构**，绝不生成冗余替代品覆盖真实证据。 |
| **Evidence Mode（真实证据模式）** | 用户已保存完整原始 Prompt、垫图、截图与参数 | 直接归档整理真实材料，严格证据分级，不生成任何替代性材料。 |

---

## 权威资产清单（Canonical Required Assets Schema）

全仓权威资产清单以 `skill/reconstruction.md` 为唯一规范源，单图输入时自动保证以下 12 项资产 100% 落地：

| 资产 ID | 规范产物形态 | 对应逆向算子 / 来源 | 作用说明 |
|---|---|---|---|
| `final_artwork` | `final.png` | 用户原件 | 最终 AI 作品成图（`[Verified]`） |
| `reconstructed_sketch` | `01_reconstructed_sketch.png` | `reference_to_sketch` | 铅笔构图草图、透视骨架关系 |
| `reconstructed_lineart` | `01_reconstructed_lineart.png` | `reference_to_lineart` | 纯净轮廓线稿、用于垫图约束 |
| `reconstructed_color_block` | `01_reconstructed_color_block.png` | `reference_to_color_block` | 大笔刷平涂色块、色彩氛围规划 |
| `generation_v1` | `02_reconstructed_generation_v1.png` | `reference_to_intermediate_generation` | 阶段初稿 V1，基础具象成型 |
| `generation_v2` | `03_reconstructed_generation_v2.png` | `reference_to_intermediate_generation` | 迭代深化稿 V2，贴近最终成品 |
| `prompt_v1` | Prompt V1 阶段初版提示词 | 动态语义解构生成 | 基础主体与环境基调描述 |
| `prompt_v2` | Prompt V2 针对性深化提示词 | 基于真实演进差距对比生成 | 深化细节与材质（含负向排除词） |
| `parameter_record` | 工具自适应参数配置表 | 工具自适应参数映射 | 仅输出当前工具真正支持的有效参数 |
| `prompt_record` | `prompt-record.md` | 模板渲染与归档 | Stage-Aware 提示词全流程演进记录表 |
| `stage_process_record`| `stage_graph.json` | 动态管线构建 | 数据驱动的动态阶段创作记录 |
| `statement_docx` | `{作品名}_{赛事简称}_AIGC说明书.docx` | `scripts/build_docx.py` | 排版严谨、真实嵌图的提交 Word 文档 |

---

## 自然可信的逆向演进（拒绝刻板剧本）

1. **真实演进差距诊断**：拒绝预先写死“V1 背景空洞、光影不足”套路台词。采用真实流程：生成初稿 V1 → 视觉比对最终成图 → 诊断实际存在的演进差距 → 针对性改写 Prompt/参数 → 迭代深化；
2. **阶段管线动态化（Dynamic Stage Graph）**：根据作品特征动态推导管线（文生图迭代、线稿引导生图、多元素分层合成），阶段数量做到 Minimal but Sufficient；
3. **参数适配工具**：严禁对所有工具无脑套用 SD 的 Steps/CFG/Denoising。工具若无负向词项（如 DALL-E）绝不硬造 Negative Prompt；Seed 统一标为“未记录（建议随机）”，严禁捏造具体数值；
4. **严格区分工具**：明确区分“原始创作工具（未记录 / 基于特征推断）”与“本次复现工具（宿主环境能力 / 推荐平台）”，绝不将复现工具冒充为原始创作工具；
5. **条件性后期**：无后期证据时客观表述为纯 AI 直出，严禁凭空强加 Photoshop 图层修整与假工程截图。

---

## 阶段证据链架构（Stage-Centric）

$$\text{Input (输入素材/垫图)} \longrightarrow \text{Tool (工具)} \longrightarrow \text{Prompt (提示词)} \longrightarrow \text{Parameters (参数)} \longrightarrow \text{Output (阶段结果)} \longrightarrow \text{Adjustment (调整说明)}$$

---

## 目录结构（Layout）

### 1. 完整仓库结构（Repository Layout）

```text
├── SKILL.md              # 规范入口（三工作模式路由与 Single Source of Truth）
├── skill/                # 核心下沉规范
│   ├── reconstruction.md # 权威资产 Schema、逆向重构规范与动态管线
│   ├── image-generation.md# 三级图像能力路由与生成算子
│   ├── workflow.md       # 三模式驱动八阶段状态机
│   ├── safety.md         # 学术真实性底线、工具适配与 IP 自查
│   └── output-spec.md    # Stage-Centric Word 文档数据驱动装配标准
├── templates/            # competition-statement / prompt-record / evidence-checklist
├── adapters/             # Cursor / Codex / Windsurf / Claude 轻量适配层
├── scripts/              # build_docx / reconstruct_assets / scan_placeholders / check_consistency / install
├── examples/             # final-image-only / minimal-example / full-example (开发与回归基准)
└── tests/                # 自动化回归测试套件
```

### 2. 安装后运行时结构（Installed Runtime Layout）

安装至 `~/.gemini/config/skills/`、`~/.agents/skills/` 或 `~/.cursor/skills/` 后的精简运行时：

```text
├── SKILL.md              # 运行时主入口
├── skill/                # 核心执行规则
├── templates/            # 渲染模板库
├── adapters/             # 各宿主适配层
├── scripts/              # 运行时构建器与本地兜底脚本
├── README.md             # 说明文档
└── LICENSE               # 开源许可
```

---

## 安装

### Google Antigravity（AGY）

```powershell
.\scripts\install.ps1 -Platform antigravity
```

### Codex

```powershell
.\scripts\install.ps1 -Platform codex
```

### Cursor

```powershell
.\scripts\install.ps1 -Platform cursor
```

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

## License

MIT
