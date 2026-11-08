"""
Entry point. Defines the sidebar menu (names, icons and order).
Streamlit Cloud runs this file, so keep the name main.py.
"""
import streamlit as st

pages = [
    st.Page("pages/0_home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/1_💬_Chatbot.py", title="Ask the Assistant", icon="💬"),
    st.Page("pages/3_❓_FAQs.py", title="FAQs", icon="❓"),
    st.Page("pages/4_🔗_Useful_Links.py", title="Useful Links", icon="🔗"),
    st.Page("pages/2_ℹ️_About.py", title="About", icon="ℹ️"),
]

st.navigation(pages).run()
