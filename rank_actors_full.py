
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
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore

def rank_actors_full(file_path="data/actor_metrics_final_ready.csv",
                     weighting_method="equal",
                     manual_weights=None,
                     cutoff_percentile=None,
                     target_success_metric=None):
    """
    Full actor ranking engine: normalization, dynamic weighting (equal, pca, regression, manual),
    scoring, ranking, and optional cutoff.

    Args:
        file_path: CSV file path for actor metrics.
        weighting_method: "equal", "pca", "regression", "manual".
        manual_weights: Dictionary if using manual weights.
        cutoff_percentile: e.g., 90 for Top 10% or 70 for Top 30%.
        target_success_metric: Column name (needed if regression-based weighting).
        
    Returns:
        Ranked DataFrame.
    """

    # Step 1: Load and Clean
    df = pd.read_csv(file_path)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if 'Actor' in numeric_cols:
        numeric_cols.remove('Actor')

    # Handle missing values
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Step 2: Z-Score Normalization
    df_z = df.copy()
    df_z[numeric_cols] = df_z[numeric_cols].apply(zscore)

    # Step 3: Dynamic Weight Assignment
    if weighting_method == "equal":
        weights = {col: 1/len(numeric_cols) for col in numeric_cols}

    elif weighting_method == "pca":
        pca = PCA()
        pca.fit(df_z[numeric_cols])
        loadings = np.abs(pca.components_).sum(axis=0)
        weights_array = loadings / loadings.sum()
        weights = {col: w for col, w in zip(numeric_cols, weights_array)}

    elif weighting_method == "regression":
        if not target_success_metric:
            raise ValueError("Provide target_success_metric for regression-based weighting.")
        if target_success_metric not in numeric_cols:
            raise ValueError(f"Target metric {target_success_metric} not found in columns.")

        X = df_z[numeric_cols].drop(columns=[target_success_metric])
        y = df_z[target_success_metric]
        model = LinearRegression()
        model.fit(X, y)
        importances = np.abs(model.coef_)
        weights_array = importances / importances.sum()
        feature_cols = X.columns.tolist()
        weights = {col: w for col, w in zip(feature_cols, weights_array)}

    elif weighting_method == "manual":
        if manual_weights is None:
            raise ValueError("Provide manual_weights when weighting_method is 'manual'.")
        weights = manual_weights

    else:
        raise ValueError("Invalid weighting_method. Choose from 'equal', 'pca', 'regression', or 'manual'.")

    # Step 4: Final Weighted Score Calculation
    weight_series = pd.Series(weights)
    used_cols = list(weight_series.keys())
    df_z['Final Score'] = df_z[used_cols].dot(weight_series)

    # Step 5: Actor Ranking
    ranked_df = df_z.sort_values(by="Final Score", ascending=False).reset_index(drop=True)

    # Step 6: Optional Cutoff
    if cutoff_percentile is not None:
        threshold_score = np.percentile(ranked_df['Final Score'], 100 - cutoff_percentile)
        ranked_df = ranked_df[ranked_df['Final Score'] >= threshold_score].reset_index(drop=True)

    return ranked_df[['Actor', 'Final Score'] + used_cols]