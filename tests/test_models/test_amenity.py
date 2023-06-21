#!/usr/bin/python3
"""Tests for `amenity` model"""
import os
import unittest
from models.amenity import Amenity


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "test only for FileStorage")
class TestAmenity(unittest.TestCase):
    def test_attributes(self):
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'name'))
        self.assertEqual(amenity.name, "")

    def test_init(self):
        amenity = Amenity(name="Swimming Pool")
        self.assertEqual(amenity.name, "Swimming Pool")
        self.assertEqual(amenity.__class__.__name__, "Amenity")
        self.assertTrue(hasattr(amenity, 'id'))
        self.assertTrue(hasattr(amenity, 'created_at'))
        self.assertTrue(hasattr(amenity, 'updated_at'))

    def test_str_representation(self):
        amenity = Amenity(name="Peter")
        string = str(amenity)
        self.assertIn("[Amenity] ({})".format(amenity.id), string)
        self.assertIn("'name': 'Peter'", string)


if __name__ == '__main__':
    unittest.main()
