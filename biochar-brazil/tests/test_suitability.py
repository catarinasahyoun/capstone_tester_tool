import unittest
import pandas as pd
from src.analysis.suitability import calculate_suitability


class TestSuitability(unittest.TestCase):

    def setUp(self):
        """Prepare mock soil dataset for suitability analysis."""
        self.mock_data = pd.DataFrame([
            {"id": 1, "pH": 6.5, "moisture": 20, "SOC": 2.5, "ash": 10, "fixed_carbon": 70},
            {"id": 2, "pH": 8.2, "moisture": 30, "SOC": 3.0, "ash": 15, "fixed_carbon": 60}
        ])

    def test_calculate_suitability_output_type(self):
        """Test that calculate_suitability returns a DataFrame."""
        result = calculate_suitability(self.mock_data)
        self.assertIsInstance(result, pd.DataFrame)

    def test_calculate_suitability_has_scores(self):
        """Ensure suitability scores are generated."""
        result = calculate_suitability(self.mock_data)
        self.assertIn("suitability_score", result.columns)
        self.assertGreater(result["suitability_score"].mean(), 0)

    def test_suitability_score_range(self):
        """Check that all scores are within [0, 1]."""
        result = calculate_suitability(self.mock_data)
        self.assertTrue(result["suitability_score"].between(0, 1).all())


if __name__ == "__main__":
    unittest.main()
