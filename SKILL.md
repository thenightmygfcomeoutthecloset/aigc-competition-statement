---
name: aigc-competition-statement
description: 为大广赛、大学生新媒体节、学院奖等高校创意竞赛整理真实、可核验的 AIGC 创作说明、AI 使用声明、Prompt 记录和 Word 提交材料；不用于伪造创作历史或普通文案写作。
---

# AIGC 竞赛创作说明书

帮助创作者把已有材料整理为可提交、可追溯的 AIGC 创作说明。先读用户提供的规则、作品、截图和元数据，再提出最多三个必要问题。

## 证据等级

- `[Verified]`：文件、截图或元数据直接证明。可以直接陈述。
- `[User-reported]`：仅由用户口头说明。使用“据创作者表述”等引述语气。
- `[Reconstructed]`：由最终作品推断。必须标明是复现建议，不是原始记录。
- `[Unknown]`：无法确认。留空或写“未记录”。

不得在用户未提供时填写 Seed、Steps、CFG、Sampler、模型精确版本、LoRA 权重、原始 Prompt、日期、软件版本、生成次数或截图细节。

## 工作方式

1. 查找当前赛事官方要求。找不到时继续使用通用草稿，但在文档顶部明确标注“尚未依据官方赛事要求校验”。
2. 为全部事实分配证据等级；创作过程只使用 `[Verified]` 和 `[User-reported]` 信息。
3. 只有缺少原始 Prompt 时才提供复现建议，并写明：
   “以下 Prompt 复现建议基于最终作品视觉分析生成，非创作时原始记录。”
4. 使用 `templates/competition-statement.md` 组织内容，生成 Word 文档后执行匿名、真实性、格式和元数据检查。

## 按需读取

- 执行完整阶段流程时读 [skill/workflow.md](skill/workflow.md)。
- 判断事实、Prompt 复现或匿名风险时读 [skill/safety.md](skill/safety.md)。
- 生成或检查 Word 时读 [skill/output-spec.md](skill/output-spec.md)。
- 生成主文档时使用 [templates/competition-statement.md](templates/competition-statement.md)；提示词记录、极简报告和导出检查分别使用同目录下的对应模板。
