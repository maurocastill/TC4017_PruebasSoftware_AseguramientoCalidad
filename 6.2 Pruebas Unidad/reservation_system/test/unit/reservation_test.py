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
    def test_create_reservation_success(
        self, _mock_save, _mock_hotel_res, mock_cust_get, _mock_res_get
            ):
        """Test successful reservation creation."""
        mock_cust_get.return_value = [Customer(1, "John", "john@email.com")]
        result = Reservation.create_reservation(100, 1, 10)
        self.assertTrue(result)

    @patch("src.reservation.Reservation.get_all", return_value=[])
    @patch("src.customer.Customer.get_all", return_value=[])
    def test_create_reservation_no_customer(
        self, _mock_cust_get, _mock_res_get
            ):
        # unused-arguments is needed for the patch but not used by linter,
        # so it is prefix with _ to avoid warnings.
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
    def test_cancel_reservation(self, _mock_save, mock_hotel_cancel, mock_get):
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

    @patch("os.path.exists", return_value=False)
    def test_get_all_file_not_exists(self, _mock_exists):
        """Test get_all when file does not exist."""
        self.assertEqual(Reservation.get_all(), [])

    @patch("builtins.open", side_effect=IOError)
    @patch("os.path.exists", return_value=True)
    def test_get_all_io_error(self, _mock_exists, _mock_file):
        """Test get_all handles IOError."""
        self.assertEqual(Reservation.get_all(), [])

    @patch("builtins.open", side_effect=IOError)
    @patch("os.makedirs")
    def test_save_all_io_error(self, _mock_makedirs, _mock_file):
        """Test save_all handles IOError."""
        try:
            Reservation.save_all([self.reservation])
        except Exception:  # pylint: disable=broad-exception-caught
            self.fail("save_all raised Exception unexpectedly on IOError")

    @patch("src.reservation.Reservation.get_all")
    def test_create_duplicate_reservation(self, mock_get):
        """Test create_reservation with duplicate ID."""
        mock_get.return_value = [self.reservation]
        self.assertFalse(Reservation.create_reservation(100, 1, 10))

    @patch("src.reservation.Reservation.get_all", return_value=[])
    @patch("src.customer.Customer.get_all")
    @patch("src.hotel.Hotel.reserve_room", return_value=False)
    def test_create_reservation_hotel_fails(
        self, _mock_hotel, mock_cust_get, _mock_res_get
    ):
        """Test create_reservation when hotel reservation fails."""
        mock_cust_get.return_value = [Customer(1, "John", "john@email.com")]
        self.assertFalse(Reservation.create_reservation(101, 1, 10))

    @patch("src.reservation.Reservation.get_all", return_value=[])
    def test_cancel_non_existent_reservation(self, _mock_get):
        """Test cancel_reservation with non-existent ID."""
        self.assertFalse(Reservation.cancel_reservation(999))


if __name__ == "__main__":
    unittest.main()
