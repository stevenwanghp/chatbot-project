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
st.write(
    "Official resources and support services for people navigating divorce through "
    "the Syariah Court in Singapore."
)
st.info("General information only — this page is not legal advice.")

useful_links = [
    {
        "title": "Syariah Court - Divorce Overview",
        "url": "https://syariahcourt.gov.sg/Divorce/Overview",
        "description": "Official step-by-step overview of the divorce process, from counselling to post-divorce.",
        "best_for": "Thinking of divorce",
    },
    {
        "title": "Marriage Counselling Programme (MCP)",
        "url": "https://syariahcourt.gov.sg/Divorce/Process-Pre-Divorce/Marriage-Counselling-Programme",
        "description": "Compulsory first step: who must attend, exemptions, the Parenting Programme and MCP agencies.",
        "best_for": "Thinking of divorce",
    },
    {
        "title": "SYC Portal (E-Services)",
        "url": "https://eservices.syariahcourt.gov.sg",
        "description": "Register for MCP, file documents, pay fees, check appointments and download your divorce certificate.",
        "best_for": "Going through divorce",
    },
    {
        "title": "Syariah Court - Divorce Fees",
        "url": "https://syariahcourt.gov.sg/Divorce/Fees",
        "description": "Full list of court fees and estimated maximum costs for each stage.",
        "best_for": "Going through divorce",
    },
    {
        "title": "Syariah Court - Forms",
        "url": "https://syariahcourt.gov.sg/Resources/Forms",
        "description": "Templates for parenting plans, matrimonial property plans, affidavits and other forms.",
        "best_for": "Going through divorce",
    },
    {
        "title": "eBantu - Form-Filling Guidance Tool (Legal Aid Bureau)",
        "url": "https://lab.mlaw.gov.sg/resources/ebantu-syariah-court-originating-documents-guidance-tool/",
        "description": "Free Ministry of Law tool explaining how to complete the Case Statement and Memorandum of Defence.",
        "best_for": "Going through divorce",
    },
    {
        "title": "Legal Aid Bureau",
        "url": "https://lab.mlaw.gov.sg/",
        "description": "Government legal aid for people who meet the means and merits tests.",
        "best_for": "Anyone needing legal help",
    },
    {
        "title": "Pro Bono SG - Community Legal Clinics",
        "url": "https://www.probono.sg/",
        "description": "Free basic legal advice from volunteer lawyers.",
        "best_for": "Anyone needing legal help",
    },
    {
        "title": "Syariah Court - Support Programmes",
        "url": "https://syariahcourt.gov.sg/Divorce/Support-Programmes",
        "description": "Free counselling at FAM centres, Children-in-Between workshops, supervised visitation and online counselling.",
        "best_for": "Helping someone / families with children",
    },
    {
        "title": "CPF - Division of CPF Assets in a Divorce",
        "url": "https://www.cpf.gov.sg/member/account-services/undergoing-a-divorce/division-of-cpf-assets",
        "description": "How CPF savings and CPF-funded property are divided after a divorce order.",
        "best_for": "Going through / after divorce",
    },
]

for index, link in enumerate(useful_links, start=1):
    st.markdown(f"### {index}. [{link['title']}]({link['url']})")
    st.write(link["description"])
    st.caption(f"Best for: {link['best_for']}")
