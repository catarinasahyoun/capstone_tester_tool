"""
Geospatial helpers:
- Convert H3 cell to centroid (lat/lon)
- Sample your downloaded GEE layers to get soil properties at that cell
"""

from typing import Dict, Any
from h3 import h3

# If your GEE layers are saved as GeoTIFFs, you can wire rasterio here.
# from rasterio.sample import sample_gen  # example
# import rasterio

def h3_to_latlon(h3_id: str) -> tuple[float, float]:
    lat, lon = h3.cell_to_latlng(h3_id)
    return float(lat), float(lon)

def get_soil_properties_from_h3(h3_id: str) -> Dict[str, Any]:
    lat, lon = h3_to_latlon(h3_id)

    # TODO: Replace the mock values below with real raster sampling or table lookup
    # Example idea:
    # with rasterio.open("data/external/soil_ph.tif") as src:
    #     pH = list(src.sample([(lon, lat)]))[0][0]
    # ... repeat for SOC, moisture, EC, temp, texture code ...

    soil = {
        "pH": 5.8,          # mock
        "SOC": 2.4,         # mock, %
        "moisture": 53.0,   # mock, %
        "EC": 1.1,          # mock, dS/m
        "temp": 27.0,       # mock, °C
        "texture": "sandy loam",  # mock or derived from a texture raster
        "lat": lat,
        "lon": lon,
    }
    return soil
