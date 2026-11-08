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

### Data source
- Approved content from the Syariah Court of Singapore website

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
st.markdown("""

### Tech stack
| Component | Tool |
|---|---|
| Interface | Streamlit |
| Language model | OpenAI {CONFIG['OPENAI_MODEL']} |
| Retrieval | OpenAI {CONFIG['EMBEDDING_MODEL']} + NumPy |
| Vector DB | Chroma |
| PDF reading | pypdf |

### Guardrails
- Answers only from approved SYC content
- Does not give legal advice; redirects to a lawyer or legal clinic if asked 
- Shows emergency contacts if a user mentions being in danger 
- Uses delimiters to protect against prompt injection
- Password-protected, with a disclaimer on every page
""")

footer()
