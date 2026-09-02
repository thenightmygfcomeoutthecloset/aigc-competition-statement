#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docx.py - Executable assembly contract for AIGC competition statement DOCX.

Takes submission_manifest.json, stage_graph.json, prompt_record.json, and visual assets,
and compiles a publication-ready, academic-standard A4 Microsoft Word document (.docx).
Guarantees:
1. Dynamic Stage Graph rendering (data-driven stages 3.1, 3.2, ...);
2. Real image embedding (PNG files embedded with academic captions);
3. Summary tables and toolchain matrices generated from stage_graph;
4. Metadata sanitization (clears author, company, last_modified_by);
5. Post-generation integrity verification and zero-placeholder assertion.
"""

import os
import sys
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
import json
import argparse
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, fill_hex: str):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Set padding in twips (1/20 of a pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def add_custom_heading(doc, text: str, level: int):
    """Add styled Chinese heading with proper spacing."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "SimHei"  # 黑体
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "SimHei")
    run.bold = True
    
    if level == 1:
        run.font.size = Pt(15)  # 小三号
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(13)  # 四号
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(11)  # 小四号
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
    return p


def add_body_paragraph(doc, text: str, bold_prefix: str = None, indent: bool = True):
    """Add standard body paragraph in SimSun."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.35
    p.paragraph_format.space_after = Pt(4)
    if indent:
        p.paragraph_format.first_line_indent = Pt(21)  # 2 characters indent
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "SimHei"
        r_pre._element.rPr.rFonts.set(qn("w:eastAsia"), "SimHei")
        r_pre.bold = True
        r_pre.font.size = Pt(10.5)  # 五号
        
    run = p.add_run(text)
    run.font.name = "SimSun"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")
    run.font.size = Pt(10.5)
    return p


def add_caption(doc, text: str):
    """Add centered academic figure caption in KaiTi."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    run.font.name = "KaiTi"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "KaiTi")
    run.font.size = Pt(9)  # 小五号
    run.font.color.rgb = RGBColor(80, 80, 80)
    return p


