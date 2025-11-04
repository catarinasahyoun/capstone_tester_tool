"""
Feedstock / biochar dataset loader.
Compatible with your uploaded Dataset_feedstock_ML.xlsx
"""

from typing import List
import pandas as pd
from pathlib import Path

CANDIDATE_COLUMNS = {
    "id": "id",
    "name": "name",
    "feedstock": "feedstock",
    "fixed carbon": "fixed_carbon",
    "volatile matter": "volatile_matter",
    "ash": "ash",
    "moisture": "moisture",
    "c": "c_pct", "c%": "c_pct", "c_pct": "c_pct",
    "h": "h_pct", "h%": "h_pct", "h_pct": "h_pct",
    "o": "o_pct", "o%": "o_pct", "o_pct": "o_pct",
    "o/c": "o_c_ratio", "o_c_ratio": "o_c_ratio",
    "pH": "pH", "ph": "pH",
    "bet": "bet", "surface area": "bet",
    "pore volume": "pore_volume",
    "density": "density",
    "production temp": "production_temp", "final temperature": "production_temp",
}

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = {c: c.strip().lower() for c in df.columns}
    df = df.rename(columns=cols)
    mapped = {}
    for c in df.columns:
        key = c
        if c in CANDIDATE_COLUMNS:
            mapped[c] = CANDIDATE_COLUMNS[c]
        else:
            # try loose matching
            for k, v in CANDIDATE_COLUMNS.items():
                if k in c:
                    mapped[c] = v
                    break
    df = df.rename(columns=mapped)
    return df

def load_biochar_dataset(path: str | Path = "data/processed/Dataset_feedstock_ML.xlsx") -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        # fallback to uploaded path if running locally
        alt = Path("/mnt/data/Dataset_feedstock_ML.xlsx")
        if alt.exists():
            path = alt
        else:
            raise FileNotFoundError(f"Biochar dataset not found at {path}")

    df = pd.read_excel(path)
    df = _normalize_columns(df)
    # keep only the columns the engine understands; missing are ok
    keep = [
        "id","name","feedstock","fixed_carbon","volatile_matter","ash","moisture",
        "c_pct","h_pct","o_pct","o_c_ratio","pH","bet","pore_volume","density","production_temp"
    ]
    cols_present = [c for c in keep if c in df.columns]
    # ensure there is an id
    if "id" not in cols_present:
        df["id"] = df.index.astype(str)
        cols_present = ["id"] + [c for c in cols_present if c != "id"]
    if "name" not in cols_present:
        df["name"] = df["feedstock"] if "feedstock" in df.columns else df["id"]
        if "name" not in cols_present: cols_present = ["name"] + cols_present
    return df[cols_present]
