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


# ── Steps everyone goes through ───────────────────────────────────────────────
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

# ── After mediation, the process splits into two paths ────────────────────────
agree, no_agree = st.columns(2)

with agree:
    with st.container(border=True):
        st.markdown(
            '<div style="text-align:center;font-weight:700;color:#2e7d32">✅ If you reach an agreement</div>',
            unsafe_allow_html=True,
        )
        arrow()
        step("6", "Consent Hearing", "The Court reviews your agreement and grants
