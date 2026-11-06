"""
Shared look and feel for every page.
Colours match syariahcourt.gov.sg: maroon #810E07, navy #223780, charcoal #323232.

Usage on each page, right after st.set_page_config(...):
    from helper_functions.ui import apply_theme, page_header, footer
    apply_theme()
    page_header("Ask about divorce", "Answers from the official Syariah Court guide", "💬")
    ...
    footer()
"""
import streamlit as st

# ── Colours ───────────────────────────────────────────────────────────────────
MAROON = "#810E07"
MAROON_DARK = "#5A0904"
NAVY = "#223780"
CHARCOAL = "#323232"

# ── Font sizes (change these to resize text on EVERY page) ────────────────────
TEXT_SIZE = "1rem"          # normal text, lists, FAQ answers, chat messages
SMALL_SIZE = ".85rem"       # captions, notes, footer, step descriptions
H1_SIZE = "1.9rem"          # page title in the maroon banner
H2_SIZE = "1.5rem"          # st.header / ## headings
H3_SIZE = "1.25rem"         # st.subheader / ### headings
H4_SIZE = "1.1rem"          # #### headings (e.g. card titles)

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap');

html, body, [class*="css"], .stMarkdown, .stChatMessage {{ font-family: 'Lato', sans-serif; }}

/* Tidy the default Streamlit chrome */
#MainMenu, footer {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; max-width: 860px; }}

/* ── Standard font sizes ── */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] p {{ font-size: {TEXT_SIZE} !important; line-height: 1.6; }}
h1 {{ font-size: {H1_SIZE} !important; }}
h2 {{ font-size: {H2_SIZE} !important; }}
h3 {{ font-size: {H3_SIZE} !important; }}
h4 {{ font-size: {H4_SIZE} !important; }}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{ font-size: {SMALL_SIZE} !important; }}

/* Page header banner */
.syc-header {{
    background: linear-gradient(120deg, {MAROON} 0%, {MAROON_DARK} 100%);
    color: #fff; border-radius: 14px; padding: 1.6rem 1.8rem 1.4rem;
    margin-bottom: 1.4rem; box-shadow: 0 6px 18px rgba(129,14,7,.18);
    border-bottom: 5px solid {NAVY};
}}
.syc-header .eyebrow {{ font-size: .75rem; letter-spacing: .14em; text-transform: uppercase; opacity: .8; }}
.syc-header h1 {{ color: #fff; font-weight: 900; font-size: {H1_SIZE} !important; margin: .2rem 0 .3rem; padding: 0; }}
.syc-header p {{ margin: 0; opacity: .92; font-size: {TEXT_SIZE} !important; }}

/* Headings */
h2, h3 {{ color: {NAVY}; font-weight: 700; }}

/* Cards (st.container(border=True)) */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: #fff; transition: box-shadow .15s ease, transform .15s ease;
}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    box-shadow: 0 6px 16px rgba(0,0,0,.07); transform: translateY(-1px);
}}

/* Expanders (FAQ) */
[data-testid="stExpander"] details {{ border-left: 4px solid {MAROON}; background: #fff; }}
[data-testid="stExpander"] summary p {{ font-size: {TEXT_SIZE} !important; font-weight: 700; }}
[data-testid="stExpander"] summary:hover {{ color: {MAROON}; }}

/* Buttons */
.stButton > button {{
    border-radius: 999px; border: 1px solid {MAROON}; color: {MAROON};
    background: #fff; font-weight: 700; font-size: {TEXT_SIZE}; transition: all .15s ease;
}}
.stButton > button:hover {{ background: {MAROON}; color: #fff; border-color: {MAROON}; }}

/* Chat */
[data-testid="stChatMessage"] {{ border-radius: 14px; padding: .9rem 1rem; }}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{ background: #F3F5FB; }}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
    background: #fff; border: 1px solid #EEE5E3;
}}
[data-testid="stChatInput"] textarea {{ font-family: 'Lato', sans-serif; font-size: {TEXT_SIZE}; }}

/* Sidebar */
[data-testid="stSidebar"] {{ border-right: 4px solid {MAROON}; }}
[data-testid="stSidebarNav"] a[aria-current="page"] {{ background: rgba(129,14,7,.08); }}
[data-testid="stSidebarNav"] a[aria-current="page"] span {{ color: {MAROON}; font-weight: 700; }}

/* Note box */
.syc-note {{ background: #FBF7F6; border-left: 4px solid {NAVY}; border-radius: 8px;
    padding: .8rem 1rem; font-size: {SMALL_SIZE}; color: #484848; margin-bottom: 1rem; }}

/* Section headings inside pages */
[data-testid="stHeading"] h2, [data-testid="stHeading"] h3 {{ color: {NAVY}; }}

/* Footer */
.syc-footer {{
    margin-top: 3rem; padding: 1rem 1.2rem; border-radius: 10px;
    background: #191919; color: #B7B7B7; font-size: {SMALL_SIZE}; line-height: 1.5;
}}
.syc-footer b {{ color: #fff; }}
</style>
"""


def apply_theme():
    """Inject the shared CSS. Call once per page, after st.set_page_config."""
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(title, subtitle="", icon="", eyebrow="Syariah Court Divorce Guide"):
    """Maroon banner with a navy underline, like the court website."""
    st.markdown(
        f"""<div class="syc-header">
              <div class="eyebrow">{eyebrow}</div>
              <h1>{icon} {title}</h1>
              <p>{subtitle}</p>
            </div>""",
        unsafe_allow_html=True,
    )


def footer():
    """Dark footer with the disclaimer and contact details."""
    st.markdown(
        """<div class="syc-footer">
            <b>General information only, not legal advice.</b> This is a student project for an
            AI Bootcamp and is not an official Syariah Court service. For help with your case,
            contact the Syariah Court: Family Link @ Lengkok Bahru, 8 Lengkok Bahru #03-01,
            Singapore 159052 · Tel 6354 8371 · MCCY_Syariah@mccy.gov.sg
        </div>""",
        unsafe_allow_html=True,
    )


def note(text):
    """Soft grey note with a navy edge, for disclaimers."""
    st.markdown(f'<div class="syc-note">ℹ️ {text}</div>', unsafe_allow_html=True)
