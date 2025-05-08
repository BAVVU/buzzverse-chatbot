import pandas as pd

# Load the talent Excel file
df = pd.read_excel("talent_data.xlsx")

# Preview the first few rows
print("🎯 Talent Data Preview:")
print(df.head())

from sklearn.preprocessing import MinMaxScaler

# --- STEP 2: Compute Reach and Engagement Quotients ---

# Create a scaler
scaler = MinMaxScaler()

# Scale Reach and Engagement columns
df['Reach Quotient'] = scaler.fit_transform(df[['Followers']])
df['Engagement Quotient'] = scaler.fit_transform(df[['Engagement Rate (%)']])

# Show updated DataFrame
print("\n📊 Talent with Quotients:")
print(df[['Talent Name', 'Reach Quotient', 'Engagement Quotient']])

# --- STEP 3: Add Total Talent Score ---

# We'll average Reach, Engagement, and Authenticity
df['Total Talent Score'] = df[['Reach Quotient', 'Engagement Quotient', 'Authenticity Score']].mean(axis=1)

# Show final output
print("\n🏆 Final Talent Scores:")
print(df[['Talent Name', 'Reach Quotient', 'Engagement Quotient', 'Authenticity Score', 'Total Talent Score']])

# Save final output to Excel
df.to_excel("talent_scores.xlsx", index=False)
print("📁 Saved: talent_scores.xlsx")