import json
import os

class Hotel:
    FILE_PATH = 'data/hotels.json'

    def __init__(self, hotel_id, name, city, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.city = city
        self.rooms = rooms

    def to_dict(self):
        """Serialize object to dictionary."""
        return self.__dict__

    @classmethod
    def get_all(cls):
        """Retrieve all hotels from file."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, 'r', encoding='utf-8') as file:
                return [cls(**data) for data in json.load(file)]
        except (json.JSONDecodeError, IOError) as error:
            print(f"Error loading hotels: {error}")
            return []

    @classmethod
    def save_all(cls, hotels):
        """Save list of hotels to file."""
        try:
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump([hotel.to_dict() for hotel in hotels], file, indent=4)
        except IOError as error:
            print(f"Error saving hotels: {error}")

    @classmethod
    def create_hotel(cls, hotel):
        """Adds a new hotel to persistence."""
        hotels = cls.get_all()
        # Check for duplicates (simple check by ID)
        if any(h.hotel_id == hotel.hotel_id for h in hotels):
            print(f"Error: Hotel ID {hotel.hotel_id} already exists.")
            return
        hotels.append(hotel)
        cls.save_all(hotels)
        print(f"Hotel {hotel.name} created.")

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Deletes a hotel by ID."""
        hotels = cls.get_all()
        hotels = [h for h in hotels if h.hotel_id != hotel_id]
        cls.save_all(hotels)
        print(f"Hotel {hotel_id} deleted.")