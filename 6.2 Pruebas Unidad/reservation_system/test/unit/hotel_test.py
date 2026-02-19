"""Unit tests for Hotel class."""
import unittest
from unittest.mock import patch, mock_open
from src.hotel import Hotel


class TestHotel(unittest.TestCase):
    """Test cases for Hotel functionality."""

    def setUp(self):
        """Initialize test data."""
        self.hotel = Hotel(1, "Test", "City", 10)

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("os.path.exists", return_value=True)
    # unused-arguments is needed for the patch but not used by linter,
    # so it is prefix with _ to avoid warnings.
    def test_get_all_empty(self, _mock_exists, _mock_file):
        """Test reading empty hotel list."""
        self.assertEqual(Hotel.get_all(), [])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    @patch("os.path.exists", return_value=True)
    def test_get_all_corrupt_json(self, _mock_exists, _mock_file):
        """Test negative case: handling JSONDecodeError."""
        self.assertEqual(Hotel.get_all(), [])

    @patch("src.hotel.Hotel.get_all", return_value=[])
    @patch("src.hotel.Hotel.save_all")
    def test_create_hotel_success(self, mock_save, _mock_get):
        """Test successful hotel creation."""
        result = Hotel.create_hotel(1, "Test", "City", 10)
        self.assertTrue(result)
        self.assertTrue(mock_save.called)

    @patch("src.hotel.Hotel.get_all")
    def test_create_hotel_duplicate(self, mock_get):
        """Test negative case: duplicate hotel ID."""
        mock_get.return_value = [self.hotel]
        result = Hotel.create_hotel(1, "Another", "City", 5)
        self.assertFalse(result)

    @patch("src.hotel.Hotel.get_all")
    @patch("src.hotel.Hotel.save_all")
    def test_reserve_room_success(self, _mock_save, mock_get):
        """Test successful room reservation."""
        mock_get.return_value = [self.hotel]
        result = Hotel.reserve_room(1)
        self.assertTrue(result)
        self.assertEqual(self.hotel.available_rooms, 9)

    @patch("src.hotel.Hotel.get_all")
    def test_reserve_room_no_availability(self, mock_get):
        """Test negative case: no available rooms."""
        full_hotel = Hotel(2, "Full", "City", 10, available_rooms=0)
        mock_get.return_value = [full_hotel]
        result = Hotel.reserve_room(2)
        self.assertFalse(result)

    def test_to_dict(self):
        """Test dictionary serialization."""
        self.assertEqual(self.hotel.to_dict()['name'], "Test")

    @patch("src.hotel.Hotel.get_all")
    @patch("src.hotel.Hotel.save_all")
    def test_delete_hotel(self, mock_save, mock_get):
        """Test successful deletion of a hotel."""
        mock_get.return_value = [self.hotel]
        result = Hotel.delete_hotel(1)
        self.assertTrue(result)
        self.assertTrue(mock_save.called)

    @patch("src.hotel.Hotel.get_all")
    @patch("src.hotel.Hotel.save_all")
    def test_modify_hotel(self, _mock_save, mock_get):
        """Test modifying hotel attributes."""
        mock_get.return_value = [self.hotel]
        result = Hotel.modify_hotel(1, name="New Name")
        self.assertTrue(result)
        self.assertEqual(self.hotel.name, "New Name")

    @patch("src.hotel.Hotel.get_all")
    @patch("src.hotel.Hotel.save_all")
    def test_cancel_reservation(self, _mock_save, mock_get):
        """Test restoring available rooms upon cancellation."""
        # Simular que hay una habitación ocupada
        self.hotel.available_rooms = 9
        mock_get.return_value = [self.hotel]
        result = Hotel.cancel_reservation(1)
        self.assertTrue(result)
        self.assertEqual(self.hotel.available_rooms, 10)

    def test_invalid_rooms_type(self):
        """Test that invalid room types raise ValueError."""
        # Comprobamos que crear el hotel con "aa" lanza error directamente
        self.assertRaises(ValueError, Hotel, 2, "Test", "City", "aa")
        self.assertRaises(ValueError, Hotel, 2, "Test", "City", -5)

    @patch("src.hotel.Hotel.get_all", return_value=[])
    def test_create_hotel_invalid_data(self, _mock_get):
        """Test that create_hotel handles ValueError gracefully."""
        # Comprobamos que el método de clase atrapa el error y retorna False
        result = Hotel.create_hotel(2, "Test", "City", "aa")
        self.assertFalse(result)

    def test_invalid_hotel_id(self):
        """Test that invalid hotel ID raises ValueError."""
        self.assertRaises(ValueError, Hotel, "A", "Test", "City", 10)
        self.assertRaises(ValueError, Hotel, -1, "Test", "City", 10)

    @patch("src.hotel.Hotel.get_all")
    @patch("src.hotel.Hotel.save_all")
    def test_delete_non_existent_hotel(self, mock_save, mock_get):
        """Test negative case: attempt to delete a hotel
        that does not exist."""
        # It simulates that the database only contains hotel ID 1
        mock_get.return_value = [self.hotel]

        # Action: it attempts to delete a hotel with ID 999 (Non-existent)
        result = Hotel.delete_hotel(999)

        # Verification: The operation must fail (False)
        # and disk write (save_all) should NOT be invoked.
        self.assertFalse(result)
        self.assertFalse(mock_save.called)


if __name__ == "__main__":
    unittest.main()
