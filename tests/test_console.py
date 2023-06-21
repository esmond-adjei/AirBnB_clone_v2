#!/usr/bin/python3
"""
A unit test module for the AirBnB console.
"""
import unittest
import os
import MySQLdb
import sqlalchemy
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.user import User
from tests import clear_stream
# from models.base_model import BaseModel


class TestHBNBCommand(unittest.TestCase):
    """
    Test cases for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_create_fs(self):
        """
        Tests the `create` command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            console = HBNBCommand()
            console.onecmd('create City name="California"')
            model_id = cout.getvalue().strip()
            clear_stream(cout)

            self.assertIn('City.{}'.format(model_id), storage.all().keys())
            console.onecmd('show City {}'.format(model_id))
            self.assertIn("'name': 'California'", cout.getvalue().strip())
            clear_stream(cout)

            console.onecmd('create User name="Kwabena" age=22 height=6.1')
            model_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(model_id), storage.all().keys())
            clear_stream(cout)

            console.onecmd('show User {}'.format(model_id))
            self.assertIn("'name': 'Kwabena'", cout.getvalue().strip())
            self.assertIn("'age': 22", cout.getvalue().strip())
            self.assertIn("'height': 6.1", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_create_db(self):
        """
        Tests the `create` command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            console = HBNBCommand()
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                console.onecmd('create User')
            clear_stream(cout)

            console.onecmd(
                'create User email="kwabee02@gmail.com" password="1111"')
            model_id = cout.getvalue().strip()
            db_connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connection.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE id="{}"'.format(model_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('kwabee02@gmail.com', result)
            self.assertIn('1111', result)
            cursor.close()
            db_connection.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_show_db(self):
        """
        Tests the `show` command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            console = HBNBCommand()
            # showing a User instance
            obj = User(email="kwabee02@gmail.com", password="1111")
            db_connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connection.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            console.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            db_connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connection.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            console.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('kwabee02@gmail.com', result)
            self.assertIn('1111', result)
            self.assertIn('kwabee02@gmail.com', cout.getvalue())
            self.assertIn('1111', cout.getvalue())
            cursor.close()
            db_connection.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_count_db(self):
        """
        Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            console = HBNBCommand()
            db_connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            console.onecmd('create State name="Enugu"')
            clear_stream(cout)
            console.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            console.onecmd('count State')
            cursor.close()
            db_connection.close()


if __name__ == "__main__":
    unittest.main()
