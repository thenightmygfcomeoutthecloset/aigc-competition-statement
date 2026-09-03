# 图像生成后端与完整版本契约

使用 `scripts/image_generation_backend.py` 的统一接口调用可记录实际工具、模型、输入、Prompt、参数与输出的图像生成后端。适配器可以连接宿主 Agent、OpenAI、Stable Diffusion、SDXL、ComfyUI 或其他提供方，但核心流水线不绑定厂商。

资产 ID、文件名与算子必须从 [`schema/canonical-assets.yaml`](../schema/canonical-assets.yaml) 读取。

## 前期视觉设计

```bash
python scripts/reconstruct_assets.py --input final.png --output-dir output
```

该命令只生成 sketch、lineart、color block。它们表达构图、轮廓、大色块和明暗关系，不是 V1/V2。

## Generation 契约

- 每个 `generation_vN` 都必须是具有主体、背景、构图、色彩和整体关系的完整作品。
- V1 建立基本成立的完整方向，不得人为注入畸形、噪声、模糊或破坏性 artifact。
- V2 及后续版本必须输入上一完整版本，并由实际 Difference Analysis 推动 Prompt Evolution。
- Prompt 和 request JSON 必须先于对应后端调用写入磁盘；成功后写 execution record。
- 若后端不可用，明确返回 `generation_backend_unavailable`。禁止任何滤镜 fallback。
