from typing import List, Dict, Any
import pandas as pd

# --- your original simple scoring kept intact ------------------------------

def calculate_suitability_score(soil_properties: pd.DataFrame) -> pd.Series:
    score = (soil_properties['pH'] - 5.5) * 2 + (soil_properties['organic_matter'] - 3) * 3
    return score.clip(lower=0)

def assess_suitability(soil_data: pd.DataFrame) -> pd.DataFrame:
    soil_data['suitability_score'] = calculate_suitability_score(soil_data)
    return soil_data[['location', 'suitability_score']]

def identify_high_potential_areas(soil_data: pd.DataFrame, threshold: float) -> List[str]:
    high_potential_areas = soil_data[soil_data['suitability_score'] > threshold]
    return high_potential_areas['location'].tolist()

# --- new: threshold engine + H3 integration --------------------------------

from src.utils.geospatial import get_soil_properties_from_h3
from src.data.loader import load_biochar_dataset
from src.analysis.thresholds import evaluate_soil_against_biochars

def evaluate_point_suitability(h3_cell_id: str,
                               dataset_path: str | None = None,
                               top_n: int = 10) -> pd.DataFrame:
    """
    Main entry for map click on an H3 cell.
    1) Read soil props from your GEE layers at the H3 centroid
    2) Load biochar dataset (Excel)
    3) Run threshold engine (cumulative 0–20)
    4) Return ranked results as DataFrame
    """
    soil = get_soil_properties_from_h3(h3_cell_id)
    df_chars = load_biochar_dataset(dataset_path)  # DataFrame
    bio_list = df_chars.to_dict(orient="records")
    results = evaluate_soil_against_biochars(soil, bio_list)
    out = pd.DataFrame(results)
    out.insert(0, "h3_id", h3_cell_id)
    out.insert(1, "soil_pH", soil.get("pH"))
    out.insert(2, "soil_SOC", soil.get("SOC"))
    out.insert(3, "soil_moisture", soil.get("moisture"))
    out.insert(4, "soil_EC", soil.get("EC"))
    out.insert(5, "soil_temp", soil.get("temp"))
    out.insert(6, "soil_texture", soil.get("texture"))
    if top_n:
        out = out.head(top_n)
    return out
