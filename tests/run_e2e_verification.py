#!/usr/bin/env python3
"""Run three different subjects through the public v0.3.0 CLI."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from manifest_schema import asset_path_map, sha256_file, validate_manifest_file

for stream in (sys.stdout, sys.stderr):
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


CASES = [
    ("生态海岸", "海岸社区中的能源塔与公共花园", "海岸曲线引导至中心能源塔", "深海蓝、植被绿、日落橙", (480, 320), 1),
    ("戏曲新声", "舞台中央的青年戏曲表演者与数字屏风", "竖向中心构图与层叠幕布", "朱红、墨黑、鎏金", (320, 480), 2),
    ("深空农场", "轨道温室、维护机器人与地球弧面", "环形结构围绕中央温室", "群青、银灰、植物绿", (400, 400), 3),
]


def make_artwork(path: Path, size: tuple[int, int], index: int) -> None:
    palettes = [((18, 42, 70), (60, 180, 125)), ((52, 18, 25), (220, 56, 42)), ((10, 18, 48), (100, 190, 90))]
    image = Image.new("RGB", size, palettes[index][0])
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 20, size[0] - 20, size[1] - 20), outline=(225, 190, 86), width=7)
    draw.ellipse((size[0] // 4, size[1] // 4, 3 * size[0] // 4, 3 * size[1] // 4), fill=palettes[index][1])
    draw.line((0, size[1], size[0] // 2, size[1] // 2, size[0], size[1]), fill=(225, 190, 86), width=9)
    image.save(path)


def run_case(root: Path, case: tuple, index: int) -> Path:
    title, subject, composition, palette, size, count = case
    case_root = root / f"case-{index + 1}-{title}"
    fixtures, output = case_root / "fixtures", case_root / "output"
    fixtures.mkdir(parents=True)
    final = case_root / "final-input.png"
    make_artwork(final, size, index)
    plan = {}
    for version in range(1, count + 1):
        snapshot = fixtures / f"v{version}.png"
        if version == count:
            shutil.copyfile(final, snapshot)
        else:
            Image.new("RGB", size, ((index + 1) * 55, version * 45, 190 - version * 25)).save(snapshot)
        plan[f"generation_v{version}"] = str(snapshot.resolve())
    analysis = case_root / "analysis.json"
    analysis.write_text(json.dumps({
        "subject": subject, "composition": composition, "palette": palette, "theme": title,
        "perspective": "根据主体空间关系建立透视", "environment": f"围绕{subject}形成完整环境",
        "foreground": "前景建立遮挡和视觉入口", "middle_ground": "中景承载核心主体", "background_visual": "背景交代完整场景",
        "lighting": "主光聚焦核心主体", "atmosphere": f"与{title}主题一致", "visual_style": "完整数字概念艺术",
        "material": "主体与环境材质清晰可辨", "detail": "保留结构与材质细节", "convergence_threshold": 0.98,
    }, ensure_ascii=False), encoding="utf-8")
    command = [sys.executable, str(SCRIPTS / "run_pipeline.py"), "--input", str(final), "--output-dir", str(output), "--title", title, "--competition", "高校创意验证赛", "--analysis-json", str(analysis), "--max-iterations", "4"]
    env = os.environ.copy()
    env.update({
        "AIGC_IMAGE_GENERATION_COMMAND": json.dumps([sys.executable, str(REPO_ROOT / "tests" / "fixture_generation_backend.py")]),
        "AIGC_IMAGE_GENERATION_BACKEND": "e2e_fixture_generation_provider",
        "AIGC_IMAGE_GENERATION_MODE": "image_to_image",
        "AIGC_IMAGE_GENERATION_MODEL": "fixture-complete-artwork-model",
        "AIGC_FIXTURE_GENERATION_PLAN": json.dumps(plan),
    })
    print("COMMAND:", subprocess.list2cmdline(command))
    process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    print(process.stdout, end="")
    print(process.stderr, end="", file=sys.stderr)
    if process.returncode != 0:
        raise RuntimeError(f"{title} pipeline exited with {process.returncode}")
    manifest_path = output / "submission_manifest.json"
    manifest = validate_manifest_file(manifest_path)
    paths = asset_path_map(manifest, manifest_path)
    expected = {sha256_file(paths[asset_id]) for asset_id in ["reconstructed_sketch", "reconstructed_lineart", "reconstructed_color_block", *[record.stage_id for record in manifest.generation_records], "final_artwork"]}
    with ZipFile(paths["statement_docx"]) as package:
        actual = {hashlib.sha256(package.read(name)).hexdigest() for name in package.namelist() if name.startswith("word/media/")}
    if actual != expected:
        raise AssertionError("DOCX media do not match dynamic execution records")
    if len(manifest.generation_records) != count:
        raise AssertionError(f"Expected {count} versions, got {len(manifest.generation_records)}")
    print(f"CASE_RESULT: {title} generation_versions={len(manifest.generation_records)} stage_count={len(manifest.stage_graph)} docx_media={len(actual)}")
    for record in manifest.generation_records:
        print(f"  {record.version}: backend={record.backend} status={record.status} output={record.output} size={paths[record.stage_id].stat().st_size}")
    return manifest_path


def run_e2e(output_dir: str) -> list[Path]:
    root = Path(output_dir).resolve()
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    manifests = [run_case(root, case, index) for index, case in enumerate(CASES)]
    print("E2E_SUMMARY:")
    for case, manifest_path in zip(CASES, manifests):
        manifest = validate_manifest_file(manifest_path)
        print(f"  {case[0]}: {len(manifest.generation_records)} generation version(s), manifest={manifest_path.stat().st_size} bytes")
    print("RESULT: PASS")
    return manifests


if __name__ == "__main__":
    run_e2e(str(REPO_ROOT / "tests" / "e2e_output"))
