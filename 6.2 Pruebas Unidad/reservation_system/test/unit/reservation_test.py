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
        mock_cust_get.return_value = [Customer(1, "John", "john@email.com")]
        result = Reservation.create_reservation(100, 1, 10)
        self.assertTrue(result)

    @patch("src.reservation.Reservation.get_all", return_value=[])
    @patch("src.customer.Customer.get_all", return_value=[])
    def test_create_reservation_no_customer(self, mock_cust_get, mock_res_get):
        """Test negative case: customer does not exist."""
        # Customer get_all returns empty, so customer 1 doesn't exist
        result = Reservation.create_reservation(100, 1, 10)
        self.assertFalse(result)
    
    def setUp(self):
        """Initialize test data."""
        self.reservation = Reservation(100, 1, 10)

    def test_to_dict(self):
        """Test dictionary serialization."""
        self.assertEqual(self.reservation.to_dict()['customer_id'], 1)

    @patch("src.reservation.Reservation.get_all")
    @patch("src.hotel.Hotel.cancel_reservation", return_value=True)
    @patch("src.reservation.Reservation.save_all")
    def test_cancel_reservation(self, mock_save, mock_hotel_cancel, mock_get):
        """Test cancelling a reservation."""
        mock_get.return_value = [self.reservation]
        result = Reservation.cancel_reservation(100)
        self.assertTrue(result)
        self.assertTrue(mock_hotel_cancel.called)
    
    def test_invalid_ids_in_reservation(self):
        """Test that invalid IDs in reservation raise ValueError."""
        # Invalid reservation ID
        self.assertRaises(ValueError, Reservation, "RES1", 1, 10)
        # Invalid customer ID
        self.assertRaises(ValueError, Reservation, 100, "CUST", 10)
        # Invalid hotel ID
        self.assertRaises(ValueError, Reservation, 100, 1, -5)

if __name__ == "__main__":
    unittest.main()