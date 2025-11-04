"""
Compute biochar application suitability based on soil and biomass properties.
"""

def calculate_suitability(df):
    """
    Calculate suitability score for biochar application.
    Weights can be adjusted in future versions or read from config.
    """
    if df.empty:
        print("No data available for suitability calculation.")
        return df

    # Weighted model: adjust based on domain knowledge
    df["suitability_score"] = (
        0.4 * df.get("pH", 0) +
        0.3 * df.get("organic_carbon", 0) +
        0.3 * df.get("moisture", 0)
    )

    print("Suitability analysis completed.")
    return df[["h3_index", "suitability_score"]]
