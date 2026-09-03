# AIGC Competition Statement

[![version](https://img.shields.io/badge/version-0.3.0-blue)](CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

从最终作品、作品分析与用户确认信息生成可审计的过程说明包：视觉复现研究、Prompt/参数记录、Stage Graph、严格 Manifest 和 A4 DOCX。

## v0.3.0 完整作品版本演进

- [`schema/canonical-assets.yaml`](schema/canonical-assets.yaml) 是唯一资产规范；代码、校验、DOCX 和测试都从该文件加载。
- `scripts/run_pipeline.py` 是真实端到端入口，不依赖测试手写某个案例的 Prompt 或 Manifest。
- `scripts/validate_manifest.py` 同时执行 JSON Schema、Pydantic、文件存在性、大小、图片解码和 SHA-256 校验。
- `generation_v1/v2/v3/...` 均为同一幅作品的完整画面快照，必须同时包含主体、背景、构图、色彩和整体空间关系；它们不是不同局部，也不由局部拼接冒充。
- sketch、lineart、color block 仅是前期视觉输入，永远不作为 generation version。
- 每轮先写 Prompt 与 Generation Request，再调用真实生成后端；随后根据实际版本图与 Final 的 Difference Analysis 派生 Adjustment Reason 和下一轮 Prompt Evolution。
- 版本数量由收敛诊断动态决定，支持 `V1 → Final`、`V1 → V2 → Final`、`V1 → V2 → V3 → Final`。默认最大三轮，Schema 设置绝对上限防止无限循环。
- 未配置真实后端时明确返回 `generation_backend_unavailable`，绝不使用 Final 滤镜、模糊、混合、降质或 OpenCV 操作伪造 V1/V2。
- 版权、原创性和原始工具来自用户确认；没有确认时写“未核验”，不做默认承诺。
- DOCX 按机器 Schema 嵌入全部规范图片，并渲染 Prompt Record 与 Parameter Record；表格使用固定列宽，竖图同时受页面宽高限制。
- 安装包包含脚本、Schema、依赖清单和 OFL 授权的 Noto Sans SC 字体。

## 安装依赖

```bash
python -m pip install -r requirements.txt
```

完整 DOCX 渲染回归还需要 LibreOffice。安装脚本会安装随包分发的 Noto Sans SC 用户字体。

## 运行完整流水线

```bash
python scripts/run_pipeline.py \
  --input /path/to/final.png \
  --output-dir /path/to/output \
  --title "作品名称" \
  --competition "赛事名称" \
  --analysis-json /path/to/analysis.json
```

正式运行需要由宿主 Agent 传入 `ImageGenerationBackend`，或设置 `AIGC_IMAGE_GENERATION_COMMAND` 指向实际图像生成适配器。外部适配器从 stdin 接收 JSON request，并按 `AIGC_OUTPUT_PATH` 写入完整结果图。

最小 `analysis.json`：

```json
{
  "subject": "画面主体与环境",
  "composition": "构图与视线组织",
  "palette": "主要色彩关系",
  "theme": "作品主题"
}
```

可选的用户确认示例：

```json
{
  "confirmations": {
    "original_tool": {
      "confirmed": true,
      "value": "创作者确认使用的工具与模型",
      "source": "用户在本次会话中的明确确认"
    }
  }
}
```

## 安装 Skill

```powershell
.\scripts\install.ps1 -Platform codex
```

```bash
bash scripts/install.sh codex
```

## 验证

```bash
python scripts/check_consistency.py
python -m pytest -q
python tests/run_e2e_verification.py
```

## License

MIT。随包字体按 [`assets/fonts/OFL.txt`](assets/fonts/OFL.txt) 分发。
