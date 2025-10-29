from typing import List
import numpy as np
import pandas as pd

def aggregate_suitability_scores(suitability_data: pd.DataFrame, hexagon_column: str, score_column: str) -> pd.DataFrame:
    """
    Aggregates suitability scores into a final index per H3 hexagon.

    Parameters:
    suitability_data (pd.DataFrame): DataFrame containing suitability scores and hexagon identifiers.
    hexagon_column (str): The name of the column containing hexagon identifiers.
    score_column (str): The name of the column containing suitability scores.

    Returns:
    pd.DataFrame: A DataFrame with hexagon identifiers and their aggregated suitability scores.
    """
    aggregated_scores = suitability_data.groupby(hexagon_column)[score_column].mean().reset_index()
    aggregated_scores.rename(columns={score_column: 'aggregated_score'}, inplace=True)
    return aggregated_scores

def calculate_weighted_scores(suitability_data: pd.DataFrame, weights: dict, hexagon_column: str) -> pd.DataFrame:
    """
    Calculates weighted suitability scores based on specified weights.

    Parameters:
    suitability_data (pd.DataFrame): DataFrame containing suitability scores.
    weights (dict): A dictionary of weights for each score type.
    hexagon_column (str): The name of the column containing hexagon identifiers.

    Returns:
    pd.DataFrame: A DataFrame with hexagon identifiers and their weighted suitability scores.
    """
    for score_type, weight in weights.items():
        suitability_data[score_type] = suitability_data[score_type] * weight
    
    weighted_scores = suitability_data.groupby(hexagon_column).sum().reset_index()
    weighted_scores.rename(columns={score_type: 'weighted_score'}, inplace=True)
    return weighted_scores

def main(suitability_data: pd.DataFrame, weights: dict, hexagon_column: str, score_column: str) -> pd.DataFrame:
    """
    Main function to aggregate and calculate weighted suitability scores.

    Parameters:
    suitability_data (pd.DataFrame): DataFrame containing suitability scores.
    weights (dict): A dictionary of weights for each score type.
    hexagon_column (str): The name of the column containing hexagon identifiers.
    score_column (str): The name of the column containing suitability scores.

    Returns:
    pd.DataFrame: A DataFrame with hexagon identifiers and their final scores.
    """
    aggregated_scores = aggregate_suitability_scores(suitability_data, hexagon_column, score_column)
    weighted_scores = calculate_weighted_scores(suitability_data, weights, hexagon_column)
    
    final_scores = pd.merge(aggregated_scores, weighted_scores, on=hexagon_column)
    return final_scores