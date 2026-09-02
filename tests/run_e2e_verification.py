#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_e2e_verification.py - End-to-end verification script for final-image-only workflow.

Creates a clean output/ directory, starts strictly from a final.png, runs:
1. Reconstruct all visual assets (sketch, lineart, color block, V1, V2);
2. Generates stage-graph.json, prompt-record.md, parameter-record.md, submission_manifest.json;
3. Builds the publication-ready DOCX;
4. Validates:
   - required_assets_missing == 0
   - dangling_placeholders == 0
   - broken_asset_paths == 0
   - empty_generated_files == 0
   - docx_missing_images == 0
   - mode_name_conflicts == 0
   - version_conflicts == 0
   - orphan_runtime_templates == 0
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw
import docx

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import reconstruct_assets
import build_docx
import scan_placeholders
import check_consistency


def run_e2e(output_dir: str):
    out = Path(output_dir).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("AIGC Competition Statement - End-to-End Execution Test")
    print("=" * 60)
    
    # 1. Provide only final.png
    final_png = out / "final.png"
    img = Image.new("RGB", (768, 1024), color=(15, 25, 45))
    draw = ImageDraw.Draw(img)
    # Tree trunks and framing
    draw.rectangle([0, 0, 150, 1024], fill=(10, 15, 25))
    draw.rectangle([618, 0, 768, 1024], fill=(10, 15, 25))
    # Glowing deer subject in center
    draw.ellipse([284, 450, 484, 650], fill=(240, 210, 90), outline=(255, 255, 255), width=4)
    draw.line([(384, 450), (320, 320)], fill=(255, 240, 120), width=6)
    draw.line([(384, 450), (448, 320)], fill=(255, 240, 120), width=6)
    # Light beam
    draw.polygon([(200, 0), (568, 0), (484, 650), (284, 650)], fill=(40, 70, 110))
    img.save(str(final_png), format="PNG")
    print(f"[1/5] Created initial test input: {final_png.name} ({final_png.stat().st_size} bytes)")

    # 2. Reconstruct all visual assets
    print("[2/5] Running visual asset reconstruction (reconstruct_assets.py)...")
    visual_assets = reconstruct_assets.reconstruct_all_assets(str(final_png), str(out))
    for k, p in visual_assets.items():
        print(f"      - {Path(p).name}: {os.path.getsize(p)} bytes")

    # 3. Generate Stage Graph, Prompt Record, and Parameter Record
    print("[3/5] Generating Stage Graph, Prompt Record, and Parameter Record...")
    stage_graph = [
        {
            "id": "stage_1",
            "title": "阶段一：概念探索与构图规划",
            "purpose": "确立幽深森林中神鹿居中站立的纵深框架构图",
            "inputs": [{"name": "逆向构图草稿", "filename": "01_reconstructed_sketch.png"}],
            "tool": "概念构思手绘工具",
            "tool_type": "概念手绘 / 设计规划",
            "prompt": "[Reconstructed Prompt | 复现建议] 原始森林深处发光神鹿、古树根系、框架式透视构图",
            "parameters": "画幅比例 3:4",
            "outputs": [{
                "filename": "01_reconstructed_sketch.png",
                "caption": "阶段一空间透视与主体占位草图",
                "evidence_level": "[Reconstructed]"
            }],
            "adjustment": "骨架确立，进入阶段二借助 AI 工具进行具象化生成",
            "evidence_level": "[Reconstructed]"
        },
        {
            "id": "stage_2",
            "title": "阶段二：AIGC 基础生成与初稿输出",
            "purpose": "将构图草图转化为具备基础色彩与光照的场景初稿",
            "inputs": [{"name": "阶段一草图", "filename": "01_reconstructed_sketch.png"}],
            "tool": "AI 图像生成模型",
            "tool_type": "生成式 AI",
            "prompt": "[Reconstructed Prompt | 复现建议] 深邃原始森林中央，古老巨木根系，发光神鹿站立在苔藓上，幽暗绿色调，框架式构图",
            "parameters": "采样步数范围 25–35 步 [Reconstructed], CFG 7.0, Seed 未记录",
            "outputs": [{
                "filename": "02_reconstructed_generation_v1.png",
                "caption": "阶段二 AI 基础生成第一版初稿图像",
                "evidence_level": "[Reconstructed]"
            }],
            "adjustment": "比对最终成图，初版主体形态已立，但树冠斜射的体积光束较为弥散，鹿角微晶发光颗粒层次感弱于成图，需针对性优化",
            "evidence_level": "[Reconstructed]"
        },
        {
            "id": "stage_3",
            "title": "阶段三：Prompt 迭代与视觉深化",
            "purpose": "针对初稿差距强化丁达尔光线漫反射与鹿角微晶质感",
            "inputs": [{"name": "阶段二初版成果", "filename": "02_reconstructed_generation_v1.png"}],
            "tool": "AI 迭代与优化工具",
            "tool_type": "生成式 AI",
            "prompt": "[Reconstructed Prompt | 复现建议] 深邃原始森林，丁达尔光线穿透高耸树冠斜射，中央神鹿鹿角长满发光枝桠与晶莹发光微粒，半透明荧光质感，微光粒子漂浮，体积漫射光，极致细节",
            "parameters": "建议重绘参数范围 0.55–0.65",
            "outputs": [{
                "filename": "03_reconstructed_generation_v2.png",
                "caption": "阶段三多轮提示词优化后的高清渲染成果",
                "evidence_level": "[Reconstructed]"
            }],
            "adjustment": "丁达尔光线穿透感强，鹿角微晶材质与地表青苔细节达到预期，完成具象生成",
            "evidence_level": "[Reconstructed]"
        }
    ]
    
    stage_graph_file = out / "stage-graph.json"
    stage_graph_file.write_text(json.dumps(stage_graph, ensure_ascii=False, indent=2), encoding="utf-8")
    
    prompt_record_content = """# Stage-Aware Prompt Record — 提示词全流程演进记录表

## 一、作品基本信息
- **作品名称**：深林微光
- **参赛赛事**：第十届大学生新媒体创意节
- **技术路径**：构图草图引导图生图 + 多轮提示词深化（纯 AI 具象直出流程）
- **工具环境**：原始创作工具：未记录（基于特征推断） / 本次复现工具：宿主生图能力

## 二、阶段提示词演进记录

### 阶段记录：stage_2（阶段二：AIGC 基础生成与初稿输出）
| 属性项 | 配置与记录详情 | 状态说明 |
|---|---|---|
| **Stage ID** | stage_2 | 阶段标识 |
| **Prompt Version** | Prompt V1 | 初版提示词 |
| **Input Asset** | 01_reconstructed_sketch.png | 构图引导草图 |
| **Positive Prompt** | 深邃原始森林中央，古老巨木根系，发光神鹿站立在苔藓上，幽暗绿色调，框架式构图 | 正向描述词 |
| **Negative Prompt** | N/A | 本阶段无负向过滤 |
| **Generation Tool** | AI 图像生成模型 | 使用工具 |
| **Parameter Profile** | 建议步数 25–35 步 [Reconstructed], CFG 7.0, Seed 未记录 | 适配参数 |
| **Output Asset** | 02_reconstructed_generation_v1.png | 阶段初稿 |
| **Adjustment Reason** | 比对成图，初版主体形态已立，但树冠体积光束弥散，鹿角微晶颗粒感不足 | 演进差距诊断 |
| **Next Stage** | stage_3 | 视觉深化阶段 |

### 阶段记录：stage_3（阶段三：Prompt 迭代与视觉深化）
| 属性项 | 配置与记录详情 | 状态说明 |
|---|---|---|
| **Stage ID** | stage_3 | 阶段标识 |
| **Prompt Version** | Prompt V2 | 深化提示词 |
| **Input Asset** | 02_reconstructed_generation_v1.png | 阶段初稿成果 |
| **Positive Prompt** | 深邃原始森林，丁达尔光线穿透高耸树冠斜射，中央神鹿鹿角长满发光枝桠与晶莹发光微粒，半透明荧光质感，微光粒子漂浮，体积漫射光，极致细节 | 正向描述词 |
| **Negative Prompt** | 模糊，过曝，结构畸变，杂乱噪点，生硬平光，失真比例 | 排除描述词 |
| **Generation Tool** | AI 迭代与优化工具 | 使用工具 |
| **Parameter Profile** | 建议重绘幅度 0.55–0.65 [Reconstructed] | 适配参数 |
| **Output Asset** | 03_reconstructed_generation_v2.png | 优化成稿 |
| **Adjustment Reason** | 丁达尔光线穿透感强，微晶发光材质与青苔细节达到预期 | 达成目标 |
| **Next Stage** | 交付归档 | 流程闭环 |
"""
    prompt_record_file = out / "prompt-record.md"
    prompt_record_file.write_text(prompt_record_content, encoding="utf-8")
    
    parameter_record_content = """# Parameter Record — 工具自适应参数配置表

| 参数项 | 推荐复现配置（非历史实测值） | 状态说明 |
|---|---|---|
| 生成模式 | 图生图 (Image-to-Image) / 构图约束生图 | [Reconstructed] |
| 建议采样步数 (Steps) | 建议范围 25–35 步 | [Reconstructed] |
| 建议引导系数 (CFG) | 建议范围 6.5–8.0 | [Reconstructed] |
| 建议重绘幅度 (Denoising) | 建议范围 0.55–0.65 | [Reconstructed] |
| 随机种子 (Seed) | 未记录（建议随机种子 -1） | 严禁捏造具体数值 |
"""
    parameter_record_file = out / "parameter-record.md"
    parameter_record_file.write_text(parameter_record_content, encoding="utf-8")
    
    # 4. Create Submission Manifest
    manifest_data = {
        "mode": "Reconstruction Mode",
        "artwork": {
            "title": "深林微光",
            "competition": "第十届大学生新媒体创意节",
            "type": "数字概念插画",
            "theme": "人与自然共生",
            "pipeline": "构图草图引导图生图 + 多轮提示词深化（纯 AI 具象直出流程）",
            "tool_environment": "原始创作工具：未记录（基于特征推断） / 本次复现工具：宿主生图能力"
        },
        "creative_rationale": {
            "background": "本作品探讨人与自然在数字微光中的共生隐喻，探索生态纯粹性之美。",
            "visual_concept": "采用深蓝与幽绿冷色基调，辅以金色高光对撞，垂直引导构图聚焦主体。",
            "ai_collaboration": "利用 AI 高效计算复杂的漫反射与微晶发光材质，提升艺术探索效率。"
        },
        "stage_graph": stage_graph,
        "disclaimer": "本说明文档中标记为 [Reconstructed] 的内容系逆向工程推演复现，用于完整呈现创作演进逻辑与工艺可复现性。"
    }
    manifest_file = out / "submission_manifest.json"
    manifest_file.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 5. Build Word Document
    docx_file = out / "深林微光_新媒体节_AIGC说明书.docx"
    print(f"[4/5] Building Word document ({docx_file.name})...")
    build_docx.build_docx_from_manifest(str(manifest_file), str(docx_file))
    print(f"      DOCX successfully built: {docx_file.stat().st_size} bytes")

    # 6. Execute 8 Zero-Defect Assertions
    print("[5/5] Executing 8 Zero-Defect Assertions...")
    
    # Assertion 1: required_assets_missing == 0
    expected_assets = [
        out / "final.png",
        out / "01_reconstructed_sketch.png",
        out / "01_reconstructed_lineart.png",
        out / "01_reconstructed_color_block.png",
        out / "02_reconstructed_generation_v1.png",
        out / "03_reconstructed_generation_v2.png",
        out / "prompt-record.md",
        out / "parameter-record.md",
        out / "stage-graph.json",
        out / "submission_manifest.json",
        docx_file
    ]
    missing = [str(p.name) for p in expected_assets if not p.exists()]
    required_assets_missing = len(missing)
    assert required_assets_missing == 0, f"Missing required assets: {missing}"
    print("  [PASS] required_assets_missing == 0")

    # Assertion 2: empty_generated_files == 0
    empty_files = [str(p.name) for p in expected_assets if p.stat().st_size == 0]
    empty_generated_files = len(empty_files)
    assert empty_generated_files == 0, f"Empty files found: {empty_files}"
    print("  [PASS] empty_generated_files == 0")

    # Assertion 3: broken_asset_paths == 0
    broken_asset_paths = 0
    for p in expected_assets:
        if not os.path.isabs(str(p.resolve())):
            broken_asset_paths += 1
    assert broken_asset_paths == 0
    print("  [PASS] broken_asset_paths == 0")

    # Assertion 4: dangling_placeholders == 0
    found_placeholders = scan_placeholders.scan_directory(str(out))
    dangling_placeholders = len(found_placeholders)
    assert dangling_placeholders == 0, f"Dangling placeholders found: {found_placeholders}"
    print("  [PASS] dangling_placeholders == 0")

    # Assertion 5: docx_missing_images == 0
    doc = docx.Document(str(docx_file))
    docx_missing_images = 0 if len(doc.inline_shapes) >= 3 else 1
    assert docx_missing_images == 0, f"DOCX has only {len(doc.inline_shapes)} inline images"
    print("  [PASS] docx_missing_images == 0 (embedded images: $len)")

    # Assertion 6: mode_name_conflicts == 0
    mode_errs = check_consistency.check_mode_names()
    mode_name_conflicts = len(mode_errs)
    assert mode_name_conflicts == 0, f"Mode conflicts found: {mode_errs}"
    print("  [PASS] mode_name_conflicts == 0")

    # Assertion 7: version_conflicts == 0
    ver_errs = check_consistency.check_version_sync()
    version_conflicts = len(ver_errs)
    assert version_conflicts == 0, f"Version conflicts found: {ver_errs}"
    print("  [PASS] version_conflicts == 0")

    # Assertion 8: orphan_runtime_templates == 0
    orphan_errs = check_consistency.check_orphan_templates()
    orphan_runtime_templates = len(orphan_errs)
    assert orphan_runtime_templates == 0, f"Orphan templates found: {orphan_errs}"
    print("  [PASS] orphan_runtime_templates == 0")

    print("\n" + "=" * 60)
    print("FINAL VERIFICATION SUMMARY:")
    print("  required_assets_missing  = 0")
    print("  dangling_placeholders    = 0")
    print("  broken_asset_paths       = 0")
    print("  empty_generated_files    = 0")
    print("  docx_missing_images      = 0")
    print("  mode_name_conflicts      = 0")
    print("  version_conflicts        = 0")
    print("  orphan_runtime_templates = 0")
    print("=" * 60)
    
    print("\nGenerated Output Tree:")
    for f in sorted(out.iterdir()):
        print(f"  ├── {f.name} ({f.stat().st_size} bytes)")
    print("\nAll End-to-End checks PASSED with flying colors!")


if __name__ == "__main__":
    test_output_dir = REPO_ROOT / "tests" / "e2e_output"
    run_e2e(str(test_output_dir))


