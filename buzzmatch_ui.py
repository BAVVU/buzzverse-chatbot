import streamlit as st
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import pandas as pd
from datetime import datetime
import io
import requests
import re
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "watchdog"

from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from transformers import pipeline





st.set_page_config(page_title="BuzzMatch | BuzzVerse Talent Portal", layout="wide")
st.title("🎯 BuzzMatch Talent Platform (Powered by BuzzVerse)")

# --- Language Switcher ---
st.sidebar.header("🌍 Language")
language = st.sidebar.selectbox("Choose Language", ["English", "Spanish", "French", "Hindi"])

# --- Tabs ---
tabs = st.tabs([
    "Trending Brands", "Suggested Matches", "Deal Room", "Campaigns", "Settings",
    "Existing User Dashboard", "ROI Calculator", "Support", "Signup/Login", "Manager Profile", "💬 BuzzBot"
])

# --- Tab: Trending Brands ---
with tabs[0]:
    st.subheader("🔥 Trending Brands")
    brands = ["Nike", "Apple", "Netflix", "Adidas", "Tesla"]
    for b in brands:
        st.markdown(f"- ⭐ {b}")
    st.text_input("Search Brand")

# --- Tab: Suggested Matches ---
with tabs[1]:
    st.subheader("💡 Suggested Matches")
    st.info("Top 3 recommended brand matches based on your profile")
    st.dataframe(pd.DataFrame({
        "Brand": ["Apple", "Tesla", "Nike"],
        "Match Score": [0.91, 0.88, 0.84],
        "Reason": ["Tech Fit", "Innovation Alignment", "Lifestyle Influence"]
    }))

# --- Tab: Deal Room ---
with tabs[2]:
    st.subheader("📅 Deal Room")
    st.date_input("Schedule Meeting")
    st.text_input("Meeting Link")
    st.text_area("Agenda")
    st.button("Send Invite")

# --- Tab: Campaigns ---
with tabs[3]:
    st.subheader("📢 Campaign Dashboard")
    campaigns = ["Summer Promo", "Wellness Week", "Tech Launch"]
    if campaigns:
        st.table(pd.DataFrame({"Campaign": campaigns, "Status": ["Running", "Upcoming", "Closed"]}))
    else:
        st.info("No active campaigns yet")
    st.text_input("Instagram Handle")
    st.selectbox("Campaign Intent", ["Browsing", "Urgent", "Future"])
    st.slider("Preferred Response Time (hrs)", 1, 72, 24)

# --- Tab: Settings ---
with tabs[4]:
    st.subheader("⚙️ Settings")
    st.text_input("Username", key="settings_username")
    st.text_input("Change Password", type="password", key="settings_pwd")
    st.radio("Account Status", ["Active", "Inactive", "Dormant"], key="settings_status")
    st.selectbox("Subscription Plan", ["Free", "Pro", "Enterprise"], key="settings_plan")
    st.button("Logout")

# --- Tab: Existing User Dashboard ---
with tabs[5]:
    st.subheader("📊 Dashboard")
    st.metric("Active Campaigns", 4)
    st.metric("Monthly ROI", "345%")
    st.metric("Engagement Rate", "6.2%")

# --- Tab: ROI Calculator ---
with tabs[6]:
    st.subheader("📈 ROI Calculator")
    fee = st.number_input("Brand Endorsement Fee ($)", key="roi_fee")
    marketing = st.number_input("Marketing Spend ($)", key="roi_marketing")
    hidden = st.number_input("Other Hidden Costs ($)", key="roi_hidden")
    revenue = st.number_input("Expected Revenue ($)", key="roi_revenue")
    if fee + marketing + hidden > 0:
        roi = ((revenue - (fee + marketing + hidden)) / (fee + marketing + hidden)) * 100
        st.metric("Estimated ROI", f"{roi:.2f}%")
        roi_data = pd.DataFrame({
            "Metric": ["Fee", "Marketing", "Hidden", "Revenue", "ROI %"],
            "Value": [fee, marketing, hidden, revenue, f"{roi:.2f}%"]
        })
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            roi_data.to_excel(writer, index=False, sheet_name="ROI")
            writer.save()
            st.download_button("Download ROI Report", buffer.getvalue(), file_name="roi_report.xlsx")

# --- Tab: Support ---
with tabs[7]:
    st.subheader("🆘 Support Center")
    st.markdown("*📞 Call Us:* 1-800-BUZZ-HELP")
    st.text_input("Ask a Question", key="support_q")
    st.button("Submit Query", key="support_submit")
    st.checkbox("Connect me to an agent", key="support_agent")

