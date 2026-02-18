"""
Module for Reservation class definition.
"""

class Reservation:
    """
    Represents a Reservation linking a Customer and a Hotel.
    """
    def __init__(self, reservation_id, customer_id, hotel_id):
        """
        Initialize a Reservation instance.
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def cancel(self):
        """
        Placeholder for cancel logic.
        """
        return f"Reservation {self.reservation_id} cancelled."