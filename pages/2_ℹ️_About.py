import streamlit as st
from helper_functions.config import load_config
from helper_functions.utility import check_password
from helper_functions.ui import apply_theme, page_header, footer

CONFIG = load_config()

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="About",
    page_icon="ℹ️",
)
apply_theme()

# Do not continue if check_password is not True.
if not check_password():
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

page_header("About This App", "What this assistant does, how it works, and its limits.", "ℹ️")

st.markdown(f"""
### Overview
The SYC Divorce Process Assistant uses OpenAI's {CONFIG['OPENAI_MODEL']} model to answer
questions about the Syariah Court divorce process. It is trained on approved content from the Syariah Court website, and is designed to provide accurate and relevant information while adhering to strict guardrails to ensure safety and compliance.

### Scope
This chatbot covers the **Syariah Court divorce process only**:
1. Eligibility to file for divorce at the Syariah Court
2. Marriage Counselling Programme
3. Filing the Originating Summons
4. Serving the Originating Summons
5. Mediation
6. Pre-Trial Conference
7. Hearing

**Out of scope**: the chatbot will politely decline and redirect:
- Legal advice or questions about the merits of a specific case
- Other Syariah Court services (e.g. inheritance certificates)
- Civil court divorce matters
- Questions unrelated to divorce


### How the chatbot works
""")
st.graphviz_chart("""
digraph {
    node [shape=box, style=rounded]
    Q [label="User asks a question"]
    C [label="Is it about the SYC divorce process?", shape=diamond]
    N [label="Polite reply: I can only help with SYC divorce procedures"]
    R [label="Find relevant SYC content"]
    L [label="LLM answers using that content only"]
    A [label="Show answer + sources"]
    Q -> C
    C -> N [label="No"]
    C -> R [label="Yes"]
    R -> L -> A
}
""")
st.markdown(f"""

### Tech stack
| Component | Tool |
|---|---|
| Interface | Streamlit |
| Language model | OpenAI {CONFIG['OPENAI_MODEL']} |
| Embedding model | OpenAI {CONFIG['EMBEDDING_MODEL']} |
| Vector search | Chroma similarity search |
| Keyword search | BM25 |
| PDF parsing to markdown | pymupdf |


### Data source
- Approved content from the Syariah Court of Singapore website

### Retrieval
Markdown documents are processed in two stages. First,
`MarkdownHeaderTextSplitter` divides each document at its headings and keeps the heading
context with each section. Then `RecursiveCharacterTextSplitter` divides long sections into
smaller chunks, targeting {CONFIG['CHUNK_SIZE']} characters with
{CONFIG['CHUNK_OVERLAP']} characters of overlap. This combination keeps related content
with its heading while avoiding oversized chunks; using only heading splitting could leave
very long sections intact, while character-only splitting could separate content from its
heading. Page and section headings are retained with each chunk to preserve context.

For each question, the assistant uses a **hybrid search approach, combining vector and keyword searches**.
It searches Chroma by vector similarity and ranks the same content with BM25 keyword search.
Vector search can find relevant passages when a question is phrased differently from the source;
BM25 can surface passages containing exact terms,
such as specific procedure names. Using both helps cover semantic matches and precise
legal vocabulary. RRF combines their rankings so neither method's score scale dominates.
It considers up to
{CONFIG['VECTOR_RETRIEVAL_CANDIDATES']} candidates from each method, then combines their
rankings using reciprocal rank fusion (RRF, rank constant
{CONFIG['RRF_RANK_CONSTANT']}). The top {CONFIG['RETRIEVAL_TOP_K']} combined results are
provided to the language model as its answer context.

### Guardrails
- Answers only from approved SYC content
- Does not give legal advice; redirects to a lawyer or legal clinic if asked 
- Shows emergency contacts if a user mentions being in danger 
- Uses delimiters to protect against prompt injection
- Password-protected, with a disclaimer on every page
""")

footer()
