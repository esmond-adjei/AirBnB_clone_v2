#!/usr/bin/python3
"""
    Declaration for database storage
"""
from sqlalchemy import create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
    """
    Database storage class
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Creates engine connection
        """
        username = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', default='localhost')
        db_name = os.getenv('HBNB_MYSQL_DB')
        connection = f'mysql+mysqldb://{username}:{password}@{host}/{db_name}'
        self.__engine = create_engine(connection, pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries current database session based on class.
        Returns a dictionary representation of the query.
        """
        new_dict = {}
        if cls is None:
            classes = [User, State, City, Amenity, Place, Review]
            for cls in classes:
                query = self.__session.query(cls).all()
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        else:
            query = self.__session.query(eval(cls)).all()
            for obj in query:
                key = f"{obj.__class__.__name__}.{obj.id}"
                new_dict[key] = obj
        return new_dict

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
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Closes the current session
        """
        self.__session.close()
