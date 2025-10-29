import unittest
from src.data.loader import load_soil_data, load_biomass_data

class TestDataLoader(unittest.TestCase):

    def test_load_soil_data(self):
        # Test loading soil data from a valid source
        soil_data = load_soil_data('data/raw/soil_data.csv')
        self.assertIsNotNone(soil_data)
        self.assertGreater(len(soil_data), 0)

    def test_load_biomass_data(self):
        # Test loading biomass data from a valid source
        biomass_data = load_biomass_data('data/raw/biomass_data.csv')
        self.assertIsNotNone(biomass_data)
        self.assertGreater(len(biomass_data), 0)

    def test_load_soil_data_invalid(self):
        # Test loading soil data from an invalid source
        with self.assertRaises(FileNotFoundError):
            load_soil_data('data/raw/non_existent_soil_data.csv')

    def test_load_biomass_data_invalid(self):
        # Test loading biomass data from an invalid source
        with self.assertRaises(FileNotFoundError):
            load_biomass_data('data/raw/non_existent_biomass_data.csv')

if __name__ == '__main__':
    unittest.main()