"""
Static plotting utilities for the Biochar-Brazil project.
Generates histograms, bar charts, and heatmaps using Matplotlib and Seaborn.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path


def plot_suitability_scores(suitability_data: pd.Series, output_path: str = "output/plots/suitability_scores.png"):
    """
    Plot the distribution of suitability scores.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(suitability_data, bins=30, kde=True)
    plt.title("Distribution of Suitability Scores for Biochar Application")
    plt.xlabel("Suitability Score")
    plt.ylabel("Frequency")
    plt.grid(True)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved suitability score distribution: {output_path}")


def plot_risk_assessment(risk_data: pd.DataFrame, output_path: str = "output/plots/risk_assessment.png"):
    """
    Plot bar chart for risk assessment.
    Expects columns: 'Risk Factor', 'Value'
    """
    if not {"Risk Factor", "Value"}.issubset(risk_data.columns):
        raise ValueError("risk_data must contain columns: 'Risk Factor' and 'Value'")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="Risk Factor", y="Value", data=risk_data)
    plt.title("Risk Assessment for Biochar Application")
    plt.xlabel("Risk Factor")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved risk assessment plot: {output_path}")


def plot_aggregated_scores(aggregated_data: pd.DataFrame, output_path: str = "output/plots/aggregated_heatmap.png"):
    """
    Plot a heatmap of aggregated suitability scores by region or H3 index.
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(aggregated_data, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Aggregated Suitability Scores by Region")
    plt.xlabel("Region")
    plt.ylabel("Score")
    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved aggregated heatmap: {output_path}")
