import unittest
from src.analysis.suitability import calculate_suitability_score

class TestSuitability(unittest.TestCase):

    def test_suitability_score(self):
        # Example input data for testing
        soil_properties = {
            'ph': 6.5,
            'organic_matter': 3.0,
            'texture': 'loamy',
            'moisture': 20
        }
        
        # Expected output based on the input data
        expected_score = 0.85  # This value should be determined based on the actual scoring logic
        
        # Calculate the suitability score
        score = calculate_suitability_score(soil_properties)
        
        # Assert that the calculated score matches the expected score
        self.assertAlmostEqual(score, expected_score, places=2)

if __name__ == '__main__':
    unittest.main()