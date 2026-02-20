"""Module for Reservation class definition and management."""
import json
import os
from src.hotel import Hotel
from src.customer import Customer


class Reservation:
    """Represents a Reservation linking Customer and Hotel."""
    FILE_PATH = 'data/reservations.json'

    def __init__(self, reservation_id, customer_id, hotel_id):
        # Validation for reservation attributes, ensuring data integrity.
        # reservation_id, customer_id, and hotel_id must be positive integers.
        if not isinstance(reservation_id, int) or reservation_id <= 0:
            raise ValueError("Reservation ID must be a positive integer.")
        if not isinstance(customer_id, int) or customer_id <= 0:
            raise ValueError("Customer ID must be a positive integer.")
        if not isinstance(hotel_id, int) or hotel_id <= 0:
            raise ValueError("Hotel ID must be a positive integer.")

        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Returns dictionary representation."""
        return self.__dict__

    @classmethod
    def get_all(cls):
        """Retrieves all reservations."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, 'r', encoding='utf-8') as file:
                return [cls(**data) for data in json.load(file)]
        except (json.JSONDecodeError, IOError):
            return []

    @classmethod
    def save_all(cls, reservations):
        """Saves reservations to file."""
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)
        try:
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump([r.to_dict() for r in reservations], file, indent=4)
        except IOError:
            pass

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        """Creates a reservation if validations pass."""
        reservations = cls.get_all()
        if any(r.reservation_id == reservation_id for r in reservations):
            print("Error: Reservation ID already exists.")
            return False

        # Validations
        customers = Customer.get_all()
        if not any(c.customer_id == customer_id for c in customers):
            print("Error: Customer not found.")
            return False

        if Hotel.reserve_room(hotel_id):
            reservations.append(cls(reservation_id, customer_id, hotel_id))
            cls.save_all(reservations)
            return True
        return False

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancels a reservation and frees the room."""
        reservations = cls.get_all()
        for reservation in reservations:
            if reservation.reservation_id == reservation_id:
                Hotel.cancel_reservation(reservation.hotel_id)
                reservations.remove(reservation)
                cls.save_all(reservations)
                return True
        return False
