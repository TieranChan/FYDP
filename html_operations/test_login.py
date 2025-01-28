
import tkinter as tk
from unittest.mock import patch, MagicMock
from admin_login import *
import unittest

"""
Unit tests for everything to do with test_login (non-GUI wise)
"""
class TestLogin(unittest.TestCase):
    def setUp(self):
        """Set up the Tkinter root and initialize widgets."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window during testing

    def tearDown(self):
        """Destroy the Tkinter root after testing."""
        self.root.destroy()

    """
    Testing trying to connect to the MYSQL Database
    """

    @patch("mysql.connector.connect")
    def test_validate_and_connect_success(self, mock_connect):
        """Test successful MySQL connection with valid credentials."""
        mock_connect.return_value = MagicMock()  # Mock successful connection
        result = validate_and_connect("test_user", "test_pass")
        self.assertEqual(result, "Success")

    @patch("mysql.connector.connect")
    def test_validate_and_connect_failure(self, mock_connect):
        mock_connect.side_effect = mysql.connector.Error("Access denied")
        result = validate_and_connect("invalid_user", "wrong_pass")
        self.assertTrue("Login Failed" in result)
    
    def test_validate_and_connect_empty_credentials(self):
        result = validate_and_connect("", "")
        self.assertEqual(result, "Both username and password are required!")
 



if __name__ == '__main__':
    unittest.main()
