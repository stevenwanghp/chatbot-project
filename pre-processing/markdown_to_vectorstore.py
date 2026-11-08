"""Chunk Markdown files and store them in a persistent Chroma vector store."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import yaml
from langchain_core.documents import Document

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from helper_functions.config import load_config
from helper_functions.vectorstore import create_text_splitter, create_vector_store

CONFIG = load_config()


def find_markdown_files(source: Path) -> list[Path]:
    if not source.exists():
        raise ValueError(f"Input does not exist: {source}")
    if source.is_file():
        if source.suffix.lower() not in {".md", ".markdown"}:
            raise ValueError(f"Input file is not Markdown: {source}")
        return [source]
    if source.is_dir():
        return sorted(
            path
            for path in source.rglob("*")
            if path.is_file() and path.suffix.lower() in {".md", ".markdown"}
        )
    raise ValueError(f"Input is not a file or directory: {source}")


def load_markdown_document(path: Path, source_name: str) -> Document | None:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return None

    metadata = {"source": source_name, "source_type": "pdf"}
    if text.startswith("---\n"):
        _, front_matter, text = text.split("---", 2)
        parsed_metadata = yaml.safe_load(front_matter) or {}
        if isinstance(parsed_metadata, dict):
            metadata.update(parsed_metadata)
        text = text.strip()
    return Document(page_content=text, metadata=metadata)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=PROJECT_ROOT / CONFIG["PROCESSED_DATA_DIRECTORY"],
        help=f"Markdown file or directory (default: {CONFIG['PROCESSED_DATA_DIRECTORY']}/)",
    )
    parser.add_argument(
        "--persist-dir",
        type=Path,
        default=PROJECT_ROOT / CONFIG["VECTOR_STORE_DIRECTORY"],
        help=(
            "directory for the persistent Chroma database "
            f"(default: {CONFIG['VECTOR_STORE_DIRECTORY']}/)"
        ),
    )
    parser.add_argument(
        "--collection",
        default=CONFIG["VECTOR_STORE_COLLECTION"],
        help="Chroma collection name",
    )
    args = parser.parse_args()

    try:
        markdown_files = find_markdown_files(args.source)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    if not markdown_files:
        print(f"No Markdown files found in {args.source}", file=sys.stderr)
        return 1

    documents = []
    for path in markdown_files:
        source_name = path.relative_to(args.source).as_posix() if args.source.is_dir() else path.name
        document = load_markdown_document(path, source_name)
        if document is None:
            print(f"Skipping empty file: {path}", file=sys.stderr)
            continue
        chunks = create_text_splitter().split_documents([document])
        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index
        documents.extend(chunks)

    if not documents:
        print("No non-empty Markdown content to process", file=sys.stderr)
        return 1

    load_dotenv(PROJECT_ROOT / ".env")
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: set OPENAI_API_KEY in .env before creating embeddings", file=sys.stderr)
        return 1

    ids = [
        hashlib.sha256(
            f"{doc.metadata.get('source_url', doc.metadata['source'])}:{doc.metadata['chunk_index']}".encode("utf-8")
        ).hexdigest()
        for doc in documents
    ]
    try:
        vector_store = create_vector_store(
            collection_name=args.collection,
            persist_directory=str(args.persist_dir),
        )
        source_names = sorted({doc.metadata["source"] for doc in documents})
        for source_name in source_names:
            vector_store.delete(where={"source": source_name})
        vector_store.add_documents(documents, ids=ids)
    except Exception as error:
        print(f"Failed to create vector store: {error}", file=sys.stderr)
        return 1

    print(
        f"Stored {len(documents)} chunks from {len(markdown_files)} Markdown files "
        f"in {args.persist_dir} (collection: {args.collection})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())