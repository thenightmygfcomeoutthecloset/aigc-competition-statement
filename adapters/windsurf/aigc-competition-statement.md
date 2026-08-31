# Windsurf Adapter

This file provides ready-to-use rules for Windsurf (Codeium).

**Installation**: Place this file at `.windsurf/rules/aigc-competition-statement.md` in your project root.

---

```markdown
# AIGC 竞赛创作说明书生成技能

## 触发条件

当用户提到以下内容时激活：
- AIGC 创作说明 / AI 声明 / 比赛 AI 说明
- 大广赛 / 新媒体节 / 新媒体创意节 / 学院奖
- AIGC 说明书 / Prompt 记录 / 比赛 AI 技术报告

不触发：普通文案任务、与竞赛无关的 AI 使用问题。

## Evidence Levels（核心机制）

处理任何信息前，先判断其可信等级：

- [Verified]：用户提供了文件/截图/元数据 → 直接陈述
- [User-reported]：用户口头说明 → "据创作者表述……"
- [Reconstructed]：从作品图推断 → "以下为复现建议，基于视觉分析……"
- [Unknown]：无法确认 → 留空或写"未记录"

## 禁止事项

绝对不得自动填写：
Seed / Steps 具体值 / CFG 具体值 / Sampler 名称 / 模型版本号 /
LoRA 权重 / 原始 Prompt（除非用户提供）/ 创作日期 / 软件版本号

Prompt 复现建议 ≠ 原始 Prompt，必须在文档中明确区分。

## 工作流程

1. 查找赛事要求（搜索/读取文件）
2. 收集素材并分级
3. 分析作品图（[Reconstructed] 标注）
4. 整理创作过程叙述
5. 生成 Prompt 复现建议（仅在无原始 Prompt 时）
6. 生成 Word 文档（无 AI 排版格式痕迹）
7. 合规检查（匿名 + 真实性）
8. 导出打包

## 文档格式要求

- 白纸黑字，Word 标准样式
- 禁止：灰色代码块 / 蓝色超链接 / 英文样式名 / 边框阴影
```