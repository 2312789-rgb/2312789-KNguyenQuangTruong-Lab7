import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Basic order-total tests."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 2}), 100000)

    def test_calculate_total_for_multiple_items(self):
        self.assertEqual(
            self.app.calculate_order_total({"pho": 1, "bun": 1}), 95000
        )

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0.0)


class TestMediumLevel(unittest.TestCase):
    """Promotion-code tests."""

    def test_online_giam10_applies_ten_percent_discount(self):
        app = YummyApp(network_status="online")
        self.assertEqual(app.apply_promo_code(1000, "GIAM10"), 900)

    def test_offline_promo_validation_raises_connection_error(self):
        app = YummyApp(network_status="offline")
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(1000, "GIAM10")

    def test_new_os_promo_applies_on_os_15(self):
        app = YummyApp(os_version=15)
        self.assertEqual(app.apply_promo_code(1000, "NEW_OS_ONLY"), 800)

    def test_new_os_promo_rejected_on_os_14(self):
        app = YummyApp(os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(1000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    """GPS-dependent nearby-restaurant tests."""

    def setUp(self):
        self.app = YummyApp()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_location_returns_two_nearby_restaurants(self, mock_location):
        mock_location.return_value = (10.0, 105.0)
        self.assertEqual(
            self.app.get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_outside_coverage_returns_empty_list(self, mock_location):
        mock_location.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])
        mock_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_lost_gps_signal_returns_location_error_message(
        self, mock_location
    ):
        mock_location.side_effect = gps_service.GPSSignalLostError
        self.assertEqual(
            self.app.get_nearby_restaurants(), "Unable to determine location."
        )
        mock_location.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
