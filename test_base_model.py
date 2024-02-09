#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""

import models

BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__
my_model = BaseModel()
my_model.name = "My First Model"
my_model.my_number = 89
print(my_model)
my_model.save()
print(my_model)
my_model_json = my_model.to_dict()
print(my_model_json)
print("JSON of my_model:")
for key in my_model_json.keys():
    value = my_model_json[key]
    type_value = type(value)
    print("\t{}: ({}) - {}".format(key, type_value, value))
