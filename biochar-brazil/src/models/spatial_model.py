"""
Spatial modeling utilities for the Biochar-Brazil project.
Integrates H3 geospatial encoding and polygon boundary checks.
"""

import geopandas as gpd
import pandas as pd
import h3
from shapely.geometry import Point, Polygon


class SpatialModel:
    def __init__(self, boundary: Polygon = None, h3_resolution: int = 6):
        self.boundary = boundary
        self.h3_resolution = h3_resolution

    def add_h3_index(self, df: pd.DataFrame, lat_col="latitude", lon_col="longitude") -> pd.DataFrame:
        """
        Add an H3 index column based on coordinates.
        """
        if lat_col not in df.columns or lon_col not in df.columns:
            raise ValueError("Missing latitude/longitude columns.")
        df["h3_index"] = df.apply(lambda row: h3.geo_to_h3(row[lat_col], row[lon_col], self.h3_resolution), axis=1)
        print(f"✅ Added H3 index (resolution {self.h3_resolution}) to {len(df)} rows.")
        return df

    def aggregate_by_hex(self, df: pd.DataFrame, value_col: str) -> pd.DataFrame:
        """
        Aggregate numerical values by H3 hexagon.
        """
        if "h3_index" not in df.columns:
            raise ValueError("Missing 'h3_index' column.")
        grouped = df.groupby("h3_index")[value_col].mean().reset_index()
        print(f"✅ Aggregated '{value_col}' by H3 hexagon.")
        return grouped

    def h3_to_geodataframe(self, df: pd.DataFrame) -> gpd.GeoDataFrame:
        """
        Convert H3 indices into polygons for visualization.
        """
        polygons = []
        for h in df["h3_index"]:
            boundary = h3.h3_to_geo_boundary(h, geo_json=True)
            polygons.append(Polygon(boundary))
        gdf = gpd.GeoDataFrame(df, geometry=polygons, crs="EPSG:4326")
        print(f"✅ Converted {len(gdf)} H3 cells into GeoDataFrame polygons.")
        return gdf

    def is_within_boundary(self, point: Point) -> bool:
        """
        Check if a point is within the specified boundary polygon.
        """
        if self.boundary is None:
            return True
        return self.boundary.contains(point)
