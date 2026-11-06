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
            "file for divorce. You can choose up to three of the five court-appointed agencies and "
            "book a session with one that has an available slot: AMP Singapore, APKIM Resources, "
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
        "question": "We have children. Is there anything extra we must do?",
        "answer": (
            "Yes. If you proceed with the divorce and have at least one child below 21, you and "
            "your spouse will go through a Parenting Programme with your counsellor. If you agree "
            "on the arrangements, you both sign the Agreed Parenting Plan before filing, and your "
            "spouse must affirm their signature before a Commissioner for Oaths. If you do not "
            "agree, the person filing (the Plaintiff) submits a Proposed Parenting Plan instead."
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
        "question": "What documents do I need to file?",
        "answer": (
            "1) The Originating Summons, issued by the Court.\n\n"
            "2) A Case Statement, an e-form on the SYC Portal with supporting documents.\n\n"
            "3) A Parenting Plan (agreed or proposed) if you have a child under 21.\n\n"
            "4) A Matrimonial Property Plan (agreed or proposed) plus Particulars of Housing "
            "Arrangement if an HDB flat is a matrimonial asset.\n\n"
            "The original marriage certificate must also be surrendered to the Court. "
            "The Ministry of Law's free eBantu tool explains how to fill in the Case Statement "
            "and Memorandum of Defence."
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
    {
        "category": "Process",
        "question": "When will I get my divorce certificate?",
        "answer": (
            "It depends on the type of divorce. For talak where the wife's iddah has not expired on "
            "the date of the Decree, it is available 3 months and 10 days after the Decree. Where "
            "the iddah has expired, and for talak ba'in and fasakh, it is available within 7 working "
            "days. Download it from the SYC Portal under 'Court File': under 'Court Orders' for "
            "divorces registered before 18 November 2022, or 'Court Documents' for those registered "
            "after 1 December 2022. If you have a lawyer, it is made available to your lawyer."
        ),
    },
    # --- Fees ---
    {
        "category": "Fees",
        "question": "How much does a divorce at the Syariah Court cost?",
        "answer": (
            "The Court's estimated maximum fees are about $87 for filing the Originating Summons "
            "(Plaintiff) and about $42 for filing a Memorandum of Defence (Defendant). Registration "
            "of the divorce is $100, and each filed document is $12. If hakam are appointed, each "
            "party pays $150 plus $22 for the Order of Court. Fees are paid on the SYC Portal by "
            "PayNow or eNETS/credit card. Lawyer's fees are separate. If you cannot afford a "
            "lawyer, check whether you qualify for help from the Legal Aid Bureau."
        ),
    },
    # --- Reconciliation ---
    {
        "category": "Reconciliation",
        "question": "My husband pronounced talak outside court but we want to reconcile. What should we do?",
        "answer": (
            "Both of you must attend in person at the Syariah Court within 7 days of the talak "
            "pronouncement. The Court will decide whether the out-of-court divorce is valid. After "
            "the decree or order is issued, both of you attend in person at the Registry of Muslim "
            "Marriages (ROMM) to register the revocation of the divorce (rujuk)."
        ),
    },
    {
        "category": "Reconciliation",
        "question": "Can I stop the divorce process if we decide to work things out?",
        "answer": (
            "Yes. If you decide not to go ahead with the divorce, you can close your case at the "
            "MCP stage. If a consent order has already been made and you wish to reconcile (rujuk), "
            "you can apply to the Court to rescind it."
        ),
    },
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
    # --- After divorce ---
    {
        "category": "After Divorce",
        "question": "My ex-spouse is not following the court order. What can I do?",
        "answer": (
            "Breaches of Syariah Court orders are enforced at the Family Justice Courts. For "
            "maintenance, nafkah iddah and mutaah, you apply under section 53(1) of the "
            "Administration of Muslim Law Act. For orders on custody and access, emas kahwin and "
            "marriage expenses, or the division of property, you can file a Magistrate's Complaint "
            "under section 53(2) in person at the Family Registry (no fee). If the order allows the "
            "Court to sign property documents for a party who refuses, file a Praecipe (Request) "
            "on the SYC Portal. Seek legal advice before taking these steps."
        ),
    },
    {
        "category": "After Divorce",
        "question": "Can a court order be changed later?",
        "answer": (
            "Yes, if there is a material change in circumstances. Applications to vary a Syariah "
            "Court order must be made at the Syariah Court, not the Family Justice Courts. File a "
            "summons with a supporting affidavit on the SYC Portal, then serve it on your ex-spouse "
            "by personal service, registered post or substituted service. Service through the "
            "portal is not allowed. The Court will then fix a mediation or Pre-Trial Conference. "
            "Fees are estimated at up to about $69."
        ),
    },
]

page_header(
    "Frequently Asked Questions",
    "Common questions about the Syariah Court divorce process, from eligibility to life after divorce.",
    "❓",
)
st.info(FAQ_DISCLAIMER)

for category in dict.fromkeys(faq["category"] for faq in FAQS):
    st.subheader(category)
    for faq in (item for item in FAQS if item["category"] == category):
        with st.expander(faq["question"]):
            st.markdown(faq["answer"])

footer()
