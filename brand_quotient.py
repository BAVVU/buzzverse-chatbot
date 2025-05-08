import pandas as pd

# Load brand data
df = pd.read_excel("brand_data.xlsx")

print("🏢 Brand Data Preview:")
print(df.head())

from sklearn.preprocessing import MinMaxScaler

# --- STEP 2: Calculate Reach + Engagement Quotients ---
df['Total Reach'] = df['Paid Reach'] + df['Organic Reach']

scaler = MinMaxScaler()

# Normalize Total Reach
df['Reach Quotient'] = scaler.fit_transform(df[['Total Reach']])

# Normalize Audience Engagement if needed
df['Engagement Quotient'] = scaler.fit_transform(df[['Audience Engagement']])

# Show results
print("\n📊 Brand Quotients:")
print(df[['Brand Name', 'Reach Quotient', 'Engagement Quotient']])

# --- STEP 3: Total Brand Score (average of all key quotients) ---
df['Total Brand Score'] = df[[
    'Reach Quotient',
    'Engagement Quotient',
    'Compensation Fairness',
    'Reputation Score',
    'Growth Potential',
    'Creative Freedom'
]].mean(axis=1)

# Sort and display top brands
print("\n🏆 Final Brand Scores:")
print(df[['Brand Name', 'Total Brand Score']].sort_values(by='Total Brand Score', ascending=False))

# --- STEP 4: Save brand scores to Excel ---
df.to_excel("brand_scores.xlsx", index=False)
print("📁 Saved: brand_scores.xlsx")