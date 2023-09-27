#!/usr/bin/python3
"""
    Declaration for database storage
"""
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session, exc
import os


class DBStorage():
    """
    Database storage class
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Creates engine connection
        """
        username = os.getenv('HBNB_MYSQL_USER', default=None)
        password = os.getenv('HBNB_MYSQL_PWD', default=None)
        localhost = os.getenv('HBNB_MYSQL_HOST', default=None)
        db_name = os.getenv('HBNB_MYSQL_DB', default=None)
        con = f'mysql+mysqldb://{username}:{password}@{localhost}/{db_name}'
        self.__engine = create_engine(con, pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries current database session based on class.
        Returns a dictionary representation of the query.
        """
        result = {}
        if cls:
            objects = self.__session.query(eval(cls)).all()
        else:
            classes = [User, State, City, Amenity, Place, Review]
            objects = []
            for cls in classes:
                objects += self.__session.query(cls).all()
        for obj in objects:
            key = f"{obj.__class__.__name__}.{obj.id}"
            result[key] = obj
        return result

    def new(self, obj):
        """
        Adds the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and creates a new session
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """
        Closes the session
        """
        self.__session.remove()
