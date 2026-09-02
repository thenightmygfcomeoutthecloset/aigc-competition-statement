# 通用竞赛创作说明书主模板（Stage-Centric 数据驱动版）

> 本模板由数据驱动引擎（`scripts/build_docx.py`）消费 `stage_graph` 动态循环渲染。
> 权威资产清单直接引用 [skill/reconstruction.md](skill/reconstruction.md)。

---

**【{artwork.title}】AIGC 创作过程说明书**

---

## 一、作品基本信息

- **作品名称**：{artwork.title}
- **参赛赛事**：{artwork.competition}
- **作品类型**：{artwork.type}
- **创作主题**：{artwork.theme}
- **AIGC 核心技术路径**：{artwork.pipeline}
- **工具环境说明**：{artwork.tool_environment}

---

## 二、创作构思与立意

### 1. 创作背景与选题动机
{creative_rationale.background}

### 2. 视觉设计思路与设计目标
{creative_rationale.visual_concept}

### 3. AIGC 工具协同目的
{creative_rationale.ai_collaboration}

---

## 三、阶段性创作过程

> 本章节基于动态阶段管线（Dynamic Stage Graph），完整呈现“输入素材 → 生成工具 → 提示词 → 参数配置 → 阶段结果 → 调整优化”的自洽闭环证据链。

<!-- REPEATABLE_STAGE_BLOCK: 针对 stage_graph 中的每个阶段循环渲染 -->
### 3.{stage.index} {stage.title}

- **创作目的**：{stage.purpose}
- **输入素材**：{stage.inputs}
- **使用工具**：{stage.tool}
- **提示词配置**：
```
{stage.prompt}
```
- **配置参数**：{stage.parameters}
- **阶段生成结果**：
{此处嵌入当前阶段 outputs 中的图片，由脚本真实嵌入}
_图 {figure.index} {output.caption} ({output.evidence_level})_
- **调整说明与优化方向**：{stage.adjustment}
- **证据等级**：{stage.evidence_level}
<!-- END_REPEATABLE_STAGE_BLOCK -->

---

## 四、AIGC 工具使用说明与人机协同分工

### 1. 核心工具链矩阵（由 stage_graph 自动生成）

| 制作阶段 | 采用工具 | 工具属性 | 具体作用 |
|---|---|---|---|
<!-- 循环生成各阶段工具行 -->
| {stage.title} | {stage.tool} | {stage.tool_type} | {stage.purpose} |

### 2. 人机协同职责划分

- **人类创作者主导环节**：提出作品核心立意与隐喻；规划画面骨骼、空间透视与构图引导；编写并迭代提示词演进策略；把控最终审美标准。
- **AI 工具协同辅助环节**：高效执行物理光线漫反射计算与环境细节生成；协助完成从初稿到深化稿的高清渲染迭代。

---

## 五、全流程 Prompt、输入素材与参数汇总表（由 stage_graph 自动生成）

| 创作阶段 | 输入素材 (Input) | 采用工具 (Tool) | 提示词 (Prompt) | 参数与产出 (Output) |
|---|---|---|---|---|
<!-- 循环生成各阶段汇总行 -->
| {stage.title} | {stage.inputs} | {stage.tool} | {stage.prompt} | {stage.parameters} / {stage.outputs} |

---

## 六、版权、素材来源与原创性说明

1. **作品原创性承诺**：本作品由创作者自主完成构思、构图规划与提示词设计，作品内容积极向上，不含任何违法违规信息，无知识产权争议与权属纠纷。
2. **输入素材来源陈述**：创作全流程中使用的草图构想系创作者自主原创规划，未引入未经授权的第三方商用摄影图或专属素材。
3. **知识产权自查结论**：画面中未出现未经授权的第三方商业 Logo、商标或受保护影视动漫专属形象，字体与美术要素符合赛事合规要求。

---

## 七、复现材料特别说明

> **【重要说明】**  
> 本说明文档中标记为 `[Reconstructed]` 的草图构图、阶段演进过程图、提示词演进及推荐配置参数，系因创作者创作过程中部分原始中间过程文件未作完整留存，由 AI 辅助分析系统根据最终作品的视觉与工程特征进行逆向工程分析和复现构建。其核心目的在于完整展示作品的技术路线、构思演进逻辑与工艺可复现性，并不代表创作当时保存的原始物理历史记录。
