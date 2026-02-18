"""Unit tests for Reservation class."""
import unittest
from unittest.mock import patch
from src.reservation import Reservation
from src.customer import Customer

class TestReservation(unittest.TestCase):
    """Test cases for Reservation functionality."""

    @patch("src.reservation.Reservation.get_all", return_value=[])
    @patch("src.customer.Customer.get_all")
    @patch("src.hotel.Hotel.reserve_room", return_value=True)
    @patch("src.reservation.Reservation.save_all")
    def test_create_reservation_success(self, mock_save, mock_hotel_res, mock_cust_get, mock_res_get):
        """Test successful reservation creation."""
        mock_cust_get.return_value = [Customer(1, "John", "email")]
        result = Reservation.create_reservation(100, 1, 10)
        self.assertTrue(result)

    @patch("src.reservation.Reservation.get_all", return_value=[])
    @patch("src.customer.Customer.get_all", return_value=[])
    def test_create_reservation_no_customer(self, mock_cust_get, mock_res_get):
        """Test negative case: customer does not exist."""
        # Customer get_all returns empty, so customer 1 doesn't exist
        result = Reservation.create_reservation(100, 1, 10)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()