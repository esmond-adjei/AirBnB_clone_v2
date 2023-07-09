#!/usr/bin/python3
"""Test cases for the baseModel class"""
import os
import unittest
from models.base_model import BaseModel
from datetime import datetime


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "test only for FileStorage")
class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def test_init(self):
        """Test the initialization of a BaseModel instance"""
        base_model = BaseModel()
        self.assertTrue(hasattr(base_model, 'id'))
        self.assertTrue(hasattr(base_model, 'created_at'))
        self.assertTrue(hasattr(base_model, 'updated_at'))
        self.assertIsInstance(base_model.id, str)
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)

    def test_str_representation(self):
        """Test the string representation of a BaseModel instance"""
        base_model = BaseModel()
        string = str(base_model)
        self.assertIn("[BaseModel] ({})".format(base_model.id), string)
        self.assertIn("'id': '{}'".format(base_model.id), string)
        self.assertIn("'created_at': {}".format(
            repr(base_model.created_at)), string)
        self.assertIn("'updated_at': {}".format(
            repr(base_model.updated_at)), string)

    def test_save(self):
        """Test the save method of a BaseModel instance"""
        base_model = BaseModel()
        previous_updated_at = base_model.updated_at
        base_model.save()
        self.assertNotEqual(previous_updated_at, base_model.updated_at)

    def test_to_dict(self):
        """Test the to_dict method of a BaseModel instance"""
        base_model = BaseModel()
        dictionary = base_model.to_dict()
        self.assertEqual(dictionary['__class__'], 'BaseModel')
        self.assertEqual(dictionary['id'], base_model.id)
        self.assertEqual(dictionary['created_at'],
                         base_model.created_at.isoformat())
        self.assertEqual(dictionary['updated_at'],
                         base_model.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
