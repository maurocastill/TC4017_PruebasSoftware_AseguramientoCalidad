"""Unit tests for Customer class."""
import unittest
from unittest.mock import patch
from src.customer import Customer

class TestCustomer(unittest.TestCase):
    """Test cases for Customer functionality."""

    def setUp(self):
        """Initialize test data."""
        self.customer = Customer(1, "John Doe", "john@email.com")

    @patch("src.customer.Customer.get_all", return_value=[])
    @patch("src.customer.Customer.save_all")
    def test_create_customer(self, mock_save, mock_get):
        """Test successful customer creation."""
        result = Customer.create_customer(1, "John Doe", "john@email.com")
        self.assertTrue(result)
        self.assertTrue(mock_save.called)

    @patch("src.customer.Customer.get_all")
    def test_create_duplicate_customer(self, mock_get):
        """Test negative case: duplicate customer ID."""
        mock_get.return_value = [self.customer]
        result = Customer.create_customer(1, "Jane", "jane@email.com")
        self.assertFalse(result)

    @patch("src.customer.Customer.get_all")
    @patch("src.customer.Customer.save_all")
    def test_delete_customer(self, mock_save, mock_get):
        """Test customer deletion."""
        mock_get.return_value = [self.customer]
        result = Customer.delete_customer(1)
        self.assertTrue(result)
    
    def test_to_dict(self):
        """Test dictionary serialization."""
        self.assertEqual(self.customer.to_dict()['name'], "John Doe")

    @patch("src.customer.Customer.get_all")
    @patch("src.customer.Customer.save_all")
    def test_modify_customer(self, mock_save, mock_get):
        """Test modifying customer attributes."""
        mock_get.return_value = [self.customer]
        result = Customer.modify_customer(1, name="Jane Doe")
        self.assertTrue(result)
        self.assertEqual(self.customer.name, "Jane Doe")
        
if __name__ == "__main__":
    unittest.main()