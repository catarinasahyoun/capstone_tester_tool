from pydeck import Deck, ScatterplotLayer
import pandas as pd

def render_map(data, map_style='light', zoom_level=5):
    """
    Renders an interactive map using Pydeck.

    Parameters:
    - data: DataFrame containing latitude and longitude for points to plot.
    - map_style: The style of the map (e.g., 'light', 'dark').
    - zoom_level: Initial zoom level for the map.
    """
    # Create a scatter plot layer
    scatter_layer = ScatterplotLayer(
        data=data,
        get_position='[longitude, latitude]',
        get_radius=1000,
        get_fill_color='[255, 0, 0, 160]',
        pickable=True,
    )

    # Create the deck
    deck = Deck(
        layers=[scatter_layer],
        initial_view_state={
            'latitude': data['latitude'].mean(),
            'longitude': data['longitude'].mean(),
            'zoom': zoom_level,
            'pitch': 0,
        },
        map_style=map_style,
    )

    # Render the map
    deck.to_html('biochar_map.html', notebook_display=True)