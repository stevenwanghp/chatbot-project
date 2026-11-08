"""Convert PDF files to Markdown using PyMuPDF4LLM.

Usage:
    python pre-processing/pdf_to_markdown.py [source] [-o output_dir]
    - source: PDF file or directory to scan (default: data/)
    - output_dir: directory for generated Markdown files (default: data_processed/)"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf4llm


PROJECT_ROOT = Path(__file__).resolve().parents[1]


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


def convert_pdf(pdf_path: Path, output_path: Path) -> None:
    markdown = pymupdf4llm.to_markdown(str(pdf_path))
    if not markdown.strip():
        raise ValueError("No text was extracted")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")


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
            convert_pdf(pdf_path, output_path)
            print(f"Converted {pdf_path} -> {output_path}")
        except Exception as error:
            failed = True
            print(f"Failed to convert {pdf_path}: {error}", file=sys.stderr)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())