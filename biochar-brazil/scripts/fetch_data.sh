#!/bin/bash
# =========================================================
# Fetch soil and biomass data for the Biochar-Brazil project
# =========================================================

# Define dataset URLs (replace with actual URLs or local file paths)
SOIL_DATA_URL="https://example.com/soil_data.csv"
BIOMASS_DATA_URL="https://example.com/biomass_data.csv"

# Define output directories relative to project root
RAW_DATA_DIR="data/raw"
PROCESSED_DATA_DIR="data/processed"

# Create directories if they don't exist
mkdir -p "$RAW_DATA_DIR"
mkdir -p "$PROCESSED_DATA_DIR"

# Download soil dataset
echo "Fetching soil dataset..."
if curl -fLo "$RAW_DATA_DIR/soil_data.csv" "$SOIL_DATA_URL"; then
    echo "Soil dataset downloaded successfully."
else
    echo "Failed to download soil dataset from $SOIL_DATA_URL"
fi

# Download biomass dataset
echo "Fetching biomass dataset..."
if curl -fLo "$RAW_DATA_DIR/biomass_data.csv" "$BIOMASS_DATA_URL"; then
    echo "Biomass dataset downloaded successfully."
else
    echo "Failed to download biomass dataset from $BIOMASS_DATA_URL"
fi

# Optional: Unzip any .zip files if present
for file in "$RAW_DATA_DIR"/*.zip; do
  [ -e "$file" ] || continue
  echo "Extracting $file..."
  unzip -o "$file" -d "$RAW_DATA_DIR"
done

echo "Data fetching completed. Files are available in $RAW_DATA_DIR"
