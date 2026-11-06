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

# ── How can we help? ──────────────────────────────────────────────────────────
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


# ── The process at a glance ───────────────────────────────────────────────────
st.markdown("### The process at a glance")


def step(num, title, text=""):
    """Draws one numbered circle with a title and short description."""
    st.markdown(
        f"""<div style="text-align:center">
              <div style="width:42px;height:42px;margin:0 auto .4rem;border-radius:50%;
                   background:#810E07;color:#fff;font-weight:900;line-height:42px">{num}</div>
              <div style="font-weight:700;color:#223780">{title}</div>
              <div style="font-size:.82rem;color:#555">{text}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def arrow():
    """Draws a small downward arrow between steps."""
    st.markdown(
        '<div style="text-align:center;color:#810E07;font-size:1.4rem;margin:.3rem 0">↓</div>',
        unsafe_allow_html=True,
    )


def branch_title(text, colour):
    """Draws the heading at the top of each path box."""
    st.markdown(
        f'<div style="text-align:center;font-weight:700;color:{colour}">{text}</div>',
        unsafe_allow_html=True,
    )


# Steps everyone goes through
steps = [
    ("1", "Counselling", "Register on the SYC Portal and attend the Marriage Counselling Programme."),
    ("2", "File the Originating Summons", "One spouse files the Originating Summons within 6 months."),
    ("3", "Serve the Originating Summons", "[Add description]"),
    ("4", "Memorandum of Defence", "[Add description]"),
    ("5", "Mediation", "Helps both parties agree on the divorce and ancillary matters."),
]

cols = st.columns(len(steps))
for col, (num, title, text) in zip(cols, steps):
    with col:
        step(num, title, text)

arrow()

# After mediation, the process splits into two paths
agree, no_agree = st.columns(2)

with agree:
    with st.container(border=True):
        branch_title("✅ Agreement reached", "#2e7d32")
        arrow()
        step("6", "Consent Hearing", "The Court reviews your agreement and grants the divorce.")

with no_agree:
    with st.container(border=True):
        branch_title("❌ No agreement", "#810E07")
        arrow()
        step("6", "Pre-Trial Conference", "The Court prepares the case for hearing.")
        arrow()
        step("7", "Hearing", "The Court hears the case and decides.")

footer()
