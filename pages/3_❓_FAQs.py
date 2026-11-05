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

"""
FAQ page content - Syariah Court divorce chatbot site.
Source: syariahcourt.gov.sg (checked 5 Nov 2026) plus linked government sites.
General information only - not legal advice.
"""

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
        "question": "Who can apply for divorce at the Syariah Court?",
        "answer": (
            "You can apply if both you and your spouse are Muslims, or if you were married "
            "under Muslim law. Other couples file at the Family Justice Courts."
        ),
    },
    {
        "category": "Eligibility",
        "question": "Is there a residency requirement?",
        "answer": (
            "Yes. At least one of you must be a Singapore citizen, OR have lived in Singapore "
            "for at least 3 continuous years before applying, OR be domiciled in Singapore "
            "(treat Singapore as your permanent home). If neither of you is a citizen, you must "
            "show proof of residence for the 3 years before applying, e.g. an employment pass, "
            "employment agreement or tenancy agreement."
        ),
    },
    # --- Before filing ---
    {
        "category": "Before Filing",
        "question": "What is the first step if I want a divorce?",
        "answer": (
            "Register for the compulsory Marriage Counselling Programme (MCP) online on the "
            "SYC Portal (eservices.syariahcourt.gov.sg). You must attend the MCP before you can "
            "file for divorce. Once your registration is accepted, you book a session with one of "
            "the court-appointed agencies: AMP Singapore, APKIM Resources, Darul Arqam, "
            "Persatuan Pemudi Islam Singapura or Reach Community Services."
        ),
    },
    {
        "category": "Before Filing",
        "question": "Can I be exempted from the Marriage Counselling Programme?",
        "answer": (
            "Possibly, if a critical or terminal illness, or a physical disability or infirmity, "
            "makes attending impractical or impossible. Apply in the 'Exemption from Counselling' "
            "section of your registration and attach proof, such as a doctor's letter dated no "
            "more than one month before you submit."
        ),
    },
    {
        "category": "Before Filing",
        "question": "We have children. Is there anything extra we must do?",
        "answer": (
            "Yes. If you have at least one child under 21, you and your spouse will go through a "
            "Parenting Programme with your counsellor. It covers co-parenting and care "
            "arrangements after divorce. If you agree on the arrangements, you both sign an Agreed "
            "Parenting Plan. If not, the person filing submits a Proposed Parenting Plan."
        ),
    },
    {
        "category": "Before Filing",
        "question": "Can I get advice on Islamic law on marriage and divorce before deciding?",
        "answer": (
            "Yes. During the MCP stage you can request a free session with a Resource Person, "
            "a registered Asatizah under MUIS' Asatizah Recognition Scheme, to clarify Muslim law "
            "on marriage and divorce."
        ),
    },
    # --- Filing & proceedings ---
    {
        "category": "Process",
        "question": "When must I file for divorce after counselling?",
        "answer": (
            "You must file the divorce application (the Originating Summons) within 6 months of "
            "the date on the 'Pre-OS Email' confirming your MCP outcome. You file online through "
            "the SYC Portal under Divorce E-services. The person filing is the Plaintiff and the "
            "spouse is the Defendant."
        ),
    },
    {
        "category": "Process",
        "question": "What documents do I need to file?",
        "answer": (
            "1) The Originating Summons, issued by the Court. "
            "2) A Case Statement, an e-form on the portal with supporting documents. "
            "3) A Parenting Plan (agreed or proposed) if you have children under 21. "
            "4) A Matrimonial Property Plan (agreed or proposed) plus Particulars of Housing "
            "Arrangement if an HDB flat is a matrimonial asset. "
            "The original marriage certificate must also be surrendered to the Court. "
            "The Ministry of Law's free eBantu tool explains how to fill in the forms."
        ),
    },
    {
        "category": "Process",
        "question": "How do I serve the divorce papers on my spouse?",
        "answer": (
            "You must serve the Service Bundle within 12 months of your filing being accepted. "
            "Options: through the SYC Portal (only if you gave your spouse's valid email), personal "
            "service by a solicitor or solicitor's clerk, or registered post with a signed "
            "Acknowledgement of Service returned. If your spouse cannot be found, apply to the "
            "Court for substituted service. Do not carry it out until the Court approves it."
        ),
    },
    {
        "category": "Process",
        "question": "I have been served divorce papers. What do I do?",
        "answer": (
            "Acknowledge receipt and file a Memorandum of Defence on the SYC Portal within 21 days "
            "of being served. In it you say whether you agree to the divorce and the proposed "
            "arrangements, or give your own proposals."
        ),
    },
    {
        "category": "Process",
        "question": "What happens at mediation?",
        "answer": (
            "A mediator meets both of you to see whether you can agree on the divorce and the "
            "ancillary matters (nafkah iddah, mutaah, children and property). Each session lasts "
            "about 60 minutes, and more sessions can be scheduled. If you have a lawyer, they must "
            "attend with you. If you reach full agreement and all documents are in order, a "
            "President of the Court may hear and decide the case on the same day."
        ),
    },
    {
        "category": "Process",
        "question": "What if we cannot agree?",
        "answer": (
            "The case goes to a Pre-Trial Conference and then a hearing, where a President of the "
            "Court decides based on affidavit evidence. In contested divorces, the Court may "
            "appoint hakam (marital conciliators), one for each party, to try to reconcile you or, "
            "if that fails, to help you reach an amicable divorce. Hakam can pronounce a divorce "
            "if they jointly agree that you should divorce."
        ),
    },
    {
        "category": "Process",
        "question": "What are 'ancillary matters'?",
        "answer": (
            "These are the issues settled alongside the divorce: custody, care and control of, and "
            "access to children; nafkah iddah (maintenance for the wife during the waiting period); "
            "mutaah (a consolatory gift to the wife); hantaran belanja and emas kahwin (wedding "
            "gifts and dowry); and division of matrimonial property, including HDB flats and CPF "
            "savings. In custody disputes, the Court may interview a child aged 7 to 21 or order a "
            "free Custody Evaluation Report."
        ),
    },
    {
        "category": "Process",
        "question": "When will I get my divorce certificate?",
        "answer": (
            "It depends on the type of divorce. For talak where the iddah has not expired at the "
            "Decree, the certificate is issued 3 months and 10 days after the Decree. For talak "
            "where the iddah has expired, talak ba'in and fasakh, it is usually issued within "
            "7 working days. Download it from the SYC Portal under 'Court File'."
        ),
    },
    # --- Fees ---
    {
        "category": "Fees",
        "question": "How much does a divorce at the Syariah Court cost?",
        "answer": (
            "Court fees are modest. The estimated maximum for filing the Originating Summons is "
            "about $87 (Plaintiff). Filing a Memorandum of Defence is about $42 (Defendant). "
            "Registration of the divorce is $100, and each filed document is $12. If hakam are "
            "appointed, each party pays $150 plus $22 for the Order of Court. Fees are paid on the "
            "SYC Portal by PayNow or eNETS/credit card. Lawyer's fees are separate. If you cannot "
            "afford a lawyer, check whether you qualify for the Legal Aid Bureau."
        ),
    },
    # --- Reconciliation ---
    {
        "category": "Reconciliation",
        "question": "My husband pronounced talak outside court but we want to reconcile. What should we do?",
        "answer": (
            "Both of you must attend in person at the Syariah Court within 7 days of the talak "
            "pronouncement. The Court will decide whether the talak is valid. After the decree or "
            "order is issued, both of you attend in person at the Registry of Muslim Marriages "
            "(ROMM) to register the revocation of the divorce (rujuk)."
        ),
    },
    {
        "category": "Reconciliation",
        "question": "Can I stop the divorce process if we decide to work things out?",
        "answer": (
            "Yes. If you decide not to go ahead after counselling, you can close your case at the "
            "MCP stage. If a consent order has already been made and you wish to reconcile (rujuk), "
            "you can apply to the Court to rescind it."
        ),
    },
    # --- Appeals ---
    {
        "category": "Appeals",
        "question": "Can I appeal a decision?",
        "answer": (
            "Yes. Against a decision of the Syariah Court (a President's order), file a notice of "
            "appeal with the Appeal Board at MUIS (Singapore Islamic Hub, 273 Braddell Road; "
            "Tel 6359 1199) within 30 days. Against a Registrar's direction or order, file Form 52 "
            "on the SYC Portal within 14 days, which is heard by a President of the Court. Either "
            "way, serve a copy on the other party within 3 days of filing. Get legal advice on "
            "whether your appeal has merit."
        ),
    },
    # --- After divorce ---
    {
        "category": "After Divorce",
        "question": "My ex-spouse is not following the court order. What can I do?",
        "answer": (
            "Syariah Court orders on nafkah iddah, mutaah, and custody, care and control or access "
            "are enforced at the Family Justice Courts. For breaches you can file a Magistrate's "
            "Complaint under section 53 of the Administration of Muslim Law Act. If the order "
            "allows the Court to sign property documents for a party who refuses, file a Praecipe "
            "(Request) on the SYC Portal."
        ),
    },
    {
        "category": "After Divorce",
        "question": "Can a court order be changed later?",
        "answer": (
            "Yes, if there is a material change in circumstances. File a summons with a supporting "
            "affidavit on the SYC Portal, then serve it on your ex-spouse by personal service, "
            "registered post or substituted service. Service through the portal is not allowed. "
            "The Court will then fix a mediation or Pre-Trial Conference. Fees are estimated at "
            "up to about $69."
        ),
    },
]

st.title("❓ Frequently Asked Questions")
st.caption(DISCLAIMER)

for category in dict.fromkeys(faq["category"] for faq in FAQS):
    st.subheader(category)
    for faq in (item for item in FAQS if item["category"] == category):
        with st.expander(faq["question"]):
            st.write(faq["answer"])