# --- Tab: Signup/Login ---
with tabs[8]:
    st.subheader("📝 Signup / Login Portal")
    auth_tabs = st.tabs(["Signup", "Login", "Recover"])

    with auth_tabs[0]:
        st.markdown("### ✍️ Signup")
        st.selectbox("Signup With", ["Email", "Google", "Microsoft SSO", "Instagram", "Twitter", "IMDB", "LinkedIn", "DigiLocker"])
        st.text_input("Username", key="signup_username")
        st.text_input("Email", key="signup_email")
        st.text_input("Phone", key="signup_phone")
        st.text_input("Password", type="password", key="signup_password")
        st.text_input("Confirm Password", type="password", key="signup_confirm")
        st.text_input("OTP - Email", key="signup_otp_email")
        st.text_input("OTP - Phone", key="signup_otp_phone")
        st.button("✅ Verify and Create Account", key="signup_submit")

    with auth_tabs[1]:
        st.markdown("### 🔐 Login")
        st.selectbox("Login With", ["Email", "Google", "Microsoft SSO", "Instagram", "Twitter", "IMDB", "LinkedIn", "DigiLocker"])
        st.text_input("Username / Email", key="login_user")
        st.text_input("Password", type="password", key="login_password")
        st.button("🔓 Login", key="login_submit")

    with auth_tabs[2]:
        st.markdown("### 🔁 Forgot Access")
        recover_type = st.radio("Recovery Option", ["Forgot Password", "Forgot Username"], key="recover_type")
        if recover_type == "Forgot Password":
            st.text_input("Registered Email / Phone", key="recover_email")
            st.text_input("OTP", key="recover_otp")
            st.text_input("New Password", type="password", key="recover_new")
            st.text_input("Confirm Password", type="password", key="recover_confirm")
            st.button("🔑 Reset Password", key="reset_pwd")
        else:
            st.text_input("Registered Email", key="recover_username_email")
            st.button("📬 Send Username", key="send_username")

# --- Tab: Manager Profile ---
with tabs[9]:
    st.subheader("🧑‍💼 Talent Manager Profile")
    st.text_input("Manager Name", key="mgr_name")
    st.text_input("Company Name", key="mgr_company")
    st.text_input("Primary Contact", key="mgr_primary")
    st.text_input("Secondary Contact", key="mgr_secondary")
    st.text_input("Email ID", key="mgr_email")
    st.text_input("City", key="mgr_city")
    st.text_input("Manager Since (current talent)", key="mgr_since")
    st.text_input("Website", key="mgr_website")
    st.multiselect("Categories Managed", ["Sports", "Celeb", "Other"], key="mgr_categories")
    st.text_input("Brand Signed", key="mgr_brand")
    st.file_uploader("Upload Manager Image", type=["png", "jpg"], key="mgr_image")
    st.file_uploader("Upload Directory (Excel)", key="mgr_directory")
    st.text_input("All Attributes", key="mgr_attributes")
    st.date_input("Book Calendar", key="mgr_calendar")
    st.checkbox("Notify on Brand Interest", key="mgr_notify")
    st.checkbox("Bookmark Campaigns", key="mgr_bookmark")
    st.checkbox("Connect on Behalf", key="mgr_connect")

# --- Tab: BuzzBot Chat ---
# --- Tab: BuzzBot Chat (Display Only) ---
with tabs[10]:
    st.subheader("🤖 BuzzBot Live Chat")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✅ Chat input MUST be outside of tab container
user_input = st.chat_input("Ask me something like: 'ROAS 3.2, CTR 2.4...'")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    def extract_metrics(text):
        ctr = re.search(r"ctr[\s:]*([\d.]+)", text, re.IGNORECASE)
        roas = re.search(r"roas[\s:]*([\d.]+)", text, re.IGNORECASE)
        cpa = re.search(r"cpa[\s:]*([\d.]+)", text, re.IGNORECASE)
        conv = re.search(r"(conversion rate|conv)[\s:]*([\d.]+)", text, re.IGNORECASE)
        return {
            "ctr": float(ctr.group(1)) if ctr else None,
            "roas": float(roas.group(1)) if roas else None,
            "cpa": float(cpa.group(1)) if cpa else None,
            "conv_rate": float(conv.group(2)) if conv else None
        }

    metrics = extract_metrics(user_input)
    if all(v is not None for v in metrics.values()):
        try:
            response = requests.post("http://localhost:8000/predict", json=metrics)
            result = response.json()
            prediction = "✅ SUCCESS" if result['success'] else "❌ FAILURE"
        except Exception as e:
            prediction = f"⚠️ Error: {e}"
    else:
        prediction = "💡 I need CTR, ROAS, CPA, and Conversion Rate to make a prediction."

    st.session_state.chat_history.append({"role": "bot", "content": prediction})
    with st.chat_message("bot"):
        st.markdown(prediction)