import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Load your dataset
df = pd.read_excel("campaign_data.xlsx")

# Define 'Success' column using business logic
df["Success"] = (
    (df["CTR (%)"] >= 2.5) &
    (df["ROAS"] >= 3.0) &
    (df["Conversion Rate (%)"] >= 1.8) &
    (df["CPA ($)"] <= 16)
).astype(int)

# Select features and target
X = df[["CTR (%)", "ROAS", "Conversion Rate (%)", "CPA ($)"]]
y = df["Success"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "models/campaign_success_model.pkl")
print("✅ Model trained and saved to models/campaign_success_model.pkl")