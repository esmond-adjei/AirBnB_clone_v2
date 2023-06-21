#!/usr/bin/python3
"""Test cases for the User class"""
import os
import unittest
from models.base_model import BaseModel
from models.user import User
from hashlib import md5


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "test only for FileStorage")
class TestUser(unittest.TestCase):
    """Test cases for the User class"""

    def test_inheritance(self):
        """Test that User inherits from BaseModel"""
        user = User()
        self.assertIsInstance(user, BaseModel)

    def test_attributes_db(self):
        """Test the attributes of the User class in db mode"""
        user = User()
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))
        self.assertTrue(hasattr(user, 'places'))
        self.assertTrue(hasattr(user, 'reviews'))

    def test_attributes_file(self):
        """Test the attributes of the User class in file mode"""
        user = User()
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))

    def test_init(self):
        """Test the initialization of a User instance"""
        user = User(email="test@example.com", password="password")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, md5("password".encode()).hexdigest())

    def test_str_representation(self):
        """Test the string representation of a User instance"""
        user = User(email="test@example.com", password="password")
        string = str(user)
        self.assertIn("[User] ({})".format(user.id), string)
        self.assertIn("'email': 'test@example.com'", string)

    def test_password_encryption(self):
        """Test that the password is encrypted with md5"""
        password = "password"
        user = User(password=password)
        self.assertEqual(user.password, md5(password.encode()).hexdigest())

    def test_attributes_default(self):
        """Test that the attributes have default values when not provided"""
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_setattr_password(self):
        """Test the __setattr__ method for the 'password' attribute"""
        user = User()
        password = "password"
        user.password = password
        self.assertEqual(user.password, md5(password.encode()).hexdigest())


if __name__ == '__main__':
    unittest.main()
