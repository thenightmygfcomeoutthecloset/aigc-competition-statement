# Output Specification — Word 文档格式与数据驱动装配规范

> 本文档定义本 Skill 生成的 Word（.docx）说明书的排版标准与数据驱动装配规范。权威资产清单直接引用 [skill/reconstruction.md](reconstruction.md)。

---

## 核心设计哲学

**学术严谨、数据驱动、真实嵌入、完整交付。**

- 生成的说明文档必须呈现出自洽的工程与设计演进闭环；
- **真正数据驱动**：第三章由 `stage_graph` 动态驱动循环渲染，不硬编码固定四阶段；
- **真实图片嵌入**：磁盘中的 PNG 文件通过 `scripts/build_docx.py` 真实嵌入文档，下方紧随楷体学术图注；
- **零占位悬挂**：文档严禁残留任何未替换的花括号模板变量或“待补齐”字样，交付前必须通过 `scripts/scan_placeholders.py` 扫描。

---

## 页面版式与字号规范

- **纸张**：A4 纵向，页边距常规（上下 2.54cm，左右 3.18cm）
- **文档总标题**：小二号（18pt），黑体，加粗，居中
- **一级标题（一、二、三...）**：小三号（15pt），黑体，加粗，段前段后 0.5 行
- **二级标题（1. 2. 3... 或 3.1 3.2...）**：四号（14pt），黑体/楷体，加粗
- **正文**：五号（10.5pt），宋体，1.35 倍行距，首行缩进 2 字符
- **图表与图注**：小五号（9pt），楷体，居中，紧随图表下方

---

## Stage-Centric 标准文档结构（七大章节）

```text
【作品名称】AIGC 创作过程说明书

一、 作品基本信息
   - 作品名称、参赛赛事、作品类型、创作主题、AIGC 核心技术路径
   - 工具环境说明（明确区分原始创作推断与复现执行工具）

二、 创作构思与立意
   - 1. 创作背景与选题动机
   - 2. 视觉设计思路与设计目标
   - 3. AIGC 工具协同目的

三、 阶段性创作过程（由 stage_graph 数据结构动态循环渲染）
   * 对 stage_graph 中的每个阶段遍历输出：*
   3.X 阶段X：{stage.title}
       - 创作目的：{stage.purpose}
       - 输入素材：{stage.inputs}
       - 使用工具：{stage.tool}
       - 提示词配置：{stage.prompt}
       - 配置参数：{stage.parameters}
       - 阶段生成结果：
         [真实嵌入该阶段 outputs 中的 PNG 图片]
         图 X {output.caption} ({output.evidence_level})
       - 调整说明与优化方向：{stage.adjustment}
       - 证据等级：{stage.evidence_level}

四、 AIGC 工具使用说明与人机协同分工
   - 1. 核心工具链矩阵（由 stage_graph 自动生成提取）
   - 2. 人机协同职责划分（人类主导 vs AI 协同）

五、 全流程 Prompt、输入素材与参数汇总表
   - 单层综合大表（由 stage_graph 自动映射整合）

六、 版权、素材来源与原创性说明
   - 1. 作品原创性承诺
   - 2. 输入素材来源陈述
   - 3. 知识产权自查结论

七、 复现材料特别说明
   - 标准学术免责声明（声明复现材料用于完整呈现创作演进逻辑与技术可复现性）
```

---

## 编译与校验流水线（Executable Assembly Pipeline）

1. **装配数据准备**：生成 `submission_manifest.json` 与 `stage_graph.json`；
2. **文档构建**：
   ```bash
   python scripts/build_docx.py --manifest submission_manifest.json --output "{作品名}_{赛事简称}_AIGC说明书.docx"
   ```
3. **占位符校验**：
   ```bash
   python scripts/scan_placeholders.py "{作品名}_{赛事简称}_AIGC说明书.docx"
   ```
4. 校验无误后方可正式交付。
