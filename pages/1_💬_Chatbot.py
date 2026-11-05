import streamlit as st
from helper_functions.llm import get_completion_stream, count_tokens
from helper_functions.utility import check_password
from helper_functions.rag import build_system_prompt

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="Chatbot",
    page_icon="💬",
)

# Do not continue if check_password is not True.
if not check_password():
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

st.title("💬 AI Chatbot")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a friendly assistant that helps people understand the divorce process at the Syariah Court Singapore.",
        height=120,
    )
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        total_tokens = sum(
            count_tokens(m["content"]) for m in st.session_state.messages
        )
        st.metric("Estimated Tokens Used", total_tokens)

# ── Chat history ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        # RAG: find the most relevant parts of the guide and add them to the system prompt
        rag_prompt, sources = build_system_prompt(user_input, system_prompt)
        full_messages = [{"role": "system", "content": rag_prompt}] + st.session_state.messages
        response = st.write_stream(get_completion_stream(full_messages))

        with st.expander("📄 Sources used from the guide"):
            for s in sources:
                st.markdown(f"**Page {s['page']}** (relevance {s['score']:.2f})")
                st.caption(s["text"][:300] + "...")

    st.session_state.messages.append({"role": "assistant", "content": response})
