import pandas as pd
import geopandas as gpd

def load_soil_data(file_path):
    """
    Load soil data from a specified CSV file.
    
    Parameters:
    - file_path: str, path to the soil data CSV file.
    
    Returns:
    - GeoDataFrame containing the soil data.
    """
    soil_data = pd.read_csv(file_path)
    return gpd.GeoDataFrame(soil_data)

def load_biomass_data(file_path):
    """
    Load biomass data from a specified CSV file.
    
    Parameters:
    - file_path: str, path to the biomass data CSV file.
    
    Returns:
    - GeoDataFrame containing the biomass data.
    """
    biomass_data = pd.read_csv(file_path)
    return gpd.GeoDataFrame(biomass_data)

def load_external_data(file_path):
    """
    Load external datasets from a specified file path.
    
    Parameters:
    - file_path: str, path to the external data file.
    
    Returns:
    - DataFrame containing the external data.
    """
    return pd.read_csv(file_path)