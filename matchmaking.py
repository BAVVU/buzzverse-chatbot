import pandas as pd

# Load both datasets
talents = pd.read_excel("talent_scores.xlsx")
brands = pd.read_excel("brand_scores.xlsx")

# Keep needed columns
talents = talents[['Talent Name', 'Industry', 'Total Talent Score', 'Compensation']]
brands = brands[['Brand Name', 'Industry', 'Total Brand Score', 'Compensation Fairness']]

print("🎯 Talent Data Loaded:")
print(talents[['Talent Name', 'Industry', 'Total Talent Score']])

print("\n🏢 Brand Data Loaded:")
print(brands[['Brand Name', 'Industry', 'Total Brand Score']])

# --- STEP 2: Match Each Talent with Top 3 Brands (Industry + Score + Fairness) ---
top_matches = []

for _, t_row in talents.iterrows():
    talent_name = t_row['Talent Name']
    talent_industry = t_row['Industry']
    talent_score = t_row['Total Talent Score']
    talent_comp = t_row['Compensation']

    # Filter matching industry brands
    industry_brands = brands[brands['Industry'].str.lower() == talent_industry.lower()].copy()

    if industry_brands.empty:
        continue

    # Calculate match scores
    industry_brands['Score Difference'] = abs(industry_brands['Total Brand Score'] - talent_score)
    industry_brands['Match Score'] = 1 - industry_brands['Score Difference']
    industry_brands['Fairness Match'] = industry_brands['Compensation Fairness'].apply(lambda x: '✓' if x >= 0.8 else '✗')

    # Reason tag generation
    def reason(row):
        reasons = []
        if row['Fairness Match'] == '✓':
            reasons.append("✓ Fair Pay")
        if row['Score Difference'] <= 0.1:
            reasons.append("✓ High Score Match")
        elif row['Score Difference'] <= 0.2:
            reasons.append("⚠ Acceptable Match")
        else:
            reasons.append("✗ Weak Match")
        return ", ".join(reasons)

    industry_brands['Reason'] = industry_brands.apply(reason, axis=1)

    # Sort by match score and select top 3
    top_3 = industry_brands.sort_values(by='Match Score', ascending=False).head(3)

    for _, b_row in top_3.iterrows():
        top_matches.append({
            'Talent Name': talent_name,
            'Brand Name': b_row['Brand Name'],
            'Industry': talent_industry,
            'Talent Score': round(talent_score, 3),
            'Brand Score': round(b_row['Total Brand Score'], 3),
            'Match Score': round(b_row['Match Score'], 3),
            'Fairness Match': b_row['Fairness Match'],
            'Reason': b_row['Reason']
        })

# Convert to DataFrame and display
match_df = pd.DataFrame(top_matches)

print("\n🤝 Top 3 Matches Per Talent:")
print(match_df)

# Save output to Excel
match_df.to_excel("top_3_matches_per_talent.xlsx", index=False)
print("\n📁 Saved: top_3_matches_per_talent.xlsx")