import unittest
import os
from src.data.loader import load_biochar_dataset
import pandas as pd


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        """Set up test environment and test file paths."""
        self.valid_path = "data/processed/Dataset_feedstock_ML.xlsx"
        self.invalid_path = "data/raw/non_existent_file.xlsx"

        # Create a small mock dataset if not present
        os.makedirs("data/processed", exist_ok=True)
        if not os.path.exists(self.valid_path):
            df_mock = pd.DataFrame({
                "id": [1, 2],
                "feedstock": ["wood", "coconut shell"],
                "fixed carbon": [75, 68],
                "volatile matter": [18, 22],
                "ash": [5, 8],
                "pH": [8.1, 9.0]
            })
            df_mock.to_excel(self.valid_path, index=False)

    def test_load_biochar_dataset_valid(self):
        """Test loading a valid biochar dataset."""
        df = load_biochar_dataset(self.valid_path)
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        self.assertIn("feedstock", df.columns)

    def test_load_biochar_dataset_invalid(self):
        """Test loading a dataset from an invalid path."""
        with self.assertRaises(FileNotFoundError):
            load_biochar_dataset(self.invalid_path)

    def tearDown(self):
        """Clean up after tests (optional)."""
        # You could remove mock files if you want a clean environment
        pass


if __name__ == "__main__":
    unittest.main()
