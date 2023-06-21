#!/usr/bin/python3
"""Test cases for the City class"""
import os
import unittest
from models.base_model import BaseModel
from models.city import City


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "test only for FileStorage")
class TestCity(unittest.TestCase):
    """Test cases for the City class"""

    def test_inheritance(self):
        """Test that City inherits from BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)

    def test_attributes(self):
        """Test the attributes of the City class"""
        city = City()
        self.assertTrue(hasattr(city, 'state_id'))
        self.assertTrue(hasattr(city, 'name'))
        self.assertEqual(city.state_id, "")
        self.assertEqual(city.name, "")

    def test_init(self):
        """Test the initialization of a City instance"""
        city = City(name="San Francisco", state_id="CA")
        self.assertEqual(city.name, "San Francisco")
        self.assertEqual(city.state_id, "CA")

    def test_str_representation(self):
        """Test the string representation of a City instance"""
        city = City(name="San Francisco", state_id="CA")
        string = str(city)
        self.assertIn("[City] ({})".format(city.id), string)
        self.assertIn("'name': 'San Francisco'", string)
        self.assertIn("'state_id': 'CA'", string)

    def test_attributes_default(self):
        """Test that the attributes have default values when not provided"""
        city = City()
        self.assertEqual(city.name, "")
        self.assertEqual(city.state_id, "")

    def test_save(self):
        """Test the save method of a City instance"""
        city = City(name="San Francisco", state_id="CA")
        previous_updated_at = city.updated_at
        city.save()
        self.assertNotEqual(previous_updated_at, city.updated_at)

    def test_to_dict(self):
        """Test the to_dict method of a City instance"""
        city = City(name="San Francisco", state_id="CA")
        dictionary = city.to_dict()
        self.assertEqual(dictionary['__class__'], 'City')
        self.assertEqual(dictionary['id'], city.id)
        self.assertEqual(dictionary['name'], 'San Francisco')
        self.assertEqual(dictionary['state_id'], 'CA')


if __name__ == '__main__':
    unittest.main()
