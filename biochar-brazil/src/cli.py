"""
Command-Line Interface for the Biochar-Brazil Suitability Analysis Tool.
"""

import argparse
import yaml
import logging.config
from pathlib import Path

from src.data.loader import load_biochar_dataset
from src.analysis.suitability import calculate_suitability
from src.visualization.plots import plot_suitability_scores
from src.visualization.map_renderer import render_map


def load_config(config_path: str):
    """
    Load YAML configuration file.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def setup_logging(logging_config_path="configs/logging.yaml"):
    """
    Configure logging for CLI runtime.
    """
    import yaml
    if Path(logging_config_path).exists():
        with open(logging_config_path, "r") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Biochar Application Suitability Tool")
    parser.add_argument(
        "--config", type=str, default="configs/config.yaml",
        help="Path to configuration YAML file"
    )
    parser.add_argument(
        "--output", type=str, default="output/",
        help="Directory to save results and plots"
    )
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger("biochar_cli")

    logger.info("Starting Biochar-Brazil analysis pipeline...")
    config = load_config(args.config)
    Path(args.output).mkdir(parents=True, exist_ok=True)

    # 1. Load dataset
    logger.info("Loading dataset...")
    data = load_biochar_dataset(config["data"]["processed_data_path"] + "Dataset_feedstock_ML.xlsx")

    # 2. Calculate suitability
    logger.info("Calculating suitability scores...")
    suitability_scores = calculate_suitability(data)

    # 3. Save plots
    logger.info("Generating visualizations...")
    plot_suitability_scores(suitability_scores["score"], f"{args.output}/suitability_distribution.png")

    # Optionally, if lat/lon exist in your dataset:
    if "latitude" in data.columns and "longitude" in data.columns:
        render_map(data, output_path=f"{args.output}/biochar_map.html")

    logger.info("Analysis complete. Results saved to: %s", args.output)


if __name__ == "__main__":
    main()
