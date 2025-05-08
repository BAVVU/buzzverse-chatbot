import pandas as pd
from langchain.schema import Document
import os

# Data files
xlsx_files = [
    "brand_data.xlsx", "brand_scores.xlsx", "talent_brand_matches.xlsx",
    "talent_data.xlsx", "talent_scores.xlsx", "campaign_data.xlsx",
    "campaign_data_with_results.xlsx", "top_3_matches_per_talent.xlsx"
]
csv_files = ["actor_metrics_final_ready.csv"]

documents = []

# Load Excel files
for file in xlsx_files:
    df = pd.read_excel(os.path.join("data", file)).fillna("")
    for _, row in df.iterrows():
        row_text = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        documents.append(Document(page_content=row_text, metadata={"source": file}))

# Load CSV file
for file in csv_files:
    df = pd.read_csv(os.path.join("data", file)).fillna("")
    for _, row in df.iterrows():
        row_text = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        documents.append(Document(page_content=row_text, metadata={"source": file}))

print(f"Loaded {len(documents)} total records.")