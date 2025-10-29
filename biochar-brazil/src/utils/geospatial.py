def validate_coordinates(lat, lon):
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not (-180 <= lon <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")
    return True

def calculate_distance(coord1, coord2):
    from geopy.distance import geodesic
    return geodesic(coord1, coord2).kilometers

def convert_to_geojson(features):
    import geojson
    return geojson.dumps({"type": "FeatureCollection", "features": features})

def extract_coordinates(geojson_feature):
    return geojson_feature['geometry']['coordinates']