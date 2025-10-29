from typing import List
import pandas as pd

def calculate_suitability_score(soil_properties: pd.DataFrame) -> pd.Series:
    # Example scoring logic based on soil properties
    score = (soil_properties['pH'] - 5.5) * 2 + (soil_properties['organic_matter'] - 3) * 3
    return score.clip(lower=0)  # Ensure scores are non-negative

def assess_suitability(soil_data: pd.DataFrame) -> pd.DataFrame:
    soil_data['suitability_score'] = calculate_suitability_score(soil_data)
    return soil_data[['location', 'suitability_score']]

def identify_high_potential_areas(soil_data: pd.DataFrame, threshold: float) -> List[str]:
    high_potential_areas = soil_data[soil_data['suitability_score'] > threshold]
    return high_potential_areas['location'].tolist()