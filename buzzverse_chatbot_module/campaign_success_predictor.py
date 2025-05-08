

# ------------------------------------------------------------------------------
# Author: Bhavani Kumbam
# Title: AI/ML Engineer | Chatbot Developer | Data Science
# Description: This script is part of the BuzzVerse prototype.
# Created On: [APRIL 2025]
# 
# ⚠️ Proprietary Notice:
# This code is authored by Bhavani Kumbam for conceptual and prototype use
# within the BuzzVerse project. Redistribution, replication, or commercial 
# use without the author's consent is prohibited.
# 
# Contact: Bhavanik7575@gmail.com | LinkedIn: www.linkedin.com/in/bhavani-k-58403428a]
# ------------------------------------------------------------------------------


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# --- STEP 1: LOAD DATA ---
df = pd.read_excel("campaign_data.xlsx")

# --- STEP 2: ADD SUCCESS LABELS BASED ON BUSINESS RULE ---
df['Success'] = np.where(
    (df['CTR (%)'] >= 2.5) &
    (df['ROAS'] >= 3.0) &
    (df['Conversion Rate (%)'] >= 1.8) &
    (df['CPA ($)'] <= 16),
    1, 0
)

df['Campaign Result'] = df['Success'].map({1: 'SUCCESS ✅', 0: 'FAILURE ❌'})
# --- STEP 3: DESCRIPTIVE STATS ---
print("🔹 Campaign Result Count:")
print(df['Campaign Result'].value_counts())

print("\n🔹 Metrics for Successful Campaigns:")
print(df[df['Success'] == 1][['CTR (%)', 'ROAS', 'Conversion Rate (%)', 'CPA ($)', 'Engagement Rate (%)']].mean())

# --- STEP 4: DIAGNOSTIC COMPARISON ---
print("\n🔹 Success vs Failure Metric Averages:")
print(df.groupby('Success')[['CTR (%)', 'ROAS', 'CPA ($)', 'Engagement Rate (%)']].mean())

# --- STEP 5: CTA EFFECTIVENESS ---
print("\n🔹 Success Rate by CTA:")
print(df.groupby('CTA')['Success'].mean().sort_values(ascending=False))

# --- STEP 6: VISUALIZATION ---
plt.figure(figsize=(8, 5))
sns.boxplot(x='Success', y='ROAS', data=df)
plt.title("ROAS by Campaign Success")
plt.xlabel("Success (0=Fail, 1=Success)")
plt.ylabel("ROAS")
plt.tight_layout()
plt.savefig("roas_boxplot.png")
plt.close()

# --- STEP 7: PREDICTIVE MODELING ---
X = df.drop(columns=['Campaign Id', 'Campaign Name', 'Brand Name', 'Success', 'Campaign Result'])
y = df['Success']
X_encoded = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("\n✅ Random Forest Model Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

# --- STEP 8: SAVE UPDATED DATA ---
df.to_excel("campaign_data_with_results.xlsx", index=False)
print("📁 Exported: campaign_data_with_results.xlsx")
