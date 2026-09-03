# AIGC 创作过程说明书模板

本模板只描述字段结构。图片资产、顺序与文件名必须运行时读取 [`schema/canonical-assets.yaml`](../schema/canonical-assets.yaml)。

## 一、作品基本信息

渲染 `artwork` 的标题、赛事、类型、主题和技术路径。

## 二、创作构思与立意

渲染 `creative_rationale`。

## 三、Stage Graph

逐阶段渲染目的、输入/输出资产、版本和对应 Execution Record。Stage 数量随实际 generation 数量变化。

## 四、前期视觉设计 / 输入素材

展示 sketch、lineart、color block 三类前期视觉设计。

## 五、AIGC 完整作品连续版本

按 Execution Records 循环展示 V1…Vn 的输入、Prompt、后端、参数、完整图、Difference Analysis、Adjustment Reason 和 Prompt Evolution。

## 六、Final Artwork

展示 Final 与最后一个 generation version 的继承关系，以及存在的后期处理。

## 七、创作工具说明

渲染用户确认的创作工具；未提供时省略本章。
