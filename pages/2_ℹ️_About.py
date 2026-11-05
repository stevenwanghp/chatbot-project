import streamlit as st
from helper_functions.utility import check_password
from helper_functions.ui import apply_theme, page_header, footer

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

st.markdown("""
### What it does
This assistant helps people understand the **divorce process at the Syariah Court Singapore**:
eligibility, counselling, filing, fees, reconciliation, appeals and life after divorce.

### How it works
- 📄 **Grounded answers (RAG)**: each question is matched to the most relevant pages of the official
  Syariah Court divorce guide, and the AI answers only from those pages, citing page numbers.
- 💬 **Conversational**: ask follow-up questions in plain language.
- 🔒 **Password protected**: access with a shared password.

### Tech stack
| Component | Tool |
|---|---|
| Interface | Streamlit |
| Language model | OpenAI GPT-4o-mini |
| Retrieval | OpenAI text-embedding-3-small + NumPy |
| PDF reading | pypdf |

### Limits
- It only knows what is in the guide. If the answer isn't there, it will say so.
- It gives **general information, not legal advice**. Court staff can't give legal advice either,
  so speak to a lawyer, the Legal Aid Bureau or Pro Bono SG about your own case.
""")

footer()
