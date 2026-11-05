"""
Simple RAG (Retrieval-Augmented Generation) over the Syariah Court divorce guide.

How it works:
1. Read the PDF and split each page into small overlapping chunks.
2. Turn every chunk into an embedding (a list of numbers) with OpenAI.
3. When the user asks a question, embed the question too.
4. Pick the chunks whose embeddings are closest to the question (cosine similarity).
5. Paste those chunks into the system prompt so the LLM answers from them.
"""
from pathlib import Path

import numpy as np
import streamlit as st
from pypdf import PdfReader

from helper_functions.llm import client

PDF_PATH = Path(__file__).resolve().parent.parent / "data" / "sycdivorceguides-eng.pdf"
EMBED_MODEL = "text-embedding-3-small"
CHUNK_WORDS = 200      # size of each chunk
OVERLAP_WORDS = 40     # words shared between neighbouring chunks
TOP_K = 4              # how many chunks to give the LLM


def load_chunks(pdf_path=PDF_PATH):
    """Return a list of {'page': n, 'text': '...'} chunks from the PDF."""
    chunks = []
    for page_no, page in enumerate(PdfReader(pdf_path).pages, start=1):
        words = (page.extract_text() or "").split()
        step = CHUNK_WORDS - OVERLAP_WORDS
        for start in range(0, len(words), step):
            piece = words[start:start + CHUNK_WORDS]
            if len(piece) < 20:          # skip tiny leftovers / blank pages
                continue
            chunks.append({"page": page_no, "text": " ".join(piece)})
    return chunks


def embed(texts):
    """Embed a list of strings. Returns an (n, d) numpy array of unit vectors."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vecs = np.array([d.embedding for d in resp.data], dtype=np.float32)
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)


@st.cache_resource(show_spinner="Reading the divorce guide...")
def build_index():
    """Runs once per app start; Streamlit caches the result."""
    chunks = load_chunks()
    vectors = embed([c["text"] for c in chunks])
    return chunks, vectors


def retrieve(question, k=TOP_K):
    """Return the k chunks most relevant to the question."""
    chunks, vectors = build_index()
    q = embed([question])[0]
    scores = vectors @ q                      # cosine similarity (vectors are normalised)
    best = np.argsort(scores)[::-1][:k]
    return [{**chunks[i], "score": float(scores[i])} for i in best]


def build_system_prompt(question, base_prompt):
    """Combine the base instructions with the retrieved context."""
    hits = retrieve(question)
    context = "\n\n".join(f"[Page {h['page']}]\n{h['text']}" for h in hits)
    prompt = f"""{base_prompt}

Answer the user's question using ONLY the context below, taken from the Syariah Court
divorce guide. If the answer is not in the context, say you don't know and suggest the
user contact the Syariah Court (Tel 6354 8371) or a lawyer. Do not make things up.
Mention the page number(s) you used, e.g. "(Guide, p.7)". This is general information,
not legal advice.

<context>
{context}
</context>"""
    return prompt, hits