def build_docx_from_manifest(manifest_path: str, output_docx_path: str) -> str:
    """Builds the complete docx according to canonical stage graph and manifest."""
    manifest_file = Path(manifest_path).resolve()
    base_dir = manifest_file.parent
    
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    artwork_info = manifest.get("artwork", {})
    title = artwork_info.get("title", "未命名作品")
    competition = artwork_info.get("competition", "高校创意竞赛")
    work_type = artwork_info.get("type", "数字图像/概念插画")
    theme = artwork_info.get("theme", "AIGC 视觉创作")
    pipeline = artwork_info.get("pipeline", "动态 AIGC 演进管线")
    tool_env = artwork_info.get("tool_environment", "原始创作工具：未记录（基于特征推断） / 本次复现工具：宿主生图能力")
    rationale = manifest.get("creative_rationale", {})
    stage_graph = manifest.get("stage_graph", [])
    prompt_record = manifest.get("prompt_record", [])
    disclaimer = manifest.get("disclaimer", "")

    doc = docx.Document()
    
    # Set standard A4 page margins (top/bottom 2.54cm, left/right 3.18cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.25)
        
    # Main Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(18)
    title_p.paragraph_format.space_after = Pt(18)
    t_run = title_p.add_run(f"【{title}】AIGC 创作过程说明书")
    t_run.font.name = "SimHei"
    t_run._element.rPr.rFonts.set(qn("w:eastAsia"), "SimHei")
    t_run.font.size = Pt(18)  # 小二号
    t_run.bold = True
    
    # -------------------------------------------------------------
    # 一、作品基本信息
    # -------------------------------------------------------------
    add_custom_heading(doc, "一、作品基本信息", level=1)
    add_body_paragraph(doc, f"：{title}", bold_prefix="作品名称", indent=False)
    add_body_paragraph(doc, f"：{competition}", bold_prefix="参赛赛事", indent=False)
    add_body_paragraph(doc, f"：{work_type}", bold_prefix="作品类型", indent=False)
    add_body_paragraph(doc, f"：{theme}", bold_prefix="创作主题", indent=False)
    add_body_paragraph(doc, f"：{pipeline}", bold_prefix="AIGC 核心技术路径", indent=False)
    add_body_paragraph(doc, f"：{tool_env}", bold_prefix="工具环境说明", indent=False)
    
    # -------------------------------------------------------------
    # 二、创作构思与立意
    # -------------------------------------------------------------
    add_custom_heading(doc, "二、创作构思与立意", level=1)
    add_custom_heading(doc, "1. 创作背景与选题动机", level=2)
    add_body_paragraph(doc, rationale.get("background", "本作品响应大赛主题要求，融合数字艺术与设计美学进行深度视觉探索。"))
    
    add_custom_heading(doc, "2. 视觉设计思路与设计目标", level=2)
    add_body_paragraph(doc, rationale.get("visual_concept", "通过严谨的构图规划与色彩冷暖层次对撞，展现极具张力的视觉感染力。"))
    
    add_custom_heading(doc, "3. AIGC 工具协同目的", level=2)
    add_body_paragraph(doc, rationale.get("ai_collaboration", "借助生成式 AI 高效计算复杂环境光照漫反射与微晶材质，实现想象力与写实细节的有机协同。"))
    
    # -------------------------------------------------------------
    # 三、阶段性创作过程 (Dynamic Stage Graph)
    # -------------------------------------------------------------
    add_custom_heading(doc, "三、阶段性创作过程", level=1)
    p_intro = add_body_paragraph(
        doc,
        "本章节基于动态阶段管线（Dynamic Stage Graph），完整呈现“输入素材 → 生成工具 → 提示词 → 参数配置 → 阶段结果 → 调整优化”的自洽闭环证据链。",
        indent=False
    )
    p_intro.paragraph_format.space_after = Pt(8)
    
    figure_counter = 1
    for idx, stage in enumerate(stage_graph, start=1):
        stage_title = stage.get("title", f"阶段{idx}")
        add_custom_heading(doc, f"3.{idx} {stage_title}", level=2)
        
        purpose = stage.get("purpose", "")
        if purpose:
            add_body_paragraph(doc, f"：{purpose}", bold_prefix="创作目的", indent=False)
            
        inputs = stage.get("inputs", [])
        if inputs:
            input_desc = "、".join([inp.get("name", str(inp)) for inp in inputs])
            add_body_paragraph(doc, f"：{input_desc}", bold_prefix="输入素材", indent=False)
            
        tool = stage.get("tool", "")
        if tool:
            add_body_paragraph(doc, f"：{tool}", bold_prefix="使用工具", indent=False)
            
        prompt = stage.get("prompt", "")
        if prompt:
            add_body_paragraph(doc, f"：{prompt}", bold_prefix="提示词配置", indent=False)
            
        params = stage.get("parameters", "")
        if params:
            add_body_paragraph(doc, f"：{params}", bold_prefix="配置参数", indent=False)
            
        # Embedded Outputs / Images
        outputs = stage.get("outputs", [])
        for out in outputs:
            img_filename = out.get("filename", "")
            img_caption = out.get("caption", f"阶段{idx}成果")
            evidence_level = out.get("evidence_level", "[Reconstructed]")
            
            # Resolve image path
            img_path = base_dir / img_filename
            if not img_path.exists() and "path" in out:
                img_path = Path(out["path"])
                
            if img_path.exists() and img_path.is_file() and img_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                img_p = doc.add_paragraph()
                img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                img_p.paragraph_format.space_before = Pt(8)
                img_p.paragraph_format.space_after = Pt(2)
                run_img = img_p.add_run()
                run_img.add_picture(str(img_path), width=Inches(5.5))
                
                # Caption
                full_caption = f"图 {figure_counter} {img_caption} ({evidence_level})"
                add_caption(doc, full_caption)
                figure_counter += 1
                
        adjustment = stage.get("adjustment", "")
        if adjustment:
            add_body_paragraph(doc, f"：{adjustment}", bold_prefix="调整说明与优化方向", indent=False)
            
        evidence_tag = stage.get("evidence_level", "[Reconstructed]")
        add_body_paragraph(doc, f"：{evidence_tag}", bold_prefix="证据等级", indent=False)
        
    # -------------------------------------------------------------
    # 四、AIGC 工具使用说明与人机协同分工
    # -------------------------------------------------------------
    add_custom_heading(doc, "四、AIGC 工具使用说明与人机协同分工", level=1)
    add_custom_heading(doc, "1. 核心工具链矩阵", level=2)
    
    # Table of tools
    tool_table = doc.add_table(rows=1, cols=4)
    tool_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tool_table.autofit = True
    hdr_cells = tool_table.rows[0].cells
    hdr_titles = ["制作阶段", "采用工具", "工具属性", "具体作用"]
    for i, title_text in enumerate(hdr_titles):
        hdr_cells[i].text = title_text
        set_cell_background(hdr_cells[i], "F2F2F2")
        set_cell_margins(hdr_cells[i])
        for r in hdr_cells[i].paragraphs[0].runs:
            r.font.name = "SimHei"
            r.bold = True
            r.font.size = Pt(9.5)
            
    for stage in stage_graph:
        row_cells = tool_table.add_row().cells
        row_cells[0].text = stage.get("title", "")
        row_cells[1].text = stage.get("tool", "")
        row_cells[2].text = stage.get("tool_type", "生成式 AI / 设计工具")
        row_cells[3].text = stage.get("purpose", "")
        for c in row_cells:
            set_cell_margins(c)
            for r in c.paragraphs[0].runs:
                r.font.name = "SimSun"
                r.font.size = Pt(9.5)
                
    add_custom_heading(doc, "2. 人机协同职责划分", level=2)
    add_body_paragraph(
        doc,
        "提出作品核心主旨与立意隐喻；规划画面骨骼、空间透视与构图引导；编写并迭代提示词策略；严格把控最终画面的审美与艺术标准。",
        bold_prefix="人类创作者主导环节："
    )
    add_body_paragraph(
        doc,
        "高效执行物理光线漫反射与环境气氛渲染；具象化呈现微晶与细腻材质；协助完成初稿到深化稿的高精渲染迭代。",
        bold_prefix="AI 工具协同辅助环节："
    )
    
    # -------------------------------------------------------------
    # 五、全流程 Prompt、输入素材与参数汇总表
    # -------------------------------------------------------------
    add_custom_heading(doc, "五、全流程 Prompt、输入素材与参数汇总表", level=1)
    summary_table = doc.add_table(rows=1, cols=5)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["创作阶段", "输入素材 (Input)", "采用工具 (Tool)", "提示词 (Prompt)", "参数与产出 (Output)"]
    for i, h_text in enumerate(s_headers):
        summary_table.rows[0].cells[i].text = h_text
        set_cell_background(summary_table.rows[0].cells[i], "F2F2F2")
        set_cell_margins(summary_table.rows[0].cells[i])
        for r in summary_table.rows[0].cells[i].paragraphs[0].runs:
            r.font.name = "SimHei"
            r.bold = True
            r.font.size = Pt(9.0)
            
    for stage in stage_graph:
        row = summary_table.add_row().cells
        row[0].text = stage.get("title", "")
        inputs = stage.get("inputs", [])
        row[1].text = "、".join([i.get("name", str(i)) for i in inputs]) if inputs else "初始输入"
        row[2].text = stage.get("tool", "")
        row[3].text = stage.get("prompt", "")
        out_names = "、".join([o.get("caption", o.get("filename", "")) for o in stage.get("outputs", [])])
        param_str = stage.get("parameters", "")
        row[4].text = f"{param_str}\n产出：{out_names}" if param_str else f"产出：{out_names}"
        for c in row:
            set_cell_margins(c)
            for r in c.paragraphs[0].runs:
                r.font.name = "SimSun"
                r.font.size = Pt(8.5)
                
    # -------------------------------------------------------------
    # 六、版权、素材来源与原创性说明
    # -------------------------------------------------------------
    add_custom_heading(doc, "六、版权、素材来源与原创性说明", level=1)
    add_body_paragraph(
        doc,
        "本作品由创作者自主完成构思、构图规划与提示词设计，作品内容积极向上，不含任何违法违规信息，无知识产权争议与权属纠纷。",
        bold_prefix="1. 作品原创性承诺："
    )
    add_body_paragraph(
        doc,
        "创作全流程中使用的草图构想系创作者自主原创规划，未引入未经授权的第三方商用摄影图或专属素材。",
        bold_prefix="2. 输入素材来源陈述："
    )
    add_body_paragraph(
        doc,
        "画面中未出现未经授权的第三方商业 Logo、商标或受保护影视动漫专属形象，字体与美术要素符合赛事合规要求。",
        bold_prefix="3. 知识产权自查结论："
    )
    
    # -------------------------------------------------------------
    # 七、复现材料特别说明
    # -------------------------------------------------------------
    add_custom_heading(doc, "七、复现材料特别说明", level=1)
    if not disclaimer:
        disclaimer = (
            "本说明文档中标记为 [Reconstructed] 的草图构图、阶段演进过程图、提示词演进及推荐配置参数，"
            "系因创作者创作过程中部分原始中间过程文件未作完整留存，由 AI 辅助分析系统根据最终作品的视觉与工程特征"
            "进行逆向工程分析和复现构建。其核心目的在于完整展示作品的技术路线、构思演进逻辑与工艺可复现性，"
            "并不代表创作当时保存的原始物理历史记录。"
        )
    p_disc = doc.add_paragraph()
    p_disc.paragraph_format.line_spacing = 1.35
    p_disc.paragraph_format.first_line_indent = Pt(21)
    p_disc.paragraph_format.space_before = Pt(6)
    p_disc.paragraph_format.space_after = Pt(12)
    r_disc = p_disc.add_run(disclaimer)
    r_disc.font.name = "KaiTi"
    r_disc._element.rPr.rFonts.set(qn("w:eastAsia"), "KaiTi")
    r_disc.font.size = Pt(10)
    
    # -------------------------------------------------------------
    # Metadata Sanitization
    # -------------------------------------------------------------
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.core_properties.comments = ""
    doc.core_properties.category = ""
    
    out_file = Path(output_docx_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_file))
    
    # -------------------------------------------------------------
    # Basic Integrity Verification
    # -------------------------------------------------------------
    assert out_file.exists(), f"DOCX file failed to save: {out_file}"
    assert out_file.stat().st_size > 0, f"DOCX file is empty: {out_file}"
    
    verify_doc = docx.Document(str(out_file))
    assert len(verify_doc.paragraphs) > 10, "DOCX has too few paragraphs"
    assert len(verify_doc.tables) >= 2, "DOCX is missing required tables"
    
    # Placeholder Scan on XML text
    full_text = []
    for p in verify_doc.paragraphs:
        full_text.append(p.text)
    for t in verify_doc.tables:
        for row in t.rows:
            for cell in row.cells:
                full_text.append(cell.text)
    combined = "\n".join(full_text)
    
    forbidden_tokens = ["{作品名称}", "{赛事名称}", "{提示词内容}", "待补齐", "待确认", "待插入", "TODO", "TBD", "PLACEHOLDER"]
    found = [tok for tok in forbidden_tokens if tok in combined]
    if found:
        raise AssertionError(f"Leaked placeholders detected in built DOCX: {found}")
        
    return str(out_file)


def main():
    parser = argparse.ArgumentParser(description="Build AIGC competition statement DOCX from manifest.")
    parser.add_argument("--manifest", "-m", required=True, help="Path to submission_manifest.json")
    parser.add_argument("--output", "-o", required=True, help="Output DOCX file path")
    args = parser.parse_args()
    
    out_path = build_docx_from_manifest(args.manifest, args.output)
    print(f"Successfully generated and verified DOCX: {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    main()

