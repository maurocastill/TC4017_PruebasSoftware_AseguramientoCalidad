import unittest
from src.hotel import Hotel

class TestHotel(unittest.TestCase):
    """
    Unit tests for the Hotel class.
    """

    def setUp(self):
        """
        Set up a valid Hotel instance for testing.
        """
        self.hotel = Hotel(1, "Grand Hotel", "Bogota", 100)

    def test_hotel_initialization(self):
        """
        Test that the hotel is initialized with correct values.
        """
        self.assertEqual(self.hotel.name, "Grand Hotel")
        self.assertEqual(self.hotel.city, "Bogota")
        self.assertEqual(self.hotel.rooms, 100)

    def test_modify_info(self):
        """
        Test that hotel attributes can be modified.
        """
        self.hotel.modify_info(name="Updated Name", city="Medellin")
        self.assertEqual(self.hotel.name, "Updated Name")
        self.assertEqual(self.hotel.city, "Medellin")
        # Ensure rooms didn't change because we didn't pass it
        self.assertEqual(self.hotel.rooms, 100)

if __name__ == '__main__':
    unittest.main()