"""Module for Customer class definition and management."""
import json
import os

class Customer:
    """Represents a Customer entity in the system."""
    FILE_PATH = 'data/customers.json'

    def __init__(self, customer_id, name, email):
        # Validation for customer attributes, ensuring data integrity.
        # customer_id must be a positive integer, email must contain '@', 
        # and name cannot be empty.
        if not isinstance(customer_id, int) or customer_id <= 0:
            raise ValueError("Customer ID must be a positive integer.")
        if not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid email format.")
        if not name:
            raise ValueError("Name cannot be empty.")
            
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Returns dictionary representation of the customer."""
        return self.__dict__

    @classmethod
    def get_all(cls):
        """Retrieves all customers from the JSON file."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, 'r', encoding='utf-8') as file:
                return [cls(**data) for data in json.load(file)]
        except (json.JSONDecodeError, IOError):
            return []

    @classmethod
    def save_all(cls, customers):
        """Saves a list of Customer instances to the JSON file."""
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)
        try:
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump([c.to_dict() for c in customers], file, indent=4)
        except IOError:
            pass

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Creates a new customer."""
        customers = cls.get_all()
        if any(c.customer_id == customer_id for c in customers):
            print(f"Error: Customer ID {customer_id} already exists.")
            return False
            
        try:
            new_customer = cls(customer_id, name, email)
        except ValueError as error:
            print(f"Validation Error: {error}")
            return False

        customers.append(new_customer)
        cls.save_all(customers)
        return True

    @classmethod
    def delete_customer(cls, customer_id):
        """Deletes a customer by ID."""
        customers = cls.get_all()
        initial_count = len(customers)
        customers = [c for c in customers if c.customer_id != customer_id]
        if len(customers) < initial_count:
            cls.save_all(customers)
            return True
        return False

    @classmethod
    def modify_customer(cls, customer_id, name=None, email=None):
        """Modifies customer info."""
        customers = cls.get_all()
        for c in customers:
            if c.customer_id == customer_id:
                if name:
                    c.name = name
                if email and "@" in email:
                    c.email = email
                cls.save_all(customers)
                return True
        return False