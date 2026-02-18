"""Unit tests for Hotel class."""
import unittest
from unittest.mock import patch, mock_open
import json
from src.hotel import Hotel

class TestHotel(unittest.TestCase):
    """Test cases for Hotel functionality."""

    def setUp(self):
        """Initialize test data."""
        self.hotel = Hotel(1, "Test", "City", 10)

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("os.path.exists", return_value=True)
    def test_get_all_empty(self, mock_exists, mock_file):
        """Test reading empty hotel list."""
        self.assertEqual(Hotel.get_all(), [])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    @patch("os.path.exists", return_value=True)
    def test_get_all_corrupt_json(self, mock_exists, mock_file):
        """Test negative case: handling JSONDecodeError."""
        self.assertEqual(Hotel.get_all(), [])

    @patch("src.hotel.Hotel.get_all", return_value=[])
    @patch("src.hotel.Hotel.save_all")
    def test_create_hotel_success(self, mock_save, mock_get):
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
    def test_reserve_room_success(self, mock_save, mock_get):
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

if __name__ == "__main__":
    unittest.main()