#!/usr/bin/python3
"""
Contains class BaseModel
"""

#!/usr/bin/python3
import uuid
from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


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
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        obj_dict = self.__dict__.copy()
        if "created_at" in obj_dict:
            obj_dict["created_at"] = obj_dict["created_at"].strftime(time)
        if "updated_at" in obj_dict:
           obj_dict["updated_at"] = obj_dict["updated_at"].strftime(time)
        obj_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in obj_dict:
            del obj_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in obj_dict:
                del obj_dict["password"]
        return obj_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)

        # Rearrange the keys in the dictionary
        ordered_keys = ['my_number', 'name', '__class__', 'updated_at', 'id', 'created_at']
        obj_dict_ordered = {key: obj_dict[key] for key in ordered_keys if key in obj_dict}

        return obj_dict_ordered
