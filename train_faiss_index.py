import os
import pandas as pd
import re
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# --- Define your local data folder ---
data_dir = "data"  # Local folder where your CSV and XLSX files are

# --- Metadata (Optional: For future use) ---
dataset_metadata = {
    "talents": set(),
    "campaigns": set(),
    "brands": set(),
    "metrics": set()
}

# --- Text sanitizer (remove unwanted HTML etc) ---
def sanitize_text(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()

# --- Process a single row cleanly into a Document object ---
def process_row(file_name: str, row: pd.Series, df: pd.DataFrame):
    content_parts = []
    file_lower = file_name.lower()

    # Label Type from file name
    if "talent" in file_lower:
        content_parts.append("Type: Talent")
    elif "campaign" in file_lower:
        content_parts.append("Type: Campaign")
    elif "brand" in file_lower:
        content_parts.append("Type: Brand")
    elif "actor" in file_lower:
        content_parts.append("Type: Actor")
    else:
        content_parts.append("Type: Other")

    # Process all columns nicely
    for col in df.columns:
        val = row[col]
        if pd.notna(val) and str(val).strip() != "":
            clean_val = sanitize_text(str(val))
            content_parts.append(f"{col}: {clean_val}")

            # Optional: Track important columns
            if any(keyword in col.lower() for keyword in ["metric", "score", "rate", "ctr", "roas", "conversion", "cpa", "engagement", "bounce", "follower"]):
                dataset_metadata["metrics"].add(col)

    return Document(
        page_content=" | ".join(content_parts),
        metadata={"source": file_name}
    )

# --- Load and process all datasets ---
documents = []
files_to_process = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if (f.endswith(".csv") or f.endswith(".xlsx")) and not f.startswith("~$")]

for file_path in files_to_process:
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        df = df.fillna("")
        for _, row in df.iterrows():
            doc = process_row(os.path.basename(file_path), row, df)
            documents.append(doc)

    except Exception as e:
        print(f"⚠️ Skipping file {file_path} due to error: {e}")

# --- Generate and save FAISS index cleanly ---
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
faiss_index = FAISS.from_documents(documents, embedding_model)
faiss_index.save_local("buzzbot_faiss_index")  # Save locally for your chatbot to use

print(f"✅ Successfully indexed {len(documents)} rows from {len(files_to_process)} files!")