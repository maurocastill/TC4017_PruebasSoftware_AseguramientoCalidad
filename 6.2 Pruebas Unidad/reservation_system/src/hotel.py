"""Module for Hotel class definition and management."""
import json
import os


class Hotel:
    """Represents a Hotel entity in the system."""
    FILE_PATH = 'data/hotels.json'

    def __init__(self, hotel_id, name, city, rooms, available_rooms=None):
        # pylint: disable=too-many-arguments, too-many-positional-arguments.
        # Validation for hotel attributes, ensuring data integrity.
        # hotel_id must be a positive integer, rooms must be a non-negative
        # integer and name/city cannot be empty.
        if not isinstance(hotel_id, int) or hotel_id <= 0:
            raise ValueError("Hotel ID must be a positive integer.")
        if not isinstance(rooms, int) or rooms < 0:
            raise ValueError("Rooms must be a positive integer.")
        if not name or not city:
            raise ValueError("Name and city cannot be empty.")

        self.hotel_id = hotel_id
        self.name = name
        self.city = city
        self.rooms = rooms
        self.available_rooms = (
            available_rooms if available_rooms is not None else rooms
        )

    def to_dict(self):
        """Returns dictionary representation of the hotel."""
        return self.__dict__

    @classmethod
    def get_all(cls):
        """Retrieves all hotels from the JSON file."""
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
        """Saves a list of Hotel instances to the JSON file."""
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)
        try:
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump([h.to_dict() for h in hotels], file, indent=4)
        except IOError as error:
            print(f"Error saving hotels: {error}")

    @classmethod
    def create_hotel(cls, hotel_id, name, city, rooms):
        """Creates a new hotel and saves it."""
        hotels = cls.get_all()
        if any(h.hotel_id == hotel_id for h in hotels):
            print(f"Error: Hotel ID {hotel_id} already exists.")
            return False

        try:
            new_hotel = cls(hotel_id, name, city, rooms)
        except ValueError as error:
            print(f"Validation Error: {error}")
            return False

        hotels.append(new_hotel)
        cls.save_all(hotels)
        return True

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Deletes a hotel by its ID."""
        hotels = cls.get_all()
        initial_count = len(hotels)
        hotels = [h for h in hotels if h.hotel_id != hotel_id]
        if len(hotels) < initial_count:
            cls.save_all(hotels)
            return True
        return False

    @classmethod
    def modify_hotel(cls, hotel_id, name=None, city=None):
        """Modifies a hotel's basic information."""
        hotels = cls.get_all()
        for h in hotels:
            if h.hotel_id == hotel_id:
                if name:
                    h.name = name
                if city:
                    h.city = city
                cls.save_all(hotels)
                return True
        return False

    @classmethod
    def reserve_room(cls, hotel_id):
        """Decreases available rooms by 1 if possible."""
        hotels = cls.get_all()
        for h in hotels:
            if h.hotel_id == hotel_id:
                if h.available_rooms > 0:
                    h.available_rooms -= 1
                    cls.save_all(hotels)
                    return True
                print(f"Error: No available rooms in hotel {hotel_id}.")
                return False
        return False

    @classmethod
    def cancel_reservation(cls, hotel_id):
        """Increases available rooms by 1."""
        hotels = cls.get_all()
        for h in hotels:
            if h.hotel_id == hotel_id:
                if h.available_rooms < h.rooms:
                    h.available_rooms += 1
                    cls.save_all(hotels)
                    return True
        return False
