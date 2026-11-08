from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from helper_functions.config import load_config
from pathlib import Path

CONFIG = load_config()

def create_embeddings():
    return OpenAIEmbeddings(model=CONFIG["EMBEDDING_MODEL"])

# def get_embeddings(texts, model):
#     response=_get_client().embeddings.create(
#         input=texts,
#         model=model
#     )
#     return [x.embedding for x in response.data]

def create_text_splitter(
    chunk_size=CONFIG["CHUNK_SIZE"],
    chunk_overlap=CONFIG["CHUNK_OVERLAP"],
):
    return RecursiveCharacterTextSplitter(
        separators=CONFIG["CHUNK_SEPARATORS"],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )


def create_vector_store(collection_name, persist_directory, embeddings=None):
    return Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=embeddings or create_embeddings(),
    )

def load_vector_store(collection_name, persist_directory, embeddings=None):
    return Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=embeddings or create_embeddings(),
    )


def load_configured_vector_store():
    project_root = Path(__file__).resolve().parents[1]
    return load_vector_store(
        collection_name=CONFIG["VECTOR_STORE_COLLECTION"],
        persist_directory=str(project_root / CONFIG["VECTOR_STORE_DIRECTORY"]),
    )


def retrieve_relevant_chunks(query, vector_store, k=CONFIG["RETRIEVAL_TOP_K"]):
    return vector_store.similarity_search(query, k=k)


def format_retrieved_context(documents):
    return "\n\n".join(
        f"Source: {document.metadata.get('source', 'Unknown')}\n{document.page_content}"
        for document in documents
    )