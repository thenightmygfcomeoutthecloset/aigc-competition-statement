#!/usr/bin/env python3
"""Build and structurally verify an A4 competition statement DOCX."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import docx
from PIL import Image
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Mm, Pt

from canonical_schema import docx_image_asset_ids
from manifest_schema import asset_path_map, validate_manifest_file

FONT_NAME = "Noto Sans SC"
TABLE_WIDTH_DXA = 9024

for stream in (sys.stdout, sys.stderr):
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


def _set_run_font(run, size: float = 10.5, bold: bool = False) -> None:
    run.font.name = FONT_NAME
    run.font.size = Pt(size)
    run.bold = bold
    fonts = run._element.get_or_add_rPr().get_or_add_rFonts()
    for key in ("ascii", "hAnsi", "eastAsia"):
        fonts.set(qn(f"w:{key}"), FONT_NAME)


def _keep(paragraph, *, next_paragraph: bool = False, lines: bool = True) -> None:
    properties = paragraph._p.get_or_add_pPr()
    if next_paragraph:
        properties.append(OxmlElement("w:keepNext"))
    if lines:
        properties.append(OxmlElement("w:keepLines"))


def _add_heading(document, text: str, level: int) -> None:
    paragraph = document.add_paragraph(style=f"Heading {level}")
    paragraph.add_run(text)
    _keep(paragraph, next_paragraph=True)


def _add_body(document, text: str, *, label: str | None = None) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(5)
    paragraph.paragraph_format.line_spacing = 1.25
    if label:
        _set_run_font(paragraph.add_run(label), bold=True)
    _set_run_font(paragraph.add_run(text))


def _set_cell_margins(cell, top: int = 80, bottom: int = 80, start: int = 120, end: int = 120) -> None:
    properties = cell._tc.get_or_add_tcPr()
    margins = properties.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        properties.append(margins)
    for name, value in (("top", top), ("bottom", bottom), ("start", start), ("end", end)):
        node = margins.find(qn(f"w:{name}"))
        if node is None:
            node = OxmlElement(f"w:{name}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def _set_table_geometry(table, widths: list[int]) -> None:
    if sum(widths) != TABLE_WIDTH_DXA:
        raise ValueError(f"Table widths must total {TABLE_WIDTH_DXA} DXA: {widths}")
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    properties = table._tbl.tblPr
    width = properties.first_child_found_in("w:tblW")
    width.set(qn("w:type"), "dxa")
    width.set(qn("w:w"), str(TABLE_WIDTH_DXA))
    indent = properties.first_child_found_in("w:tblInd")
    if indent is None:
        indent = OxmlElement("w:tblInd")
        properties.append(indent)
    indent.set(qn("w:type"), "dxa")
    indent.set(qn("w:w"), "0")
    layout = properties.first_child_found_in("w:tblLayout")
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        properties.append(layout)
    layout.set(qn("w:type"), "fixed")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for value in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(value))
        grid.append(col)
    for row in table.rows:
        for cell, value in zip(row.cells, widths):
            cell.width = Inches(value / 1440)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            _set_cell_margins(cell)
            tc_width = cell._tc.get_or_add_tcPr().get_or_add_tcW()
            tc_width.set(qn("w:type"), "dxa")
            tc_width.set(qn("w:w"), str(value))


def _fill_table(table, rows: list[list[str]], widths: list[int]) -> None:
    for row_values in rows:
        cells = table.add_row().cells
        for cell, value in zip(cells, row_values):
            cell.text = value
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.line_spacing = 1.1
                for run in paragraph.runs:
                    _set_run_font(run, size=8.5)
    _set_table_geometry(table, widths)
    for cell in table.rows[0].cells:
        for run in cell.paragraphs[0].runs:
            _set_run_font(run, size=9, bold=True)


def _add_image_with_caption(document, image_path: Path, caption: str, asset_id: str) -> None:
    with Image.open(image_path) as image:
        width_px, height_px = image.size
    max_width, max_height = 5.75, 6.65
    ratio = min(max_width / width_px, max_height / height_px)
    width, height = width_px * ratio, height_px * ratio
    image_paragraph = document.add_paragraph()
    image_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    image_paragraph.paragraph_format.space_before = Pt(6)
    image_paragraph.paragraph_format.space_after = Pt(2)
    _keep(image_paragraph, next_paragraph=True)
    shape = image_paragraph.add_run().add_picture(str(image_path), width=Inches(width), height=Inches(height))
    shape._inline.docPr.set("descr", asset_id)
    caption_paragraph = document.add_paragraph()
    caption_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_paragraph.paragraph_format.space_after = Pt(8)
    _keep(caption_paragraph)
    _set_run_font(caption_paragraph.add_run(caption), size=9)


def _configure_document(document) -> None:
    section = document.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(25)
    section.right_margin = Mm(25)
    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = FONT_NAME
    normal.font.size = Pt(10.5)
    normal._element.rPr.rFonts.set(qn("w:ascii"), FONT_NAME)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), FONT_NAME)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_NAME)
    for level, size in ((1, 15), (2, 13), (3, 11)):
        style = styles[f"Heading {level}"]
        style.font.name = FONT_NAME
        style.font.size = Pt(size)
        style.font.bold = True
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_NAME)
        style.paragraph_format.space_before = Pt(12 if level == 1 else 8)
        style.paragraph_format.space_after = Pt(6 if level == 1 else 4)


_CN_DRAFT = {1: "初稿", 2: "第二稿", 3: "第三稿", 4: "第四稿", 5: "第五稿", 6: "第六稿"}

_PROMPT_KEYS = ("subject", "composition", "palette", "atmosphere", "visual_style")

_PARAM_LABELS = {
    "aspect_ratio": "画幅比例",
    "render_mode": "渲染方式",
    "output_quality": "输出质量",
    "seed": "随机种子",
    "negative_prompt": "负向提示词",
}


def _draft_name(version: int) -> str:
    return _CN_DRAFT.get(version, f"第{version}稿")


def _naturalize_prompt(prompt: str) -> str:
    values: list[str] = []
    for segment in prompt.split("；"):
        segment = segment.strip()
        if ":" not in segment:
            continue
        key, _, value = segment.partition(":")
        if key.strip() in _PROMPT_KEYS:
            value = value.strip()
            if value and value not in values:
                values.append(value)
    return "。".join(values) + "。"


def _flow_title(kind: str, version: int | None) -> str:
    if kind == "input_design":
        return "构图与视觉设计"
    if kind == "generation":
        return f"{_draft_name(version)}生成"
    if kind == "final":
        return "最终定稿"
    return kind


def _flow_purpose(kind: str) -> str:
    if kind == "input_design":
        return "确定作品的构图、轮廓与色彩方向，形成前期视觉稿。"
    if kind == "generation":
        return "依据视觉方向生成完整画面。"
    if kind == "final":
        return "完成最终画面并定稿。"
    return ""


def _param_rows(parameters: dict) -> list[list[str]]:
    rows: list[list[str]] = []
    for key, value in parameters.items():
        if key == "iteration":
            continue
        label = _PARAM_LABELS.get(key, key)
        text = str(value)
        if key == "seed":
            text = text.replace("（建议随机）", "").replace("(建议随机)", "").strip()
        rows.append([label, text])
    return rows


def _verify_docx(docx_path: Path, image_assets: list[tuple[str, Path]], required_tokens: list[str]) -> None:
    result = docx.Document(docx_path)
    if len(result.inline_shapes) != len(image_assets):
        raise AssertionError(f"DOCX image count mismatch: expected {len(image_assets)}, got {len(result.inline_shapes)}")
    embedded = []
    for shape in result.inline_shapes:
        asset_id = shape._inline.docPr.get("descr")
        relationship_id = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
        blob = result.part.related_parts[relationship_id].blob
        embedded.append((asset_id, hashlib.sha256(blob).hexdigest()))
    expected = [(asset_id, hashlib.sha256(path.read_bytes()).hexdigest()) for asset_id, path in image_assets]
    if embedded != expected:
        raise AssertionError("DOCX drawings do not correspond one-for-one with canonical image assets")
    text = "\n".join(paragraph.text for paragraph in result.paragraphs)
    table_text = "\n".join(cell.text for table in result.tables for row in table.rows for cell in row.cells)
    combined = text + "\n" + table_text
    missing = [token for token in required_tokens if token not in combined]
    if missing:
        raise AssertionError(f"DOCX did not render required records: {missing}")
    forbidden = ["{作品名称}", "{赛事名称}", "待补齐", "待插入", "TODO", "TBD", "PLACEHOLDER"]
    leaked = [token for token in forbidden if token in combined]
    if leaked:
        raise AssertionError(f"DOCX contains placeholders: {leaked}")


def build_docx_from_manifest(manifest_path: str, output_docx_path: str) -> str:
    manifest = validate_manifest_file(manifest_path, allow_missing_asset_ids={"statement_docx"})
    paths = asset_path_map(manifest, manifest_path)
    output = Path(output_docx_path).resolve()
    if output != paths["statement_docx"]:
        raise ValueError(f"Output path must match statement_docx manifest asset: {paths['statement_docx']}")
    image_ids = docx_image_asset_ids(generation_versions=len(manifest.generation_records))
    missing = [asset_id for asset_id in image_ids if not paths[asset_id].is_file()]
    if missing:
        raise FileNotFoundError(f"Canonical images missing: {missing}")

    document = docx.Document()
    _configure_document(document)
    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_after = Pt(14)
    _keep(title, next_paragraph=True)
    _set_run_font(title.add_run(f"【{manifest.artwork.title}】AIGC 创作过程说明书"), size=18, bold=True)

    _add_heading(document, "一、作品基本信息", 1)
    for label, value in (
        ("作品名称：", manifest.artwork.title), ("参赛赛事：", manifest.artwork.competition),
        ("作品类型：", manifest.artwork.type), ("创作主题：", manifest.artwork.theme),
    ):
        _add_body(document, value, label=label)

    _add_heading(document, "二、创作构思与立意", 1)
    _add_body(document, manifest.creative_rationale.background, label="创作背景：")
    _add_body(document, manifest.creative_rationale.visual_concept, label="视觉构思：")

    _add_heading(document, "三、创作流程", 1)
    flow_stages = [stage for stage in manifest.stage_graph if stage.kind != "difference_analysis"]
    for index, stage in enumerate(flow_stages, start=1):
        _add_heading(document, f"3.{index} {_flow_title(stage.kind, stage.version)}", 2)
        _add_body(document, _flow_purpose(stage.kind))

    _add_heading(document, "四、前期视觉设计", 1)
    caption_by_id = {
        output_item.asset_id: output_item.label
        for stage in manifest.stage_graph
        for output_item in stage.outputs
    }
    caption_by_id["final_artwork"] = "最终作品"
    preliminary_ids = [asset_id for asset_id in image_ids if asset_id.startswith("reconstructed_")]
    figure_number = 1
    for asset_id in preliminary_ids:
        _add_image_with_caption(document, paths[asset_id], f"图 {figure_number} {caption_by_id.get(asset_id, asset_id)}", asset_id)
        figure_number += 1

    _add_heading(document, "五、作品生成过程", 1)
    for index, (record, parameter_item) in enumerate(zip(manifest.generation_records, manifest.parameter_record), start=1):
        _add_heading(document, f"5.{index} {_draft_name(index)}", 2)
        _add_body(document, _naturalize_prompt(record.prompt), label="生成提示词：")
        tool = manifest.original_tool or record.model
        _add_body(document, tool, label="生成工具：")
        rows = _param_rows(parameter_item.parameters)
        if rows:
            parameter_table = document.add_table(rows=1, cols=2)
            parameter_table.rows[0].cells[0].text = "参数"
            parameter_table.rows[0].cells[1].text = "说明"
            _fill_table(parameter_table, rows, [1872, 7152])
        _add_image_with_caption(document, paths[record.stage_id], f"图 {figure_number} {_draft_name(index)}", record.stage_id)
        figure_number += 1

    _add_heading(document, "六、最终作品", 1)
    _add_image_with_caption(document, paths["final_artwork"], f"图 {figure_number} 最终作品", "final_artwork")

    if manifest.original_tool:
        _add_heading(document, "七、创作工具说明", 1)
        _add_body(document, manifest.original_tool, label="创作工具：")

    document.core_properties.author = ""
    document.core_properties.last_modified_by = ""
    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(output)
    if not output.is_file() or output.stat().st_size == 0:
        raise AssertionError(f"DOCX was not created: {output}")
    expected_order = [*preliminary_ids, *[record.stage_id for record in manifest.generation_records], "final_artwork"]
    required_tokens = ["创作流程", "作品生成过程", "最终作品", *[record.model for record in manifest.generation_records]]
    _verify_docx(output, [(asset_id, paths[asset_id]) for asset_id in expected_order], required_tokens)
    return str(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build AIGC competition statement DOCX")
    parser.add_argument("--manifest", "-m", required=True)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()
    output = build_docx_from_manifest(args.manifest, args.output)
    print(f"DOCX generated and verified: {output} ({Path(output).stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
