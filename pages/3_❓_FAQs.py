import streamlit as st
from helper_functions.utility import check_password
from helper_functions.ui import apply_theme, page_header, footer

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="FAQs",
    page_icon="❓",
)
apply_theme()

# Do not continue if check_password is not True.
if not check_password():
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

FAQ_DISCLAIMER = (
    "This page gives general information only and is not legal advice. "
    "For the full details, refer to the SYC Divorce Guide or contact the Syariah Court."
)

FAQS = [
    # --- Eligibility ---
    {
        "category": "Eligibility",
        "question": "Am I eligible to file for divorce at the Syariah Court?",
        "answer": (
            "You may apply for divorce at the Syariah Court if you and your spouse are Muslims, "
            "or were married under Muslim law, AND either of you:\n\n"
            "- is a Singapore citizen; or\n"
            "- has lived in Singapore for at least 3 continuous years before applying; or\n"
            "- is domiciled in Singapore (Singapore is the country you treat as your permanent "
            "home, or have a substantial connection with)."
        ),
    },
    {
        "category": "Eligibility",
        "question": "Neither of us is a Singapore citizen. What do we need to show?",
        "answer": (
            "You must show proof of residence in Singapore for the 3 years before your application, "
            "for example an employment pass showing your length of stay, an employment agreement, "
            "or a tenancy agreement."
        ),
    },
    # --- Before filing ---
    {
        "category": "Before Filing",
        "question": "What is the first step if I want a divorce?",
        "answer": (
            "Register for the compulsory Marriage Counselling Programme (MCP) online on the "
            "SYC Portal (eservices.syariahcourt.gov.sg). You must attend the MCP before you can "
            "file for divorce."
        ),
    },
    {
        "category": "Before Filing",
        "question": "Can I be exempted from the Marriage Counselling Programme?",
        "answer": (
            "Possibly, if a critical or terminal illness, or a physical disability or infirmity, "
