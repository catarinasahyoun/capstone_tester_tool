#!/bin/bash

# Fetch data
bash ./scripts/fetch_data.sh

# Preprocess data
python3 -m src.data.preprocessing

# Run analysis
python3 -m src.analysis.suitability
python3 -m src.analysis.risk_assessment
python3 -m src.analysis.aggregation

# Generate visualizations
python3 -m src.visualization.map_renderer
python3 -m src.visualization.plots

# Save results
echo "Pipeline execution completed. Results are saved in the data/processed directory."