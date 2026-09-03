#!/usr/bin/env python3
"""Render every DOCX page through LibreOffice and run basic visual regression checks."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import fitz
from PIL import Image, ImageChops

for stream in (sys.stdout, sys.stderr):
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


def find_soffice() -> Path | None:
    discovered = shutil.which("soffice") or shutil.which("libreoffice")
    if discovered:
        return Path(discovered)
    candidates = [
        Path("C:/Program Files/LibreOffice/program/soffice.exe"),
        Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe"),
        Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"),
        Path("/usr/bin/libreoffice"),
        Path("/usr/local/bin/libreoffice"),
    ]
    return next((path for path in candidates if path.is_file()), None)


def render_docx(docx_path: str | Path, output_dir: str | Path, *, dpi: int = 144) -> list[Path]:
    source = Path(docx_path).resolve()
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    soffice = find_soffice()
    if soffice is None:
        raise RuntimeError("LibreOffice soffice executable was not found")
    with tempfile.TemporaryDirectory(prefix="aigc_lo_profile_") as profile:
        profile_uri = Path(profile).resolve().as_uri()
        process = subprocess.run(
            [str(soffice), "--headless", f"-env:UserInstallation={profile_uri}", "--convert-to", "pdf", "--outdir", str(output), str(source)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    pdf_path = output / f"{source.stem}.pdf"
    if process.returncode != 0 or not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"LibreOffice render failed ({process.returncode}): {process.stdout}\n{process.stderr}")
    pages: list[Path] = []
    scale = dpi / 72
    with fitz.open(pdf_path) as document:
        if document.page_count == 0:
            raise RuntimeError("LibreOffice produced a zero-page PDF")
        extracted_pages = [page.get_text().strip() for page in document]
        if any(not text for text in extracted_pages):
            blank_numbers = [str(index) for index, text in enumerate(extracted_pages, start=1) if not text]
            raise AssertionError(f"Rendered PDF has text-empty pages: {', '.join(blank_numbers)}")
        if not re.search(r"[\u3400-\u9fff]", "\n".join(extracted_pages)):
            raise AssertionError("Rendered PDF did not preserve extractable Chinese text")
        for index, page in enumerate(document, start=1):
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
            page_path = output / f"page-{index}.png"
            pixmap.save(page_path)
            pages.append(page_path)
    return pages


def audit_rendered_pages(page_paths: list[Path]) -> None:
    if not page_paths:
        raise AssertionError("No rendered pages were produced")
    for page_path in page_paths:
        with Image.open(page_path).convert("RGB") as image:
            background = Image.new("RGB", image.size, "white")
            bbox = ImageChops.difference(image, background).getbbox()
            if bbox is None:
                raise AssertionError(f"Blank rendered page: {page_path.name}")
            left, top, right, bottom = bbox
            if left <= 2 or top <= 2 or right >= image.width - 2 or bottom >= image.height - 2:
                raise AssertionError(f"Rendered content touches page edge (possible overflow): {page_path.name}: {bbox}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a DOCX with LibreOffice and audit every page")
    parser.add_argument("docx")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dpi", type=int, default=144)
    args = parser.parse_args()
    pages = render_docx(args.docx, args.output_dir, dpi=args.dpi)
    audit_rendered_pages(pages)
    print(f"Rendered and audited {len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
