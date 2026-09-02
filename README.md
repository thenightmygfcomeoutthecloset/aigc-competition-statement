# AIGC Competition Statement

> **上传一张最终 AI 作品，即可自动分析画面、逆向重建合理创作流程、生成必要的复现垫图与阶段结果，并输出结构完整的 AIGC 创作说明文档。**

[![version](https://img.shields.io/badge/version-0.2.1-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

面向大广赛、大学生新媒体创意节、学院奖等高校创意竞赛的 AIGC 创作说明书 Agent Skill。

---

## 核心三工作模式

Agent 接收作品后根据已有材料自动选择最适工作模式：

| 模式 | 适用场景 | 核心机制 |
|---|---|---|
| **Reconstruction Mode（逆向重构模式）** | **用户仅提供一张最终作品**，或创作过程材料严重缺失 | 自动进行画面多维深度分析、推导合理创作管线、实际调用图像工具逆向生成复现垫图（如手绘草图/线稿）与阶段视觉结果、构建具备前后因果关系的演进 Prompt（V1/V2）与建议参数范围，输出 Stage-Centric 竞赛说明书。**绝不停止流程逼问用户补齐材料。** |
| **Hybrid Mode（混合重构模式）** | 用户提供了部分真实材料（如仅有工具名或口述思路，缺少草图或Prompt） | 真实材料归为 `[Verified]` / `[User-reported]`；**仅对缺失环节启动重构**，绝不生成冗余替代品覆盖真实证据。 |
| **Evidence Mode（真实证据模式）** | 用户已保存完整原始 Prompt、垫图、截图与参数 | 直接归档整理真实材料，严格证据分级，不生成任何替代性材料。 |

> **真实性底线**：Reconstructed 内容在文档中均明确标为复现建议，绝不伪充真实历史记录。

---

## 阶段证据链架构（Stage-Centric）

文档彻底抛弃机械按“截图类型”罗列的旧方式，全面以 **创作阶段** 为核心单元，贯穿闭环证据链：

$$\text{Input (输入素材/垫图)} \longrightarrow \text{Tool (工具)} \longrightarrow \text{Prompt (提示词)} \longrightarrow \text{Parameters (参数)} \longrightarrow \text{Output (阶段结果)} \longrightarrow \text{Adjustment (调整说明)}$$

### 七大标准文档章节
1. **作品基本信息**（作品名、赛事、类型、主题、AIGC技术路径）
2. **创作构思**（选题立意、视觉思路、设计目标、人机协同目的）
3. **阶段性创作过程**（核心证据链：阶段1构图规划 → 阶段2基础生成 → 阶段3迭代深化 → 阶段4后期整合）
   - **条件性后期输出**：有真实后期证据才输出后期阶段并标为 Verified/User-reported；无后期证据则如实说明纯 AI 直出，**严禁强加 Photoshop 图层操作与假截图**。
4. **AIGC 工具使用说明与人机协同分工**（工具矩阵与主观能动性分工）
5. **全流程 Prompt、输入素材与参数汇总表**（单层完整对照大表）
6. **版权、素材来源与原创性说明**（知识产权排查；未确认时标注 `Requires User Confirmation`）
7. **复现材料特别说明**（包含 Reconstructed 内容时必带的学术免责声明）

---

## 30 秒快速预览（单图启动流程）

```text
用户：
比赛：第十届大学生新媒体创意节
作品名：《深林微光》
[仅上传一张成图 final.png，无原始 Prompt，无草图，无参数记录]

Skill：
→ 检测到仅有成图，自动进入 Reconstruction Mode (不停止、不逼问)
→ 深度结构化解构画面 (构图、透视、色彩、光照、材质与技术路径)
→ 推导合理管线：构图草图 → 线稿控制生图 (V1) → 提示词光影深化 (V2)
→ 调用生图能力实际渲染生成 01_reconstructed_sketch.png (粗糙铅笔草图)
→ 调用生图能力实际渲染生成 02_reconstructed_generation_v1.png (阶段缺陷初稿)
→ 依据初稿瑕疵针对性生成演进 Prompt V2 (解决体积光与微晶质感)
→ 给出建议复现参数范围 (Seed 标为未记录，严禁编造)
→ 判定为纯生图直出流程，不编造虚假 Photoshop 阶段与假截图
→ 执行版权自查与 Submission Check
→ 生成标准格式 Stage-Centric Word 说明书并导出清空元数据的文档
```

---

## 真实性原则与证据分级（Evidence Levels）

$$\text{[Verified]} > \text{[User-reported]} > \text{[Reconstructed]} > \text{[Unknown]}$$

- `[Verified]`：文件、截图、草图原件或元数据直接证明，直接客观陈述。
- `[User-reported]`：创作者口头表述，使用引述语气。
- `[Reconstructed]`：基于最终作品逆向推导生成的垫图、阶段稿、Prompt 或参数建议，明确标为复现内容。
- `[Unknown]`：无法确认的信息，如实标注“未记录”或留空。

### 五大反伪造铁律
1. **不伪造历史 Prompt**：缺失时仅提供演进复现建议并醒目标记。
2. **不虚构历史参数**：Seed、Steps、CFG、精确模型等无记录即标为“未记录”，严禁编造虚假随机种子。
3. **严禁生成假软件界面**：禁止用生图工具生成假 Photoshop 图层截图、ComfyUI 节点截图或 WebUI 历史截屏来冒充操作证据！
4. **不把推测冒充事实**：成品分析与客观历史记录严格分级隔离。
5. **不擅自臆测具体模型**：绝不得仅凭视觉画面推测具体商业模型或 LoRA。

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

在 Cursor 中通过 `/aigc-competition-statement` 调用；在 AGY 等平台中直接上传作品并提出参赛文案需求即可自动激活。

---

## 目录结构

```text
├── SKILL.md              # 规范入口（三模式路由定义与 Single Source of Truth）
├── skill/                # 核心下沉规范
│   ├── reconstruction.md # 逆向重构模式、创作管线推导与演进 Prompt 规范
│   ├── image-generation.md# 逆向图像生成算子、视觉链要求与 Fallback 机制
│   ├── workflow.md       # 模式驱动的八阶段详细工作流
│   ├── safety.md         # 真实性底线、禁止假软件截图、IP 审查与素材分类
│   └── output-spec.md    # Stage-Centric Word 文档输出与排版标准
├── templates/            # 通用说明书、Prompt 记录、报告和检查清单
├── adapters/             # Cursor / Codex / Windsurf / Claude 轻量适配层
├── examples/             # final-image-only / minimal-example / full-example
└── scripts/              # Windows 与 macOS/Linux 自动化安装器
```

## License

MIT
