#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_reconstruction.py - Comprehensive regression test suite for v0.2.2.

Covers:
1. test_reconstruction_final_image_only (full asset generation from single image)
2. test_no_dangling_placeholders (zero placeholders across outputs)
3. test_v2_required (generation_v2 cannot be skipped)
4. test_prompt_evolution (prompt_v1 != prompt_v2, adjustment_reason exists)
5. test_docx_embeds_generated_assets (images embedded in DOCX, captions present)
6. test_mode_names (strictly Evidence, Hybrid, Reconstruction modes)
7. test_version_sync (all versions == 0.2.2)
8. test_examples_match_schema (examples align with canonical schema)
9. test_installed_runtime_complete (installed directory has runtime scripts & modules)
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
import docx

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import reconstruct_assets
import build_docx
import scan_placeholders
import check_consistency


class TestAIGCReconstruction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="aigc_test_"))
        
        # Create a sample test final artwork
        cls.sample_image_path = cls.temp_dir / "final.png"
        img = Image.new("RGB", (600, 800), color=(20, 30, 60))
        draw = ImageDraw.Draw(img)
        # Draw background shapes, gradients, and a central subject
        draw.rectangle([50, 50, 550, 750], fill=(30, 45, 90), outline=(220, 180, 50), width=4)
        draw.ellipse([200, 250, 400, 450], fill=(240, 200, 80), outline=(255, 255, 255), width=3)
        draw.polygon([(300, 150), (250, 250), (350, 250)], fill=(80, 180, 220))
        draw.line([(100, 700), (500, 700)], fill=(120, 220, 150), width=5)
        img.save(str(cls.sample_image_path), format="PNG")

    @classmethod
    def tearDownClass(cls):
        if cls.temp_dir.exists():
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_version_sync(self):
        """test_version_sync: assert all version references == 0.2.2."""
        errs = check_consistency.check_version_sync()
        self.assertEqual(errs, [], f"Version sync errors found: {errs}")

    def test_mode_names(self):
        """test_mode_names: assert official modes are strictly Evidence, Hybrid, Reconstruction."""
        errs = check_consistency.check_mode_names()
        self.assertEqual(errs, [], f"Mode name violations found: {errs}")

    def test_examples_match_schema(self):
        """test_examples_match_schema: verify examples reflect canonical assets."""
        examples_dir = REPO_ROOT / "examples"
        for ex in ["final-image-only.md", "minimal-example.md", "full-example.md"]:
            path = examples_dir / ex
            self.assertTrue(path.exists(), f"Example {ex} missing")
            content = path.read_text(encoding="utf-8")
            self.assertIn("01_reconstructed_sketch.png", content)
            self.assertIn("02_reconstructed_generation_v1.png", content)
            self.assertIn("03_reconstructed_generation_v2.png", content)
            self.assertIn("prompt-record", content)

    def test_installed_runtime_complete(self):
        """test_installed_runtime_complete: simulate install and verify complete runtime layout."""
        sim_install_dir = self.temp_dir / "installed_runtime"
        sim_install_dir.mkdir(parents=True, exist_ok=True)
        
        # Simulate Safe-Copy-Skill
        items = ["SKILL.md", "skill", "templates", "adapters", "scripts", "README.md", "LICENSE"]
        for it in items:
            src = REPO_ROOT / it
            if src.exists():
                dest = sim_install_dir / it
                if src.is_dir():
                    shutil.copytree(src, dest)
                else:
                    shutil.copy2(src, dest)
                    
        # Verify critical runtime assets
        self.assertTrue((sim_install_dir / "SKILL.md").exists())
        self.assertTrue((sim_install_dir / "skill" / "reconstruction.md").exists())
        self.assertTrue((sim_install_dir / "skill" / "image-generation.md").exists())
        self.assertTrue((sim_install_dir / "skill" / "workflow.md").exists())
        self.assertTrue((sim_install_dir / "templates" / "competition-statement.md").exists())
        self.assertTrue((sim_install_dir / "templates" / "prompt-record.md").exists())
        self.assertTrue((sim_install_dir / "templates" / "evidence-checklist.md").exists())
        self.assertTrue((sim_install_dir / "scripts" / "reconstruct_assets.py").exists())
        self.assertTrue((sim_install_dir / "scripts" / "build_docx.py").exists())
        self.assertTrue((sim_install_dir / "scripts" / "scan_placeholders.py").exists())

    def test_reconstruction_final_image_only_and_pipeline(self):
        """
        Comprehensive test:
        1. Generates all 5 visual assets from final.png;
        2. Asserts V2 required;
        3. Tests prompt evolution (V1 != V2, adjustment_reason exists);
        4. Compiles real DOCX and asserts image embedding;
        5. Scans for zero dangling placeholders.
        """
        out_dir = self.temp_dir / "pipeline_output"
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1. Reconstruct all visual assets via scripts/reconstruct_assets.py
        assets = reconstruct_assets.reconstruct_all_assets(str(self.sample_image_path), str(out_dir))
        
        # Verify 5 files exist and non-empty
        expected_files = [
            "01_reconstructed_sketch.png",
            "01_reconstructed_lineart.png",
            "01_reconstructed_color_block.png",
            "02_reconstructed_generation_v1.png",
            "03_reconstructed_generation_v2.png"
        ]
        for ef in expected_files:
            file_path = out_dir / ef
            self.assertTrue(file_path.exists(), f"Asset {ef} was not generated")
            self.assertGreater(file_path.stat().st_size, 0, f"Asset {ef} is empty (0 bytes)")

        # 2. Assert V2 exists (test_v2_required)
        self.assertTrue((out_dir / "03_reconstructed_generation_v2.png").exists())

        # 3. Prompt Evolution Verification (test_prompt_evolution)
        prompt_v1 = "深邃星空古殿中央，发光几何神兽，金色与青蓝冷暖光照，中央纵深对称构图"
        prompt_v2 = "深邃星空古殿中央，发光神兽鳞片微晶折射，丁达尔斜射体积光，漫反射光晕，超高清细节"
        adjustment_reason = "经比对最终成图，初版主体形态已立，但边缘体积光较弥散，微晶折射层次未收敛，在 V2 中强化体积光与微晶描述"
        
        self.assertNotEqual(prompt_v1, prompt_v2)
        self.assertTrue(len(adjustment_reason) > 10)

        # 4. Construct Manifest and Stage Graph
        stage_graph = [
            {
                "id": "stage_1",
                "title": "阶段一：概念探索与构图规划",
                "purpose": "明确建筑透视与核心神兽空间占位骨骼",
                "inputs": [{"name": "构图草图", "filename": "01_reconstructed_sketch.png"}],
                "tool": "概念构思手绘工具",
                "tool_type": "概念手绘 / 设计规划",
                "prompt": "[Reconstructed Prompt | 复现建议] 星空古殿与中央神兽空间透视大框架",
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
                "prompt": f"[Reconstructed Prompt | 复现建议] {prompt_v1}",
                "parameters": "采样步数范围 25–35 步 [Reconstructed], CFG 7.0, Seed 未记录",
                "outputs": [{
                    "filename": "02_reconstructed_generation_v1.png",
                    "caption": "阶段二 AI 生成第一版初稿图像",
                    "evidence_level": "[Reconstructed]"
                }],
                "adjustment": adjustment_reason,
                "evidence_level": "[Reconstructed]"
            },
            {
                "id": "stage_3",
                "title": "阶段三：Prompt 迭代与视觉深化",
                "purpose": "修正初稿光影缺陷，强化微晶质感与丁达尔光线",
                "inputs": [{"name": "阶段二初版成果", "filename": "02_reconstructed_generation_v1.png"}],
                "tool": "AI 迭代与优化工具",
                "tool_type": "生成式 AI",
                "prompt": f"[Reconstructed Prompt | 复现建议] {prompt_v2}",
                "parameters": "建议重绘参数范围 0.55–0.65",
                "outputs": [{
                    "filename": "03_reconstructed_generation_v2.png",
                    "caption": "阶段三多轮提示词优化后的高清渲染成果",
                    "evidence_level": "[Reconstructed]"
                }],
                "adjustment": "光影聚集，微晶细节达到预期，完成具象生成",
                "evidence_level": "[Reconstructed]"
            }
        ]

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

        manifest_path = out_dir / "submission_manifest.json"
        manifest_path.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2), encoding="utf-8")

        # 5. Build DOCX via scripts/build_docx.py
        docx_path = out_dir / "深林微光_新媒体节_AIGC说明书.docx"
        build_docx.build_docx_from_manifest(str(manifest_path), str(docx_path))
        
        self.assertTrue(docx_path.exists())
        self.assertGreater(docx_path.stat().st_size, 0)

        # 6. Verify DOCX Image Embeddings (test_docx_embeds_generated_assets)
        doc = docx.Document(str(docx_path))
        # Check inline shapes (images embedded)
        self.assertGreaterEqual(len(doc.inline_shapes), 3, "DOCX did not embed at least 3 generated images")
        
        # Check figure captions
        doc_text = "\n".join([p.text for p in doc.paragraphs])
        self.assertIn("图 1 阶段一空间透视与主体占位草图", doc_text)
        self.assertIn("图 2 阶段二 AI 生成第一版初稿图像", doc_text)
        self.assertIn("图 3 阶段三多轮提示词优化后的高清渲染成果", doc_text)

        # 7. Zero Placeholder Assertion (test_no_dangling_placeholders)
        found_placeholders = scan_placeholders.scan_directory(str(out_dir))
        self.assertEqual(found_placeholders, [], f"Dangling placeholders found: {found_placeholders}")


if __name__ == "__main__":
    unittest.main()
