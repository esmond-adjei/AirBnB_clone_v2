#!/usr/bin/python3
""" Place Module for HBNB project """
import os
import models
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, Integer, Float, Table

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_assoc_table = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60), ForeignKey(
                                  'places.id'), nullable=False),
                              Column('amenity_id', String(60), ForeignKey(
                                  'amenities.id'), nullable=False)
                              )


class Place(BaseModel, Base):
    """Representation of Place """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review",
                               backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity",
                                 secondary=place_assoc_table,
                                 viewonly=False)

    else:
        """ A place to stay """
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        reviews = []
        amenity_ids = []

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """
                Sets the amenities ids to a list
            """
            self.amenity_ids = obj.id
            if obj.__class__.__name__ != "Amenity":
                return
            amenity_dict = models.storage.all(obj)
            for val in amenity_dict.values():
                if self.id == val.place_id:
                    self.amenity_ids.append(val.id)

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
