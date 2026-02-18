"""
Module for Hotel class definition.
"""

class Hotel:
    """
    Represents a Hotel entity in the system.
    """
    def __init__(self, hotel_id, name, city, rooms):
        """
        Initialize a Hotel instance.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.city = city
        self.rooms = rooms

    def display_info(self):
        """
        Returns a string representation of the hotel.
        """
        return f"Hotel: {self.name} (ID: {self.hotel_id}) in {self.city}"

    def modify_info(self, name=None, city=None, rooms=None):
        """
        Updates hotel attributes if new values are provided.
        """
        if name:
            self.name = name
        if city:
            self.city = city
        if rooms:
            self.rooms = rooms