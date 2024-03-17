import unittest
import pandas as pd
import yaml
import logging
from app.prediction import process_data_for_prediction


class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        # Load training data
        self.master_df = pd.read_csv("../data/training_data.csv", dtype={'hr': int, 'yr': int, 'cnt': float})

        with open("../data/config.yaml", 'r') as stream:
            try:
                configs = yaml.safe_load(stream)
                self.model_features = configs.get('model_features', [])
            except yaml.YAMLError as exc:
                logging.error(f"Error loading feature configuration: {exc}")

    def test_process_data_for_valid_date(self):
        """
        Test data processing for a valid date.
        """
        date_str = "2012-06-15"
        processed_df = process_data_for_prediction(date_str, self.master_df, self.model_features)
        self.assertNotEqual(processed_df.empty, True)
        self.assertIn('yr', processed_df.columns)
        self.assertEqual(processed_df['yr'].unique()[0], 1)  # Since 2012 is one year after the base year 2011

    def test_process_data_for_nonexistent_date(self):
        """
        Test data processing for a date that does not exist in the dataset.
        """
        date_str = "2013-01-01"  # There is no data beyond 2012
        processed_df = process_data_for_prediction(date_str, self.master_df, self.model_features)
        self.assertEqual(processed_df.empty, False)


if __name__ == '__main__':
    unittest.main()
