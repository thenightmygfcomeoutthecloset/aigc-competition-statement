# AIGC 竞赛创作说明书生成技能

> 只需提供最终作品图，即可自动反推 Prompt、生成工作流描述，并输出符合比赛标准的 AIGC 创作过程说明书（Word 格式）。

适用赛事：大广赛、大学生新媒体创意节、学院奖等国内高校创意竞赛。

## 核心能力

- ✅ 从成品图反推生成合理的 Prompt（正向 + 负向）和参数
- ✅ 自动生成 ComfyUI / SD / Midjourney / DALL-E 工作流描述
- ✅ 按国内竞赛标准模板输出 Word 文档（创意阐释 → AI 技术报告 → 过程截图）
- ✅ 自动匿名检查、格式验收、ZIP 打包

## 各平台使用方法

### Google Antigravity (AGY)

技能会自动被发现和激活，无需额外操作。

手动安装：把本仓库 clone 到以下任一位置：
```
# 全局（所有项目生效）
~/.gemini/config/skills/aigc-competition-statement/

# 项目级（仅当前项目生效）
你的项目/.agents/skills/aigc-competition-statement/
```

### OpenAI Codex / ChatGPT

1. 复制 [`SKILL.md`](./SKILL.md) 的全部内容（忽略开头的 YAML 部分）
2. 粘贴到 Codex 的 **Setup Instructions** 或 ChatGPT 的 **Custom Instructions** 中
3. 然后直接说"帮我写比赛的 AI 创作说明"即可

### Claude (Anthropic)

1. 创建一个 **Project**
2. 把 `SKILL.md` 内容粘贴到 **Project Instructions** 中
3. 上传你的最终作品图，开始对话

### Cursor / Windsurf

```
# Cursor：放到项目根目录
.cursor/rules/aigc-competition-statement.md

# Windsurf：放到项目根目录
.windsurfrules
```

把 `SKILL.md` 的内容（去掉 YAML frontmatter）复制进去即可。

### 其他任何 AI 工具

本质上 `SKILL.md` 就是一份结构化的中文指令文档。
你可以直接把内容粘贴到任何支持自定义 System Prompt 的 AI 工具中使用。

## 使用示例

```
用户：帮我写比赛的 AI 创作说明，我参加的是第十届大学生新媒体节，
     作品图在 E:\竞赛\作品\ 目录下，我用的 ComfyUI + SDXL。

AI：（自动执行 SKILL.md 中的完整流程）
```

## License

MIT
