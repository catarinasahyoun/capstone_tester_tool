"""
Aggregate suitability and risk scores by H3 hexagon.
"""

def aggregate_by_h3(df):
    if "h3_index" not in df.columns:
        print("Missing H3 index column. Skipping aggregation.")
        return df

    grouped = df.groupby("h3_index").agg({
        "suitability_score": "mean",
        "risk_score": "mean"
    }).reset_index()

    print("Aggregation by H3 index completed.")
    return grouped
