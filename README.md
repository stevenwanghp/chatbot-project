# Syariah Court Divorce Process Assistant

A Streamlit retrieval-augmented chatbot that answers general questions about the Singapore Syariah Court divorce process using official court resources. It is an informational student project, not an official court service or a substitute for legal advice.

## Features

- Answers questions using retrieved official Syariah Court content.
- Shows source titles, links, and relevance scores with each answer.
- Filters retrieval results using the relevance threshold in `config.yaml`.
- Includes FAQs, useful links, and app methodology pages.
- Logs chat queries, retrieved chunks, assistant responses, and errors locally.

## Requirements

- Python 3.10 or later
- An OpenAI API key with access to the configured chat and embedding models

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root for local development:

```dotenv
OPENAI_API_KEY=your-openai-api-key
```

The Streamlit pages also require an access password. Add it to `.streamlit/secrets.toml`:

```toml
password = "choose-a-local-access-password"
```

Keep `.env` and `.streamlit/secrets.toml` private; they are excluded from version control.

## Run

From the project root with the virtual environment active:

```bash
streamlit run main.py
```

## Refresh the Knowledge Base

The repository includes processed Markdown and a persistent Chroma database. To convert PDFs in `data/`, fetch the configured official web pages, and rebuild the vector store, ensure `OPENAI_API_KEY` is set in `.env`, then run:

```bash
python "pre-processing/pdf_to_markdown.py"
python "pre-processing/fetch_official_pages.py"
python "pre-processing/markdown_to_vectorstore.py"
```

The PDF converter scans `data/` and writes Markdown to `data_processed/` by default. It accepts a PDF file or directory as its first argument and `-o` or `--output-dir` to change the destination. The fetcher uses the URLs allowlisted in `config.yaml`. To fetch one configured page only:

```bash
python "pre-processing/fetch_official_pages.py" --url "https://syariahcourt.gov.sg/Divorce/Overview"
```

The indexer accepts an optional Markdown file or directory as its first argument. Run any preprocessing script with `--help` to see its options.

## Configuration

Application and ingestion settings are in `config.yaml`, including chat and embedding models, system prompt, generation parameters, chunking, vector-store location, source URLs, retrieval count, minimum relevance score, and log rotation. The Streamlit visual theme is configured separately in `.streamlit/config.toml`.

## Logs and Privacy

Chat interaction logs are written to `logs/assistant.log` by default, with rotation controlled by `LOG_MAX_BYTES` and `LOG_BACKUP_COUNT` in `config.yaml`. Logs may contain sensitive user queries, retrieved source text, assistant responses, and error details. The `logs/` directory is ignored by Git; restrict access to the files and remove them when they are no longer needed.

## Project Layout

- `main.py`: Streamlit multipage app entry point.
- `pages/`: Home, chatbot, About, FAQ, and useful-links pages.
- `helper_functions/`: Configuration, LLM, retrieval, vector-store, logging, and shared UI helpers.
- `pre-processing/`: Fetches official pages and builds the Chroma index.
- `data_processed/`: Processed source Markdown.
- `chroma_db/`: Persistent Chroma vector database.
