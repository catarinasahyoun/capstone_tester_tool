"""
File I/O helper utilities for the Biochar-Brazil project.
Supports reading and writing of text, CSV, and structured files.
"""

import pandas as pd
from pathlib import Path


def read_data(file_path: str) -> str:
    """
    Read plain text data from a file.
    """
    file_path = Path(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_data(file_path: str, data: str):
    """
    Write text data to a file (overwrites existing content).
    """
    file_path = Path(file_path)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)


def append_data(file_path: str, data: str):
    """
    Append text data to an existing file.
    """
    file_path = Path(file_path)
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(data)


def read_csv(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.
    """
    file_path = Path(file_path)
    return pd.read_csv(file_path)


def write_csv(file_path: str, dataframe: pd.DataFrame):
    """
    Write a pandas DataFrame to a CSV file.
    """
    file_path = Path(file_path)
    dataframe.to_csv(file_path, index=False)
    print(f"✅ CSV saved: {file_path}")
