"""
Module for Customer class definition.
"""

class Customer:
    """
    Represents a Customer entity in the system.
    """
    def __init__(self, customer_id, name, email):
        """
        Initialize a Customer instance.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def display_info(self):
        """
        Returns a string representation of the customer.
        """
        return f"Customer: {self.name} (ID: {self.customer_id}), Email: {self.email}"

    def modify_info(self, name=None, email=None):
        """
        Updates customer attributes if new values are provided.
        """
        if name:
            self.name = name
        if email:
            self.email = email