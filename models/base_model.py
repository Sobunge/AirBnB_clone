#!/usr/bin/python3
""" A Base model class """
import uuid
from datetime import datetime


class BaseModel:
    """A class that defines common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Initialize the BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key,
                            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                elif key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Return a string representation of the BaseModel instance."""
        return "[{}] ({}) {}".format(
                type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update the updated_at with the current datetime."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Return a dictionary containing all keys/values of __dict__ """
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = type(self).__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict
