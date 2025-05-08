import streamlit as st
import sys
import os
import re
import pandas as pd
import csv
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from bs4 import BeautifulSoup
import ollama
import importlib.util

# --- Load talent_ranker.py dynamically (for top actors logic) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
talent_ranker_path = os.path.join(current_dir, "talent_ranker.py")

spec = importlib.util.spec_from_file_location("talent_ranker", talent_ranker_path)
talent_ranker = importlib.util.module_from_spec(spec)
sys.modules["talent_ranker"] = talent_ranker
spec.loader.exec_module(talent_ranker)

rank_actors = talent_ranker.rank_actors

# --- Page Setup ---
st.set_page_config(page_title="BuzzBot Chat", layout="centered", page_icon="🧙")

# --- Custom CSS ---
st.markdown("""
<style>
    .chat-wrapper {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        height: calc(100vh - 160px);
        overflow-y: auto;
    }
    .stChatMessage { animation: fadeIn 0.3s ease forwards; }
    .chat-input {
        position: fixed; bottom: 20px; left: 50%;
        transform: translateX(-50%);
        width: 80%; max-width: 800px;
        background: white; padding: 12px;
        border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        z-index: 100;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def sanitize_text(text):
    return BeautifulSoup(str(text), "html.parser").get_text()

def ask_llama3(prompt):
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

@st.cache_resource
def get_retriever():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local("buzzbot_faiss_index", embedding_model, allow_dangerous_deserialization=True)
    return db.as_retriever(search_kwargs={"k": 20})

retriever = get_retriever()

# --- Chat Session ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Page Header ---
st.title("💬 BuzzBot Marketing Assistant")
st.caption("Powered by LLaMA 3 (Ollama) • Local FAISS Knowledge Base")

# --- Chat Display ---
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            st.caption(msg.get("timestamp", ""))

# --- Chat Input ---
user_input = st.chat_input("Ask anything about talents, brands, campaigns, or scores...")

# --- Chat Handling Functions ---
def log_chat(question, response):
    with open("chat_log.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), question, response])

def handle_user_query(prompt):
    clean_input = sanitize_text(prompt).lower()

    # --- Direct special rules first ---
    if any(kw in clean_input for kw in ["top actors", "top 3", "ranked actors", "best actors"]):
        df = rank_actors("data/actor_metrics_final_ready.csv")
        top3 = df.head(3)
        output = "🎬 **Top 3 Ranked Actors:**\n\n"
        for i, row in top3.iterrows():
            output += f"**{i+1}. {row['Actor']}** — Score: `{round(row['Final Score'], 2)}`\n"
        return output

    elif "best roi" in clean_input or "highest roi" in clean_input:
        df = pd.read_csv("data/actor_metrics_final_ready.csv")
        top_roi = df.sort_values(by="ROI", ascending=False).head(3)
        output = "💰 **Top 3 Actors by ROI:**\n\n"
        for i, row in top_roi.iterrows():
            output += f"**{i+1}. {row['Actor']}** — ROI: `{row['ROI']}`\n"
        return output

    elif "list all campaign" in clean_input or "campaign names" in clean_input:
        try:
            df = pd.read_excel("data/campaign_data.xlsx")
            if "Campaign Name" in df.columns:
                campaigns = df["Campaign Name"].dropna().unique().tolist()
                output = "📢 **Campaign Names:**\n\n"
                for i, name in enumerate(campaigns, start=1):
                    output += f"{i}. {name}\n"
                return output
            else:
                return "⚠️ Sorry, no 'Campaign Name' column found."
        except Exception as e:
            return f"⚠️ Error loading campaign names: {str(e)}"

    elif "list all talents" in clean_input or "talent names" in clean_input or "list talents" in clean_input:
        try:
            df = pd.read_excel("data/talent_data.xlsx")
            if "Talent Name" in df.columns:
                talents = df["Talent Name"].dropna().unique().tolist()
                output = "🎭 **Talent Names:**\n\n"
                for i, name in enumerate(talents, start=1):
                    output += f"{i}. {name}\n"
                return output
            else:
                return "⚠️ Sorry, no 'Talent Name' column found."
        except Exception as e:
            return f"⚠️ Error loading talents: {str(e)}"

    elif "list all brands" in clean_input or "brand names" in clean_input:
        try:
            df = pd.read_excel("data/brand_data.xlsx")
            if "Brand Name" in df.columns:
                brands = df["Brand Name"].dropna().unique().tolist()
                output = "🏢 **Brand Names:**\n\n"
                for i, name in enumerate(brands, start=1):
                    output += f"{i}. {name}\n"
                return output
            else:
                return "⚠️ Sorry, no 'Brand Name' column found."
        except Exception as e:
            return f"⚠️ Error loading brand names: {str(e)}"

    elif "nike" in clean_input and ("campaign" in clean_input or "run" in clean_input):
        return """Here are some notable Nike campaigns:

- **Just Do It** (1988–present): Iconic motivational campaign  
- **Run India** (2020): Encouraging running culture in India  
- **Dream Crazy** (2018): Featuring Colin Kaepernick  
- **You Can't Stop Us** (2020): Pandemic-era unity campaign  
- **Play New** (2021): Focused on trying new sports"""

    # --- FAISS fallback retrieval if no direct rule matched ---
    docs = retriever.get_relevant_documents(clean_input)

    if docs:
        combined_context = "\n".join(doc.page_content for doc in docs)
        final_prompt = f"""You are BuzzBot, an expert marketing assistant.
Use ONLY the below data to answer user's question politely:

{combined_context}

User Question: {prompt}
"""
        return ask_llama3(final_prompt)
    else:
        # Fallback answer if no relevant documents
        return ("Thanks for asking! Currently, I could not find direct matching data. "
                "However, feel free to ask anything else related to marketing, talent profiles, brand metrics, or campaigns. 🚀")

# --- Main Execution ---
if user_input:
    clean_input = sanitize_text(user_input)
    st.session_state.chat_history.append({
        "role": "user",
        "content": clean_input,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    try:
        bot_reply = handle_user_query(user_input)
        if not bot_reply.strip():
            bot_reply = "🤔 Hmm, I need a bit more details to help you better."

    except Exception as e:
        bot_reply = f"⚠️ Error occurred: {str(e)}"

    st.session_state.chat_history.append({
        "role": "bot",
        "content": bot_reply,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    log_chat(clean_input, bot_reply)
    st.rerun()
