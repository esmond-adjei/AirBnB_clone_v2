#!/usr/bin/python3
"""Test cases for the Review class"""
import os
import unittest
from models.base_model import BaseModel
from models.review import Review


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "test only for FileStorage")
class TestReview(unittest.TestCase):
    """Test cases for the Review class"""

    def test_inheritance(self):
        """Test that Review inherits from BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)

    def test_attributes_db(self):
        """Test the attributes of the Review class in db mode"""
        review = Review()
        self.assertTrue(hasattr(review, 'text'))
        self.assertTrue(hasattr(review, 'place_id'))
        self.assertTrue(hasattr(review, 'user_id'))

    def test_attributes_file(self):
        """Test the attributes of the Review class in file mode"""
        review = Review()
        self.assertTrue(hasattr(review, 'text'))
        self.assertTrue(hasattr(review, 'place_id'))
        self.assertTrue(hasattr(review, 'user_id'))

    def test_init(self):
        """Test the initialization of a Review instance"""
        review = Review(text="Great place",
                        place_id="place123", user_id="user456")
        self.assertEqual(review.text, "Great place")
        self.assertEqual(review.place_id, "place123")
        self.assertEqual(review.user_id, "user456")

    def test_str_representation(self):
        """Test the string representation of a Review instance"""
        review = Review(text="Great place",
                        place_id="place123", user_id="user456")
        string = str(review)
        self.assertIn("[Review] ({})".format(review.id), string)
        self.assertIn("'text': 'Great place'", string)
        self.assertIn("'place_id': 'place123'", string)
        self.assertIn("'user_id': 'user456'", string)

    def test_attributes_default(self):
        """Test that the attributes have default values when not provided"""
        review = Review()
        self.assertEqual(review.text, "")
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")

    def test_save(self):
        """Test the save method of a Review instance"""
        review = Review(text="Great place",
                        place_id="place123", user_id="user456")
        previous_updated_at = review.updated_at
        review.save()
        self.assertNotEqual(previous_updated_at, review.updated_at)

    def test_to_dict(self):
        """Test the to_dict method of a Review instance"""
        review = Review(text="Great place",
                        place_id="place123", user_id="user456")
        dictionary = review.to_dict()
        self.assertEqual(dictionary['__class__'], 'Review')
        self.assertEqual(dictionary['id'], review.id)
        self.assertEqual(dictionary['text'], 'Great place')
        self.assertEqual(dictionary['place_id'], 'place123')
        self.assertEqual(dictionary['user_id'], 'user456')


if __name__ == '__main__':
    unittest.main()
