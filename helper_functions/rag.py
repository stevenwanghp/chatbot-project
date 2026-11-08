"""Retrieve relevant Syariah Court content from the persistent Chroma store."""

import streamlit as st

from helper_functions.config import load_config
from helper_functions.vectorstore import load_configured_vector_store

TOP_K = load_config()["RETRIEVAL_TOP_K"]
MIN_RELEVANCE_SCORE = load_config()["MIN_RELEVANCE_SCORE"]


@st.cache_resource(show_spinner="Connecting to the Syariah Court resources...")
def build_index():
    """Load and cache the configured persistent Chroma collection."""
    return load_configured_vector_store()


def retrieve(question, k=TOP_K):
    """Return retrieved Chroma documents scoring at least the minimum relevance."""
    results = build_index().similarity_search_with_relevance_scores(question, k=k)
    return [
        {
            "source": document.metadata.get("title") or document.metadata.get("source", "Unknown"),
            "source_url": document.metadata.get("source_url"),
            "text": document.page_content,
            "score": float(score),
        }
        for document, score in results
        if float(score) >= MIN_RELEVANCE_SCORE
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
