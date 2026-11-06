import streamlit as st
from helper_functions.utility import check_password
from helper_functions.ui import apply_theme, page_header, footer

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="Syariah Court Divorce Guide",
    page_icon="⚖️",
)
apply_theme()

# Do not continue if check_password is not True.
if not check_password():
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

page_header(
    "Understanding Divorce at the Syariah Court",
    "Clear, step-by-step answers for anyone thinking about, going through, "
    "or supporting someone through a divorce under Muslim law in Singapore.",
    "⚖️",
)

st.markdown("### How can we help?")

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown("#### 💬 Ask a question")
        st.write("Chat with our assistant. Answers come from the official Syariah Court website and divorce guide.")
        st.page_link("pages/1_💬_Chatbot.py", label="Start chatting →")
with col2:
    with st.container(border=True):
        st.markdown("#### ❓ FAQs")
        st.write("Eligibility, counselling, fees, reconciliation, appeals and more.")
        st.page_link("pages/3_❓_FAQs.py", label="Browse FAQs →")
with col3:
    with st.container(border=True):
        st.markdown("#### 🔗 Resources")
        st.write("Official forms, the SYC Portal, legal aid and support services.")
        st.page_link("pages/4_🔗_Useful_Links.py", label="See resources →")
st.markdown("### The process at a glance")

# Steps everyone goes through
steps = [
    ("1", "Counselling", "Register on the SYC Portal and attend the Marriage Counselling Programme."),
    ("2", "File the Originating Summons", "One spouse files the Originating Summons within 6 months."),
    ("3", "Serve the Originating Summons", "[Add description]"),
    ("4", "Spouse files the Memorandum of Defence", "[Add description]"),
    ("5", "Mediation", "Helps both parties agree on the divorce and ancillary matters."),
]

for number, title, description in steps:
    st.markdown(f"**{number}. {title}**  \n{description}")

# After mediation, the process splits into two paths
st.markdown("**6. After mediation**")
agree, no_agree = st.columns(2)

with agree:
    st.success(
        "✅ **If you reach an agreement**\n\n"
        "➡️ **Consent Hearing**: the Court reviews your agreement and grants the divorce."
    )

with no_agree:
    st.warning(
        "❌ **If you don't reach an agreement**\n\n"
        "➡️ **Pre-Trial Conference**\n\n"
        "➡️ **Hearing**: the Court hears the case and decides."
    )

cols = st.columns(len(steps))
for col, (num, title, text) in zip(cols, steps):
    with col:
        st.markdown(
            f"""<div style="text-align:center">
                  <div style="width:42px;height:42px;margin:0 auto .4rem;border-radius:50%;
                       background:#810E07;color:#fff;font-weight:900;line-height:42px">{num}</div>
                  <div style="font-weight:700;color:#223780">{title}</div>
                  <div style="font-size:.82rem;color:#555">{text}</div>
                </div>""",
            unsafe_allow_html=True,
        )

footer()
