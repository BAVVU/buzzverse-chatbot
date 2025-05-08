# 🤖 BuzzVerse Chatbot – AI/ML Talent Matching Assistant

This repository contains the **core chatbot logic and AI components** developed as part of the **BuzzVerse prototype**. The goal is to build a fully offline, domain-specific, and production-ready conversational assistant that matches talents to brands, predicts campaign success, and offers dynamic insights.

## 📌 Features

- **Conversational AI** powered by LLaMA 3 via Ollama
- **Offline retrieval** using FAISS and HuggingFace sentence transformers
- **Custom dataset ingestion** and training (actors, campaigns, brands, talents)
- **Actor ranking engine** with dynamic weighting (Equal, PCA, Regression, Manual)
- **Campaign success prediction** using logistic regression
- **RAG-based architecture** to enhance accuracy and context

## 🛠️ Tech Stack

- **Python 3.11**
- **Streamlit** (for chatbot UI prototype)
- **FAISS** – for vector search
- **Hugging Face Transformers** – for embeddings
- **LangChain** – for chaining logic and retrieval
- **Pandas, Scikit-learn, NumPy** – for data preprocessing and ML
- **Custom scripts** for data parsing, ranking, embedding, and evaluation

## 📂 Main Files

- `chatbot_widget.py` – Chatbot interface logic
- `train_faiss_index.py` – Indexing datasets into FAISS
- `rank_actors_full.py` – Actor scoring based on multiple dynamic metrics
- `campaign_success_predictor.py` – Logistic regression-based outcome prediction
- `buzzmatch_ui.py` – Streamlit multi-tab UI (for internal preview)

## 👤 Author

**Bhavani Kumbam**  
AI/ML Engineer | Data Scientist | Chatbot Developer  
📧 bhavanik7575@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/bhavani-k-58403428a)

---

## 🚫 Legal

This project is under development.  
All code is authored by Bhavani Kumbam. Redistribution or commercial use is prohibited without permission.