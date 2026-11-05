import streamlit as st
from helper_functions.utility import check_password

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="FAQs",
    page_icon="❓",
)

# Do not continue if check_password is not True.
if not check_password():
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

st.title("❓ Frequently Asked Questions")

with st.expander("How do I start a conversation?"):
    st.write("Open the 💬 Chatbot page, type a message in the chat box, and press Enter.")

with st.expander("Can I customize how the chatbot responds?"):
    st.write(
        "Yes. Edit the **System Prompt** in the sidebar on the Chatbot page to guide "
        "the assistant's behavior."
    )

with st.expander("How do I start over?"):
    st.write(
        "Select **🗑️ Clear Conversation** in the Chatbot page's sidebar to clear "
        "the current conversation."
    )

with st.expander("What does the token estimate measure?"):
    st.write(
        "The sidebar shows an estimate of tokens used by the messages in the current "
        "chat. It is an estimate, not a billing total."
    )

with st.expander("Which AI model does this app use?"):
    st.write("The app uses OpenAI GPT-4o-mini.")

with st.expander("Can I rely on the chatbot for professional advice?"):
    st.write(
        "No. The chatbot is for educational and demonstration purposes. Its responses "
        "should not be taken as professional advice."
    )
