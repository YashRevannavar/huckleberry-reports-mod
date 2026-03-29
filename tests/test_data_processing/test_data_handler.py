import unittest
import os
from backend.data_processing.data_handler import DataHandler

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        self.handler = DataHandler()
        self.test_csv_path = "test_temp.csv"
        with open(self.test_csv_path, "w") as f:
            f.write("Type,Start,End,Duration,Start Condition,End Condition,Notes\n")
            f.write("Feed,2024-01-01 10:00,2024-01-01 10:30,,Breast Milk,120,\n")
            
    def tearDown(self):
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)

    def test_load_data_success(self):
        result = self.handler.load_data(self.test_csv_path)
        self.assertTrue(result.success, "Data loading should succeed for valid CSV")
        self.assertIsNotNone(result.data, "Data tuple should not be None")
        
        records, df = result.data
        self.assertEqual(len(records), 1)
        self.assertEqual(df.iloc[0]['activity_type'], 'Feed')

if __name__ == '__main__':
    unittest.main()
