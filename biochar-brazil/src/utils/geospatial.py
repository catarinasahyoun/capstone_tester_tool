"""
Geospatial helper functions for the Biochar-Brazil project.
Includes:
- Conversion between H3 hexagons and geographic coordinates.
- Sampling or mock extraction of soil properties.
"""

from typing import Dict, Any, Tuple
from h3 import h3


def h3_to_latlon(h3_id: str) -> Tuple[float, float]:
    """
    Convert an H3 cell ID to its centroid latitude and longitude.
    """
    lat, lon = h3.cell_to_latlng(h3_id)
    return float(lat), float(lon)


def get_soil_properties_from_h3(h3_id: str) -> Dict[str, Any]:
    """
    Retrieve soil property values corresponding to an H3 cell.
    Replace mock data with real raster or tabular lookups later.
    """
    lat, lon = h3_to_latlon(h3_id)

    # Mock values for now — can be replaced with GEE or raster sampling later
    soil = {
        "pH": 5.8,                # example soil pH
        "SOC": 2.4,               # soil organic carbon (%)
        "moisture": 53.0,         # %
        "EC": 1.1,                # electrical conductivity (dS/m)
        "temp": 27.0,             # temperature (°C)
        "texture": "sandy loam",  # soil texture class
        "latitude": lat,
        "longitude": lon,
    }
    return soil
