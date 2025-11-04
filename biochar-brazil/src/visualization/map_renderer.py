"""
Map rendering utilities for the Biochar-Brazil project.
Generates interactive maps using Pydeck (Deck.gl).
"""

from pydeck import Deck, ScatterplotLayer
import pandas as pd
from pathlib import Path


def render_map(
    data: pd.DataFrame,
    output_path: str = "output/maps/biochar_map.html",
    map_style: str = "light",
    zoom_level: int = 5,
    radius: int = 1000
):
    """
    Render an interactive Pydeck map from a DataFrame with latitude and longitude.

    Parameters:
    - data (DataFrame): Must contain 'latitude' and 'longitude' columns.
    - output_path (str): Where to save the HTML map.
    - map_style (str): 'light' or 'dark' map theme.
    - zoom_level (int): Initial zoom level.
    - radius (int): Marker radius for visualization.
    """
    # Validate coordinates
    if "latitude" not in data.columns or "longitude" not in data.columns:
        raise ValueError("DataFrame must contain 'latitude' and 'longitude' columns.")

    data = data.dropna(subset=["latitude", "longitude"])

    scatter_layer = ScatterplotLayer(
        data=data,
        get_position='[longitude, latitude]',
        get_radius=radius,
        get_fill_color='[255, 0, 0, 160]',
        pickable=True,
    )

    deck = Deck(
        layers=[scatter_layer],
        initial_view_state={
            "latitude": float(data["latitude"].mean()),
            "longitude": float(data["longitude"].mean()),
            "zoom": zoom_level,
            "pitch": 0,
        },
        map_style=f"mapbox://styles/mapbox/{map_style}-v10",
        tooltip={"text": "Lat: {latitude}\nLon: {longitude}"},
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    deck.to_html(output_path, notebook_display=False)
    print(f"✅ Interactive map saved to: {output_path}")
