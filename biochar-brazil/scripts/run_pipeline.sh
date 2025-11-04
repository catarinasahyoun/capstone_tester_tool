#!/bin/bash
# =========================================================
# Run full Biochar-Brazil modeling pipeline
# =========================================================

echo "Starting Biochar-Brazil pipeline..."

# Step 1: Fetch required datasets
bash ./scripts/fetch_data.sh

# Step 2: Execute main modeling pipeline
echo "Running main analysis workflow..."
python3 src/main.py

# Step 3: Completion message
echo "Pipeline execution completed successfully."
echo "Processed results are saved in the data/processed directory."
