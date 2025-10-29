from shapely.geometry import Point, Polygon
import geopandas as gpd
import numpy as np

class SpatialModel:
    def __init__(self, boundary: Polygon):
        self.boundary = boundary

    def is_within_boundary(self, point: Point) -> bool:
        return self.boundary.contains(point)

    def calculate_distance(self, point1: Point, point2: Point) -> float:
        return point1.distance(point2)

    def find_high_potential_areas(self, points: gpd.GeoDataFrame, threshold: float) -> gpd.GeoDataFrame:
        high_potential_areas = points[points.geometry.apply(lambda x: self.is_within_boundary(x))]
        high_potential_areas['distance_to_boundary'] = high_potential_areas.geometry.apply(
            lambda x: self.calculate_distance(x, self.boundary.exterior)
        )
        return high_potential_areas[high_potential_areas['distance_to_boundary'] < threshold]