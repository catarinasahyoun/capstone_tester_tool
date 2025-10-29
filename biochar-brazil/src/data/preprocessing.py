import pandas as pd
import numpy as np

def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Fill missing values
    df = df.fillna(method='ffill')
    
    return df

def prepare_data(raw_data_path):
    # Load raw data
    df = pd.read_csv(raw_data_path)
    
    # Clean the data
    df = clean_data(df)
    
    # Additional preprocessing steps can be added here
    
    return df

def normalize_data(df, columns):
    # Normalize specified columns
    for column in columns:
        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
    
    return df

def encode_categorical(df, columns):
    # One-hot encode categorical variables
    df = pd.get_dummies(df, columns=columns, drop_first=True)
    
    return df

def preprocess(raw_data_path, categorical_columns):
    # Prepare the data
    df = prepare_data(raw_data_path)
    
    # Normalize numerical columns (example: 'pH', 'N', 'P', 'K')
    df = normalize_data(df, ['pH', 'N', 'P', 'K'])
    
    # Encode categorical columns
    df = encode_categorical(df, categorical_columns)
    
    return df