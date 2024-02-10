#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

        def __str__(self):
            """String representation of the BaseModel class"""
            created_at_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S.%f")
            updated_at_str = self.updated_at.strftime("%Y-%m-%d %H:%M:%S.%f")
            return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id,
                {
                    'id': self.id,
                    'created_at': created_at_str,
                    'updated_at': updated_at_str,
                    'name': getattr(self, 'name', None),
                    'my_number': getattr(self, 'my_number', None)
                }
            )

    def __repr__(self):
        """Return the string representation of the BaseModel object."""
        return "[{}] ({}) {}".format(
            type(self).__name__,
            self.id,
            {
                'my_number': getattr(self, 'my_number', None),
                'name': getattr(self, 'name', None),
                'updated_at': self.updated_at,
                'id': self.id,
                'created_at': self.created_at,
            }
        )

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = {
            'my_number': getattr(self, 'my_number', None),
            'name': getattr(self, 'name', None),
            '__class__': self.__class__.__name__,
            'updated_at': self.updated_at.isoformat(),
            'id': self.id,
            'created_at': self.created_at.isoformat()
        }

        if save_fs is None and hasattr(self, 'password'):
            del new_dict["password"]

        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
