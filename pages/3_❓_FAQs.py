import streamlit as st
from helper_functions.utility import check_password
from helper_functions.ui import apply_theme, page_header, footer, note

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

# FAQ page content - Syariah Court divorce chatbot site.
# Source: syariahcourt.gov.sg (checked 5 Nov 2026) plus linked government sites.
# General information only - not legal advice.

DISCLAIMER = (
    "This page gives general information about divorce at the Syariah Court Singapore. "
    "It is not legal advice. Court staff cannot give legal advice or prepare documents for you, "
    "so please speak to a lawyer about your own situation. "
    "Syariah Court: Family Link @ Lengkok Bahru, 8 Lengkok Bahru, #03-01, Singapore 159052 | "
    "Tel: 6354 8371 | Email: MCCY_Syariah@mccy.gov.sg"
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
            "file for divorce. MCP agencies include: AMP Singapore, APKIM Resources, "
            "Darul Arqam (Muslim Converts' Association of Singapore), Persatuan Pemudi Islam "
            "Singapura, or Reach Community Services Singapore."
        ),
    },
    {
        "category": "Before Filing",
        "question": "Can I be exempted from the Marriage Counselling Programme?",
        "answer": (
            "Possibly, if a critical or terminal illness, or a physical disability or infirmity, "
            "makes attending impractical or impossible. Apply in the 'Exemption from Counselling' "
            "section of your registration and attach proof, such as a letter from a registered "
            "medical practitioner dated no more than one month before you submit."
        ),
    },
    {
        "category": "Before Filing",
        "question": "Can I get advice on Islamic law on marriage and divorce before deciding?",
        "answer": (
            "Yes. You can get free clarification on Muslim law on marriage and divorce from a "
            "Resource Person. All Resource Persons are registered Asatizah under MUIS' Asatizah "
            "Recognition Scheme."
        ),
    },
    # --- Filing & proceedings ---
    {
        "category": "Process",
        "question": "When must I file for divorce after counselling?",
        "answer": (
            "You must file the divorce application (the Originating Summons) within 6 months of "
            "the date of the issuance email ('Pre-OS Email') you receive after completing the MCP. "
            "You file online through the SYC Portal. The person filing is the Plaintiff and the "
            "spouse is the Defendant."
        ),
    },
    {
        "category": "Process",
        "question": "How do I serve the divorce papers on my spouse?",
        "answer": (
            "You must serve the Originating Summons within 12 months of your filing being accepted. "
            "Options: through the SYC Portal (only if you have your spouse's valid email address); "
            "personal service by a Court Process Server, a solicitor or an authorised solicitor's "
            "clerk; or registered post, with your spouse signing and returning an Acknowledgement "
            "of Service. If these fail or are not possible, apply to the Court for substituted "
            "service by filing a summons with a supporting affidavit. Do not carry out substituted "
            "service until the Court has made an order."
        ),
    },
    {
        "category": "Process",
        "question": "I have been served divorce papers. What do I do?",
        "answer": (
            "You are now known as the Defendant. Acknowledge receipt and file a Memorandum of Defence on the SYC Portal within 21 days "
            "of being served. In it you say whether you agree to the divorce and the proposed "
            "arrangements, or give your own proposals."
        ),
    },
    {
        "category": "Process",
        "question": "What happens at mediation?",
        "answer": (
            "A mediator meets both of you to see whether you can agree on the divorce and the "
            "ancillary matters (such as nafkah iddah, mutaah, children and property). Each session "
            "lasts 60 minutes, and more sessions can be scheduled. If you have a lawyer, you must "
            "attend with them. If you reach agreement, and the agreement and required documents "
            "are filed and accepted by the Court, a President of the Court may hear and decide the "
            "divorce on the same day. If you do not agree, the case goes to a Pre-Trial Conference."
        ),
    },
    {
        "category": "Process",
        "question": "What if we cannot agree?",
        "answer": (
            "The case goes to a Pre-Trial Conference and then a hearing, where a President of the "
            "Court decides based on the evidence in the parties' affidavits. In contested divorces, "
            "the Court may appoint hakam (marital conciliators), one for each party, to try to "
            "reconcile you or, if that fails, to help you reach an amicable divorce. The hakam may "
            "pronounce a divorce if they jointly agree that you should divorce."
        ),
    },
    {
        "category": "Process",
        "question": "What are 'ancillary matters'?",
        "answer": (
            "These are the issues settled alongside the divorce: custody, care and control of, and "
            "access to children; nafkah iddah (maintenance for the wife during the waiting period); "
            "mutaah (a consolatory gift to the wife); hantaran belanja and emas kahwin; and the "
            "division or disposition of property. Where custody is disputed and a child is aged 7 "
            "to 21, the Court may hold a confidential Joint Child Interview. In cases with serious "
            "disputes, the Court may order a free, confidential Custody Evaluation Report."
        ),
    },
    # --- Reconciliation ---
    {
        "category": "Reconciliation",
        "question": "My husband pronounced talak outside court but we want to reconcile. What should we do?",
        "answer": (
            "Both of you must attend in person at the Syariah Court within 7 days of the talak "
            "pronouncement. The Court will decide whether the out-of-court divorce is valid. You"
            "will still need to file for a divoce. After the decree or order is issued, 
            "both of you attend in person at the Registry of Muslim "
            "Marriages (ROMM) to register the revocation of the divorce (rujuk)."
        ),
    },
    {
    # --- Appeals ---
    {
        "category": "Appeals",
        "question": "Can I appeal a decision?",
        "answer": (
            "Yes. Against a decision of the Syariah Court, file a notice of appeal with the Appeal "
            "Board at MUIS (Singapore Islamic Hub, 273 Braddell Road; Tel 6359 1199) within 30 days. "
            "Against a Registrar's direction or order, file Form 52 on the SYC Portal within 14 days; "
            "it is heard by a President of the Court. Either way, serve a copy on every other party "
            "within 3 days of filing. Get legal advice on whether your appeal has merit."
        ),
    },
        
page_header(
    "Frequently Asked Questions",
    "Common questions about the Syariah Court divorce process, from eligibility to life after divorce.",
    "❓",
)
note(DISCLAIMER)

for category in dict.fromkeys(faq["category"] for faq in FAQS):
    st.subheader(category)
    for faq in (item for item in FAQS if item["category"] == category):
        with st.expander(faq["question"]):
            st.write(faq["answer"])

footer()
