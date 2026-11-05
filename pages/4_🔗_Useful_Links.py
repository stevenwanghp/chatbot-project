import streamlit as st
from helper_functions.utility import check_password

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="Useful Links",
    page_icon="🔗",
)

# Do not continue if check_password is not True.
if not check_password():
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

st.title("🔗 Useful Links")

st.write("Here are some helpful resources for this chatbot app and its underlying tools:")

links = [
    ("Streamlit Documentation", "https://docs.streamlit.io/"),
    ("OpenAI API Documentation", "https://platform.openai.com/docs/"),
    ("OpenAI Models Overview", "https://platform.openai.com/docs/models"),
    ("GitHub Repository", "https://github.com/stevenwanghp/chatbot-project"),
]

for label, url in links:
    st.markdown(f"- [{label}]({url})")

st.info(
    "Use these links to learn more about the tools and services that power this app."
)
