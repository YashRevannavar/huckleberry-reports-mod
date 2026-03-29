import unittest
import pandas as pd
from backend.analytics.analytics_handler import AnalyticsHandler
from backend.data_processing.enums import ActivityType, FeedType

class TestAnalyticsHandler(unittest.TestCase):
    def setUp(self):
        self.handler = AnalyticsHandler()
        self.df = pd.DataFrame([{
            'activity_type': ActivityType.FEED.value,
            'start_time': pd.to_datetime('2024-01-01 10:00:00'),
            'feed_amount_ml': 120.0,
            'feed_type': FeedType.BREAST_MILK.value,
            'duration_minutes': 0.0,
            'diaper_condition': '',
            'temperature': 0.0,
            'weight_kg': 0.0
        }])

    def tearDown(self):
        pass

    def test_calculate_daily_kpis(self):
        result = self.handler.calculate_daily_kpis(self.df)
        self.assertTrue(result.success, "KPI calculation should succeed")
        kpis = result.data
        self.assertEqual(len(kpis), 1)
        self.assertEqual(kpis[0].total_feed_volume_ml, 120.0)

if __name__ == '__main__':
    unittest.main()
