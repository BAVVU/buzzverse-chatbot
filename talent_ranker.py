import pandas as pd
from scipy.stats import zscore

def rank_actors(file_path="data/actor_metrics_final_ready.csv", weights=None):
    """
    Rank actors based on normalized metrics and optional weights.

    Args:
        file_path: CSV file path containing actor metrics.
        weights: Optional dictionary of {metric: weight}.
                 If None, equal weight is assigned to all metrics.

    Returns:
        Ranked DataFrame with Actor, Final Score, and metric columns.
    """

    # Load data
    df = pd.read_csv(file_path)

    # Select numeric columns (excluding 'Actor' name)
    numeric_cols = df.select_dtypes(include=[int, float]).columns.tolist()
    if "Actor" in numeric_cols:
        numeric_cols.remove("Actor")

    # Normalize metrics using Z-Score
    df_z = df[numeric_cols].apply(zscore)

    # Handle custom weights
    if weights is None:
        weights = {col: 1 / len(numeric_cols) for col in numeric_cols}

    # Calculate Final Score
    weight_series = pd.Series(weights)
    used_cols = list(weight_series.keys())

    df["Final Score"] = df_z[used_cols].dot(weight_series)

    # Rank actors by Final Score
    ranked_df = df.sort_values(by="Final Score", ascending=False).reset_index(drop=True)

    return ranked_df[["Actor", "Final Score"] + used_cols]