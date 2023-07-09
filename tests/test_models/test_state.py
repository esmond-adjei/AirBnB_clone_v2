#!/usr/bin/python3
"""Test cases for the State class"""
import os
import unittest
import models
from models.base_model import BaseModel
from models.state import State
from models.city import City


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "test only for FileStorage")
class TestState(unittest.TestCase):
    """Test cases for the State class"""

    def test_inheritance(self):
        """Test that State inherits from BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)

    def test_attributes_db(self):
        """Test the attributes of the State class in db mode"""
        state = State()
        self.assertTrue(hasattr(state, 'name'))
        self.assertTrue(hasattr(state, 'cities'))

    def test_attributes_file(self):
        """Test the attributes of the State class in file mode"""
        state = State()
        self.assertTrue(hasattr(state, 'name'))
        self.assertTrue(hasattr(state, 'cities'))

    def test_init(self):
        """Test the initialization of a State instance"""
        state = State(name="California")
        self.assertEqual(state.name, "California")

    def test_str_representation(self):
        """Test the string representation of a State instance"""
        state = State(name="California")
        string = str(state)
        self.assertIn("[State] ({})".format(state.id), string)
        self.assertIn("'name': 'California'", string)

    def test_attributes_default(self):
        """Test that the attributes have default values when not provided"""
        state = State()
        self.assertEqual(state.name, "")

    def test_cities_property(self):
        """Test the cities property of a State instance"""
        state = State()
        city1 = City(state_id=state.id)
        city2 = City(state_id=state.id)
        city3 = City(state_id="different_id")

        # Add the cities to the storage
        models.storage.new(city1)
        models.storage.new(city2)
        models.storage.new(city3)
        models.storage.save()

        cities = state.cities
        self.assertEqual(len(cities), 2)
        self.assertIn(city1, cities)
        self.assertIn(city2, cities)
        self.assertNotIn(city3, cities)


if __name__ == '__main__':
    unittest.main()
