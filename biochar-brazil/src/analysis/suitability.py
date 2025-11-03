from typing import List
import pandas as pd

# --- Existing basic suitability functions ---------------------------------

def calculate_suitability_score(soil_properties: pd.DataFrame) -> pd.Series:
    """Simple scoring logic based on soil pH and organic matter."""
    score = (soil_properties['pH'] - 5.5) * 2 + (soil_properties['organic_matter'] - 3) * 3
    return score.clip(lower=0)  # Ensure scores are non-negative


def assess_suitability(soil_data: pd.DataFrame) -> pd.DataFrame:
    """Assess soil suitability using basic soil properties."""
    soil_data['suitability_score'] = calculate_suitability_score(soil_data)
    return soil_data[['location', 'suitability_score']]


def identify_high_potential_areas(soil_data: pd.DataFrame, threshold: float) -> List[str]:
    """Identify locations exceeding a given suitability score threshold."""
    high_potential_areas = soil_data[soil_data['suitability_score'] > threshold]
    return high_potential_areas['location'].tolist()


# --- Advanced Threshold-based Biochar Evaluation --------------------------

from src.analysis.thresholds import evaluate_soil_against_biochars


def evaluate_biochar_suitability(soil_row: pd.Series, biochar_data: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluate which biochars are most suitable for a single soil sample
    using the threshold engine from thresholds.py.
    """
    # Convert one soil record (row) to a dict
    soil_dict = {
        "moisture": soil_row.get("moisture"),
        "pH": soil_row.get("pH"),
        "SOC": soil_row.get("organic_matter") or soil_row.get("SOC"),
        "EC": soil_row.get("EC"),
        "temp": soil_row.get("temperature"),
        "texture": soil_row.get("texture"),
    }

    # Convert DataFrame of biochar properties to list of dicts
    biochar_list = biochar_data.to_dict(orient="records")

    # Evaluate all biochars for this soil sample
    results = evaluate_soil_against_biochars(soil_dict, biochar_list)

    # Convert to DataFrame for easy ranking and integration
    return pd.DataFrame(results).sort_values(by="score", ascending=False)


def batch_biochar_evaluation(soil_data: pd.DataFrame, biochar_data: pd.DataFrame) -> pd.DataFrame:
    """
    Run biochar suitability evaluation for multiple soil locations.
    Returns a long-format DataFrame linking each soil site to best-matched biochars.
    """
    all_results = []
    for _, row in soil_data.iterrows():
        soil_location = row.get("location", f"Sample_{_}")
        eval_df = evaluate_biochar_suitability(row, biochar_data)
        eval_df.insert(0, "location", soil_location)
        all_results.append(eval_df)

    return pd.concat(all_results, ignore_index=True)
