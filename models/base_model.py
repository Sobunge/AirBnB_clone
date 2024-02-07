#!/usr/bin/python3
import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()

        # Rearrange the keys in the dictionary
        ordered_keys = [
                'my_number', 'name', '__class__',
                'updated_at', 'id',
                'created_at'
                ]
        obj_dict_ordered = {
                key: obj_dict[key]
                for key in ordered_keys
                if key in obj_dict
        }

        return obj_dict_ordered
