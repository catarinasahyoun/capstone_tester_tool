"""
Data preprocessing utilities for the Biochar-Brazil project.
Handles cleaning, normalization, and encoding for multiple dataset types.
"""

import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the input DataFrame:
    - Remove duplicates
    - Fill missing numeric values with column mean
    - Drop rows with missing coordinates if present
    """
    df = df.drop_duplicates()

    # If latitude/longitude exist, drop rows missing them
    if "latitude" in df.columns and "longitude" in df.columns:
        df = df.dropna(subset=["latitude", "longitude"])

    # Fill numeric NaN with mean
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    print("Data cleaned successfully.")
    return df


def normalize_data(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Normalize numeric columns to range [0,1].
    Skips columns that are not found in the DataFrame.
    """
    for column in columns:
        if column in df.columns:
            min_val = df[column].min()
            max_val = df[column].max()
            if pd.notna(min_val) and pd.notna(max_val) and max_val != min_val:
                df[column] = (df[column] - min_val) / (max_val - min_val)
    print("Numeric normalization completed.")
    return df


def encode_categorical(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    One-hot encode categorical variables, if present.
    """
    cols_to_encode = [c for c in columns if c in df.columns]
    if cols_to_encode:
        df = pd.get_dummies(df, columns=cols_to_encode, drop_first=True)
        print(f"Encoded categorical columns: {cols_to_encode}")
    return df


def preprocess(raw_data_path: str, categorical_columns: list[str] = None) -> pd.DataFrame:
    """
    Full preprocessing pipeline:
    - Load CSV
    - Clean data
    - Normalize numeric columns (pH, N, P, K if available)
    - Encode categorical columns (if any)
    """
    df = pd.read_csv(raw_data_path)
    df = clean_data(df)

    # Normalize known numeric columns (only if they exist)
    df = normalize_data(df, ["pH", "N", "P", "K", "organic_carbon", "moisture"])

    # Encode categorical variables (optional)
    if categorical_columns:
        df = encode_categorical(df, categorical_columns)

    print(f"Preprocessing completed for {raw_data_path}")
    return df
