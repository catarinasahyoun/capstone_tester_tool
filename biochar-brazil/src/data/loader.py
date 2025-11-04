"""
General data loader for all CSV/Excel datasets used in the Biochar-Brazil project.
Supports multiple datasets (soil, biomass, environmental, etc.).
"""

from pathlib import Path
import pandas as pd

def load_data(path: str | Path) -> pd.DataFrame:
    """
    Load a dataset (CSV or Excel) from the given path.
    Automatically detects file format.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    if path.suffix.lower() in [".csv"]:
        df = pd.read_csv(path)
    elif path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    print(f"Loaded dataset from {path} with {len(df)} rows and {len(df.columns)} columns.")
    return df


def load_multiple(datasets: list[str] | None = None, base_dir: str = "data/raw") -> dict[str, pd.DataFrame]:
    """
    Load multiple datasets at once from the raw data folder.
    Returns a dictionary of DataFrames.
    Example: data = load_multiple(["soil_data.csv", "biomass_data.csv"])
    """
    base_path = Path(base_dir)
    if datasets is None:
        datasets = [p.name for p in base_path.glob("*.csv")]

    loaded = {}
    for file_name in datasets:
        try:
            df = load_data(base_path / file_name)
            loaded[file_name] = df
        except Exception as e:
            print(f"Warning: Could not load {file_name}: {e}")
    return loaded
