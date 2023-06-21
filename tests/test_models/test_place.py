#!/usr/bin/python3
"""Test cases for the Place class"""
import os
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models.place import Place


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "test only for FileStorage")
class TestPlace(unittest.TestCase):
    """Test cases for the Place class"""

    def test_inheritance(self):
        """Test that Place inherits from BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)

    def test_attributes_db(self):
        """Test the attributes of the Place class in db mode"""
        place = Place()
        self.assertTrue(hasattr(place, 'city_id'))
        self.assertTrue(hasattr(place, 'user_id'))
        self.assertTrue(hasattr(place, 'name'))
        self.assertTrue(hasattr(place, 'description'))
        self.assertTrue(hasattr(place, 'number_rooms'))
        self.assertTrue(hasattr(place, 'number_bathrooms'))
        self.assertTrue(hasattr(place, 'max_guest'))
        self.assertTrue(hasattr(place, 'price_by_night'))
        self.assertTrue(hasattr(place, 'latitude'))
        self.assertTrue(hasattr(place, 'longitude'))
        self.assertTrue(hasattr(place, 'reviews'))
        self.assertTrue(hasattr(place, 'amenities'))

    def test_attributes_file(self):
        """Test the attributes of the Place class in file mode"""
        place = Place()
        self.assertTrue(hasattr(place, 'city_id'))
        self.assertTrue(hasattr(place, 'user_id'))
        self.assertTrue(hasattr(place, 'name'))
        self.assertTrue(hasattr(place, 'description'))
        self.assertTrue(hasattr(place, 'number_rooms'))
        self.assertTrue(hasattr(place, 'number_bathrooms'))
        self.assertTrue(hasattr(place, 'max_guest'))
        self.assertTrue(hasattr(place, 'price_by_night'))
        self.assertTrue(hasattr(place, 'latitude'))
        self.assertTrue(hasattr(place, 'longitude'))
        self.assertTrue(hasattr(place, 'amenity_ids'))

    def test_init(self):
        """Test the initialization of a Place instance"""
        place = Place(name="Cozy House", city_id="city123", user_id="user456")
        self.assertEqual(place.name, "Cozy House")
        self.assertEqual(place.city_id, "city123")
        self.assertEqual(place.user_id, "user456")

    def test_str_representation(self):
        """Test the string representation of a Place instance"""
        place = Place(name="Cozy House", city_id="city123", user_id="user456")
        string = str(place)
        self.assertIn("[Place] ({})".format(place.id), string)
        self.assertIn("'name': 'Cozy House'", string)
        self.assertIn("'city_id': 'city123'", string)
        self.assertIn("'user_id': 'user456'", string)

    def test_attributes_default(self):
        """Test that the attributes have default values when not provided"""
        place = Place()
        self.assertEqual(place.name, "")
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)

    def test_amenities_property(self):
        """Test the amenities property getter and setter"""
        place = Place()
        self.assertEqual(place.amenities, [])
        amenity = Amenity()
        place.amenities = amenity  # "123"
        self.assertEqual(place.amenities, amenity.id)

    def test_amenities_property_file_mode(self):
        """Test the amenities property in file mode"""
        place = Place()
        amenity = Amenity(name="Wifi")
        place.amenities = amenity
        self.assertEqual(place.amenity_ids, amenity.id)

    def test_save(self):
        """Test the save method of a Place instance"""
        place = Place(name="Cozy House", city_id="city123", user_id="user456")
        previous_updated_at = place.updated_at
        place.save()
        self.assertNotEqual(previous_updated_at, place.updated_at)

    def test_to_dict(self):
        """Test the to_dict method of a Place instance"""
        place = Place(name="Cozy House", city_id="city123", user_id="user456")
        dictionary = place.to_dict()
        self.assertEqual(dictionary['__class__'], 'Place')
        self.assertEqual(dictionary['id'], place.id)
        self.assertEqual(dictionary['name'], 'Cozy House')
        self.assertEqual(dictionary['city_id'], 'city123')
        self.assertEqual(dictionary['user_id'], 'user456')


if __name__ == '__main__':
    unittest.main()
