import traceback
from uuid import uuid4

import streamlit as st
from helper_functions.llm import get_completion_stream, count_tokens
from helper_functions.app_logging import log_chat_interaction
from helper_functions.config import load_config
from helper_functions.utility import check_password
from helper_functions.rag import build_system_prompt
from helper_functions.ui import apply_theme, page_header, footer

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="Ask the Assistant",
    page_icon="💬",
)
apply_theme()

# Do not continue if check_password is not True.
if not check_password():
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->
CONFIG = load_config()
USER_AVATAR = "🙂"
BOT_AVATAR = "⚖️"
SYSTEM_PROMPT = CONFIG["SYSTEM_PROMPT"]
SUGGESTIONS = [
    "Who can apply for divorce at the Syariah Court?",
    "What is the Marriage Counselling Programme?",
    "How long do I have to serve the Originating Summons?",
    "Can we still reconcile after talak?",
]

page_header(
    "Ask the Assistant",
    "Ask anything about the divorce process. Answers are grounded in official Syariah Court resources.",
    "💬",
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💬 Conversation")
    if st.button("🗑️ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        total_tokens = sum(count_tokens(m["content"]) for m in st.session_state.messages)
        st.metric("Estimated tokens used", total_tokens)

    with st.expander("⚙️ Advanced settings"):
        system_prompt = st.text_area("System prompt", value=SYSTEM_PROMPT, height=160)

    st.caption("Need to speak to someone? Syariah Court: **6354 8371**")

# ── Chat history ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

pending = None

if not st.session_state.messages:
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        st.markdown(
            "**Assalamualaikum and welcome.** I can explain eligibility, counselling, filing, "
            "fees, reconciliation, appeals and what happens after a divorce.\n\n"
            "Pick a question below or type your own."
        )
    cols = st.columns(2)
    for i, q in enumerate(SUGGESTIONS):
        if cols[i % 2].button(q, key=f"suggest_{i}", use_container_width=True):
            pending = q

for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Type your question here...") or pending

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_input)

    interaction_id = str(uuid4())
    sources = []
    response = ""
    error_details = None
    phase = "retrieval"
    try:
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            # RAG: find the most relevant parts of the guide and add them to the system prompt
            with st.spinner("Searching Syariah Court resources..."):
                rag_prompt, sources = build_system_prompt(user_input, system_prompt)
            phase = "generation"
            full_messages = [{"role": "system", "content": rag_prompt}] + st.session_state.messages
            response = st.write_stream(get_completion_stream(full_messages))

            with st.expander("📄 Sources used"):
                for s in sources:
                    if s["source_url"]:
                        source_label = f"[{s['source']}]({s['source_url']})"
                    else:
                        source_label = s["source"]
                    st.markdown(f"**{source_label}** · relevance {s['score']:.2f}")
                    st.caption(s["text"][:300] + "...")
    except Exception as error:
        error_details = {
            "phase": phase,
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
        }
        st.error("Sorry, something went wrong while preparing your answer.")
    finally:
        log_chat_interaction(
            interaction_id=interaction_id,
            query=user_input,
            retrieved_chunks=sources,
            response=response,
            error=error_details,
        )

    if not error_details:
        st.session_state.messages.append({"role": "assistant", "content": response})
    if pending:
        st.rerun()  # hide the suggestion buttons once a question has been asked

footer()
