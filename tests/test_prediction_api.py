import unittest
import requests


class TestPredictionService(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5555/prediction"

    def test_valid_date(self):
        """Test prediction with a valid date."""
        response = requests.post(self.BASE_URL, json={'date': '2012-06-15'})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 24)  # Assuming 24 hours in response
        for hour, prediction in data.items():
            self.assertIsInstance(prediction, float)

    def test_invalid_date_format(self):
        """Test prediction with an invalid date format."""
        response = requests.post(self.BASE_URL, json={'date': '15-06-2012'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_missing_date(self):
        """Test prediction without providing a date."""
        response = requests.post(self.BASE_URL, json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_future_date(self):
        """Test prediction with a future dates."""
        response = requests.post(self.BASE_URL, json={'date': '2025-07-15'})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        for hour, prediction in data.items():
            self.assertIsInstance(prediction, float)  # check if it handles future dates gracefully

    def test_leap_year_date(self):
        """Test prediction for a date in a leap year."""
        response = requests.post(self.BASE_URL, json={'date': '2012-02-29'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)

    def test_nonexistent_date(self):
        """Test prediction for a nonexistent date."""
        response = requests.post(self.BASE_URL, json={'date': '2019-02-29'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


if __name__ == "__main__":
    unittest.main()
