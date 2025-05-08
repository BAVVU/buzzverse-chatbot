import pandas as pd
import random

# List of Actors
actors = [f"Actor {i}" for i in range(1, 10)]

# Create dictionary
structured_data = {"Actor": actors}

# Hardcoded realistic values
structured_data["Domestic and Global Gross"] = [120000, 15000, 400000, 6100000, 5200000, 300000, 525000, 1250000, 300000]
structured_data["Opening Weekend Gross"] = [100, 200, 600, 500, 1400, 50, 800, 900, 700]
structured_data["ROI"] = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
structured_data["Awards and Nominations"] = [6, 4, 8, 8, 7, 2, 21, 44, 7]
structured_data["Reviews"] = [4, 5, 2, 8, 1, 4, 7, 5, 6]
structured_data["Festival Recognition"] = [1, 1, 4, 1, 4, 1, 1, 0, 4]
structured_data["Social Media Followers"] = [1000000, 1000000, 4000000, 1000000, 5000000, 1000000, 500000, 9000000, 7000000]

# Random realistic values
random_metrics = {
    "Google Trends": lambda: random.randint(10, 100),
    "Fan Following": lambda: random.randint(10000, 1000000),
    "Director Collaborations": lambda: random.randint(1, 10),
    "Role Diversity": lambda: random.choice(["Basic", "Moderate", "Diverse"]),
    "Franchise Appearances": lambda: random.randint(0, 5),
    "Draw Factor": lambda: round(random.uniform(1.0, 10.0), 1),
    "Screen Presence": lambda: random.choice(["Low", "Moderate", "High"]),
    "Cultural Impact": lambda: random.choice(["None", "Some", "Significant"]),
    "Viewership Numbers": lambda: random.randint(100000, 5000000),
    "Subscriber Impact": lambda: random.randint(1000, 100000),
    "Brand Endorsements": lambda: random.randint(0, 15),
    "Merchandise Influence": lambda: random.randint(1000, 500000),
    "Media Sentiment": lambda: random.choice(["Positive", "Negative", "Neutral"]),
    "Longevity (Years)": lambda: random.randint(1, 30),
    "Versatility": lambda: random.choice(["Low", "Medium", "High"]),
}

for key, func in random_metrics.items():
    structured_data[key] = [func() for _ in actors]

# Convert to DataFrame
df_final = pd.DataFrame(structured_data)

# Save the file
csv_output_path = "data/actor_metrics_final_ready.csv"
df_final.to_csv(csv_output_path, index=False)

print(f"✅ Actor Metrics Data saved successfully to: {csv_output_path}")