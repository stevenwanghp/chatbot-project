"""Retrieve relevant Syariah Court content from the persistent Chroma store."""

import re

import streamlit as st
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from helper_functions.config import load_config
from helper_functions.vectorstore import load_configured_vector_store

CONFIG = load_config()
TOP_K = CONFIG["RETRIEVAL_TOP_K"]
VECTOR_CANDIDATES = CONFIG["VECTOR_RETRIEVAL_CANDIDATES"]
KEYWORD_CANDIDATES = CONFIG["KEYWORD_RETRIEVAL_CANDIDATES"]
RRF_RANK_CONSTANT = CONFIG["RRF_RANK_CONSTANT"]
TOKEN_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    text = re.sub(r"<[^>]+>", " ", text)
    return TOKEN_PATTERN.findall(text.casefold())


def _document_key(document: Document) -> tuple[str, object]:
    source = str(document.metadata.get("source", ""))
    chunk_index = document.metadata.get("chunk_index")
    return source, chunk_index if chunk_index is not None else document.page_content


def fuse_ranked_documents(
    ranked_lists: list[list[Document]],
    k: int = TOP_K,
) -> list[tuple[Document, float]]:
    fused_scores = {}
    documents_by_key = {}
    for ranked_documents in ranked_lists:
        seen = set()
        for rank, document in enumerate(ranked_documents, start=1):
            key = _document_key(document)
            if key in seen:
                continue
            seen.add(key)
            fused_scores[key] = fused_scores.get(key, 0.0) + 1 / (
                RRF_RANK_CONSTANT + rank
            )
            documents_by_key[key] = document

    ranked_keys = sorted(fused_scores, key=fused_scores.get, reverse=True)
    return [(documents_by_key[key], fused_scores[key]) for key in ranked_keys[:k]]


@st.cache_resource(show_spinner="Connecting to the Syariah Court resources...")
def build_index():
    """Load Chroma and build a cached BM25 index over the same chunks."""
    vector_store = load_configured_vector_store()
    records = vector_store.get(include=["documents", "metadatas"])
    documents = [
        Document(page_content=text, metadata=metadata or {})
        for text, metadata in zip(
            records.get("documents") or [],
            records.get("metadatas") or [],
        )
        if text
    ]
    tokenized_documents = [
        tokenize(f"{document.metadata.get('section_path', '')} {document.page_content}")
        for document in documents
    ]
    keyword_index = BM25Okapi(tokenized_documents) if tokenized_documents else None
    return vector_store, documents, keyword_index


def retrieve(question, k=TOP_K):
    """Fuse vector and keyword rankings, retaining the best source chunks."""
    vector_store, keyword_documents, keyword_index = build_index()
    relevance_score_fn = vector_store._select_relevance_score_fn()
    vector_results = vector_store.similarity_search_with_score(
        question,
        k=VECTOR_CANDIDATES,
    )
    vector_candidates = []
    vector_scores = {}
    for document, distance in vector_results:
        score = float(relevance_score_fn(distance))
        key = _document_key(document)
        vector_candidates.append(document)
        vector_scores[key] = score

    keyword_candidates = []
    keyword_ranks = {}
    query_tokens = tokenize(question)
    if keyword_index and query_tokens:
        keyword_scores = keyword_index.get_scores(query_tokens)
        candidate_indices = sorted(
            range(len(keyword_documents)),
            key=lambda index: keyword_scores[index],
            reverse=True,
        )
        for index in candidate_indices:
            if keyword_scores[index] <= 0:
                break
            document = keyword_documents[index]
            key = _document_key(document)
            keyword_candidates.append(document)
            keyword_ranks[key] = len(keyword_candidates)
            if len(keyword_candidates) >= KEYWORD_CANDIDATES:
                break

    results = fuse_ranked_documents(
        [vector_candidates, keyword_candidates],
        k=k,
    )
    return [
        {
            "source": document.metadata.get("title") or document.metadata.get("source", "Unknown"),
            "source_url": document.metadata.get("source_url"),
            "text": document.page_content,
            "hybrid_score": float(score),
            "vector_score": vector_scores.get(_document_key(document)),
            "keyword_rank": keyword_ranks.get(_document_key(document)),
        }
        for document, score in results
    ]


def build_system_prompt(question, base_prompt):
    """Combine the base instructions with the retrieved context."""
    hits = retrieve(question)
    context_parts = []
    for hit in hits:
        source_label = hit["source"]
        if hit["source_url"]:
            source_label += f" ({hit['source_url']})"
        context_parts.append(f"[Source: {source_label}]\n{hit['text']}")
    context = "\n\n".join(context_parts)
    prompt = f"""{base_prompt}

Answer the user's question using ONLY the official Syariah Court context below. If the
answer is not in the context, say you don't know and suggest the
user contact the Syariah Court (Tel 6354 8371) or a lawyer. Do not make things up.
When naming sources, format each source that has a URL in the context as a Markdown link:
[source title](source URL). Use plain source titles when no URL is provided, and never
invent a URL. This is general information, not legal advice.

<context>
{context}
</context>"""
    return prompt, hits
