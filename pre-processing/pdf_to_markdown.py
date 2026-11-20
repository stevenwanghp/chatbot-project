"""Convert PDF files to Markdown using PyMuPDF4LLM.

Usage:
    python pre-processing/pdf_to_markdown.py [source] [-o output_dir]
    - source: PDF file or directory to scan (default: data/)
    - output_dir: directory for generated Markdown files (default: data_processed/)"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pymupdf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MIN_TEXT_COVERAGE = 0.9


def find_pdfs(source: Path) -> list[Path]:
    if not source.exists():
        raise ValueError(f"Input does not exist: {source}")
    if source.is_file():
        if source.suffix.lower() != ".pdf":
            raise ValueError(f"Input file is not a PDF: {source}")
        return [source]
    if source.is_dir():
        return sorted(
            path for path in source.rglob("*")
            if path.is_file() and path.suffix.lower() == ".pdf"
        )
    raise ValueError(f"Input is not a file or directory: {source}")


def _text_tokens(text: str) -> set[str]:
    return set(re.findall(r"[^\W\d_]{3,}", text.casefold()))


def _restore_text_columns(page: pymupdf.Page, chunk: dict) -> str:
    markdown = chunk.get("text", "")
    replacements = []
    text_blocks = [
        block
        for block in page.get_text("blocks")
        if len(block) > 6 and block[6] == 0 and block[4].strip()
    ]

    for box in chunk.get("page_boxes", []):
        if box.get("class") != "text":
            continue
        x0, y0, x1, y1 = box["bbox"]
        blocks = [
            block
            for block in text_blocks
            if block[0] >= x0 - 2
            and block[1] >= y0 - 2
            and block[2] <= x1 + 2
            and block[3] <= y1 + 2
        ]
        columns = []
        for block in sorted(blocks, key=lambda item: item[0]):
            column = next(
                (group for group in columns if abs(group[0][0] - block[0]) <= 20),
                None,
            )
            if column is None:
                columns.append([block])
            else:
                column.append(block)
        if len(columns) < 2 or any(len(column) < 2 for column in columns):
            continue

        column_text = []
        for column in sorted(columns, key=lambda group: min(block[0] for block in group)):
            ordered_blocks = sorted(column, key=lambda block: block[1])
            for index, block in enumerate(ordered_blocks):
                text = block[4].strip()
                if index < len(ordered_blocks) - 1 and len(text) <= 40 and "\n" not in text:
                    text = f"**{text}**"
                column_text.append(text)
        start, end = box["pos"]
        replacements.append((start, end, "\n\n" + "\n\n".join(column_text) + "\n\n"))

    for start, end, replacement in sorted(replacements, reverse=True):
        markdown = markdown[:start] + replacement + markdown[end:]
    return markdown


def convert_pdf(pdf_path: Path, output_path: Path, use_ocr: bool = False) -> list[str]:
    warnings = []
    page_markdown = []
    with pymupdf.open(pdf_path) as document:
        page_chunks = document.to_markdown(
            page_chunks=True,
            force_text=True,
            use_ocr=use_ocr,
        )
        if len(page_chunks) != len(document):
            raise ValueError(
                f"Expected Markdown for {len(document)} pages, got {len(page_chunks)}"
            )

        for page_number, (page, chunk) in enumerate(zip(document, page_chunks), start=1):
            text = _restore_text_columns(page, chunk).strip()
            source_tokens = _text_tokens(page.get_text("text", sort=True))
            markdown_tokens = _text_tokens(text)
            if source_tokens:
                missing_tokens = source_tokens - markdown_tokens
                coverage = 1 - len(missing_tokens) / len(source_tokens)
                if coverage < MIN_TEXT_COVERAGE:
                    missing_preview = ", ".join(sorted(missing_tokens)[:8])
                    warnings.append(
                        f"{pdf_path.name}, page {page_number}: only "
                        f"{coverage:.0%} of native text tokens appear in Markdown; "
                        f"review missing text (for example: {missing_preview})."
                    )
            elif not text:
                warnings.append(
                    f"{pdf_path.name}, page {page_number}: no text extracted; "
                    "try --ocr if the page contains readable text in an image."
                )

            if text:
                page_markdown.append(f"## Source page {page_number}\n\n{text}")

    markdown = "\n\n---\n\n".join(page_markdown)
    if not markdown.strip():
        raise ValueError("No text was extracted")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=PROJECT_ROOT / "data",
        help="PDF file or directory to scan (default: data/)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "data_processed",
        help="directory for generated Markdown files (default: data_processed/)",
    )
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="OCR pages detected as image-based (requires an installed OCR engine)",
    )
    args = parser.parse_args()

    try:
        pdfs = find_pdfs(args.source)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    if not pdfs:
        print(f"No PDF files found in {args.source}", file=sys.stderr)
        return 1

    failed = False
    for pdf_path in pdfs:
        relative_path = (
            pdf_path.relative_to(args.source)
            if args.source.is_dir()
            else Path(pdf_path.name)
        )
        output_path = (args.output_dir / relative_path).with_suffix(".md")
        try:
            page_warnings = convert_pdf(pdf_path, output_path, use_ocr=args.ocr)
            print(f"Converted {pdf_path} -> {output_path}")
            for warning in page_warnings:
                print(f"Warning: {warning}", file=sys.stderr)
        except Exception as error:
            failed = True
            print(f"Failed to convert {pdf_path}: {error}", file=sys.stderr)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())