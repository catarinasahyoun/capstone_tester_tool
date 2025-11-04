"""
Estimate environmental or agricultural risks associated with biochar application.
"""

def assess_risk(df):
    """
    Compute a simple inverse risk score based on suitability.
    In future, integrate environmental or toxicity data.
    """
    if "suitability_score" not in df.columns:
        print("Suitability scores missing. Run calculate_suitability() first.")
        return df

    df["risk_score"] = 1 - (df["suitability_score"] / df["suitability_score"].max())
    print("Risk assessment completed.")
    return df[["h3_index", "risk_score"]]
