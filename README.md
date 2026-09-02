# AIGC Competition Statement

> 上传一张最终 AI 作品，自动分析画面、逆向整理创作流程、复现必要的 Prompt、垫图与阶段性结果，并生成结构完整的 AIGC 创作说明文档。

[![version](https://img.shields.io/badge/version-0.2.0-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

面向大广赛、大学生新媒体创意节、学院奖等高校创意竞赛的 AIGC 创作说明书 Agent Skill。

原始材料存在时优先采用真实记录（Evidence Mode）；缺失材料时自动进入逆向重构模式（Reconstruction Mode）。所有复现内容均严格醒目标记，绝不与真实历史记录混淆。

---

## 核心双模式

| 模式 | 适用场景 | 核心能力 |
|---|---|---|
| **Reconstruction Mode（逆向重构模式）** | **用户仅提供一张最终作品**，或创作过程材料严重缺失 | 自动进行画面多维结构化分析、推导合理创作管线、逆向生成复现垫图（如手绘草图/线稿）、阶段视觉结果、演进 Prompt（V1/V2/V3）与参数建议，组织完整说明书。 |
| **Evidence Mode（真实证据模式）** | 用户已保存原始 Prompt、垫图、截图或参数 | 直接归档整理真实材料，严格分级，不生成任何非必要的替代材料。 |

---

## 核心证据链架构（Stage-Centric）

文档以 **创作阶段** 为核心单元，贯穿严密的闭环证据链：

$$\text{Input (输入素材/垫图)} \longrightarrow \text{Tool (工具)} \longrightarrow \text{Prompt (提示词)} \longrightarrow \text{Parameters (参数)} \longrightarrow \text{Output (阶段结果)} \longrightarrow \text{Adjustment (调整说明)}$$

### 文档七大标准章节
1. **作品基本信息**（作品名、类型、主题、AIGC技术类型）
2. **创作构思**（选题动机、视觉思路、设计目标、协同目的）
3. **阶段性创作过程**（阶段1构思规划 → 阶段2基础生成 → 阶段3迭代深化 → 阶段4人工后期）
4. **AIGC 工具使用说明**（全流程工具链与人机协同职责切分）
5. **Prompt、输入素材与参数汇总表**（全流程单层大表）
6. **版权、素材来源与原创性说明**（知识产权自查与原创声明）
7. **复现材料特别说明**（包含 Reconstructed 内容时的官方免责说明）

---

## 30 秒快速预览（Reconstruction Mode）

```text
用户：
比赛：第十届大学生新媒体创意节
作品名：《未来之声》
[仅上传一张最终成图，无原始 Prompt，无垫图，无参数记录]

Skill：
→ 读取比赛规则与格式规范
→ 深度结构化分析画面（构图、色彩、透视、光影、材质与生成路径）
→ 推导创作流程：构图草稿 → 线稿控制生图 (V1) → 光影优化 (V2) → PS精修
→ 逆向生成复现输入垫图（01_reconstructed_sketch 构图草图）
→ 逆向生成演进 Prompt（V1 基础主体 → V2 全息光效与体积光）
→ 给出推荐复现参数并注明非历史实测值
→ 执行版权/IP 审查与匿名检查
→ 生成标准 Stage-Centric Word 说明书并导出清空元数据的文档
```

---

## 真实性原则与证据分级（Evidence Levels）

$$\text{[Verified]} > \text{[User-reported]} > \text{[Reconstructed]} > \text{[Unknown]}$$

- `[Verified]`：文件、截图、草图或元数据直接证明，直接陈述。
- `[User-reported]`：创作者口述，使用引述语气。
- `[Reconstructed]`：基于最终作品逆向分析生成的垫图、阶段稿、Prompt 或参数建议，明确标为复现内容，非原始历史记录。
- `[Unknown]`：无法确认的信息，如实标注“未记录”或留空。

### 四大反伪造红线
- **不伪造历史 Prompt**：缺失时仅提供演进复现建议并醒目标记。
- **不虚构历史参数**：Seed、Steps、CFG、精确模型等无记录即标为“未记录”，严禁编造虚假种子。
- **不把推测冒充事实**：成品分析与客观历史记录严格分级隔离。
- **不擅自臆测具体模型**：绝不得仅凭视觉画面推测具体商业模型或 LoRA。

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

支持 `-DryRun` 预览与安全归档卸载：

```powershell
.\scripts\install.ps1 -Platform antigravity -DryRun
.\scripts\install.ps1 -Platform antigravity -Uninstall
```

---

## 调用方式

在 Codex 中输入：
```text
$aigc-competition-statement 帮我整理这件作品的 AIGC 创作说明。
比赛：第十八届大广赛
（上传最终作品图）
```

在 Cursor 中通过 `/aigc-competition-statement` 调用；在 AGY 等平台中直接上传图片并提出参赛文案需求即可自动激活。

---

## 目录结构

```text
├── SKILL.md              # 规范入口（双模式定义与 Single Source of Truth）
├── skill/                # 核心下沉规范
│   ├── reconstruction.md # 逆向重构模式、垫图生成与阶段视觉链规范
│   ├── workflow.md       # 详细 8 阶段执行流程
│   ├── safety.md         # 真实性红线、版权/IP 审查与素材分类
│   └── output-spec.md    # Stage-Centric Word 文档输出规范
├── templates/            # 通用说明书、Prompt 记录、报告和检查清单
├── adapters/             # Cursor / Codex / Windsurf / Claude 轻量适配层
├── examples/             # minimal-example / full-example 实战样例
└── scripts/              # Windows 与 macOS/Linux 自动化安装器
```

## License

MIT
