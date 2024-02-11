#!/usr/bin/python3

import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""

    def test_attributes(self):
        """Test initialization of BaseModel attributes."""
        model = BaseModel()
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_str_method(self):
        """Test __str__ method."""
        model = BaseModel()
        expected_str = f"[BaseModel] ({model.id}) {model.__dict__}"
        self.assertEqual(str(model), expected_str)

    def test_save_method(self):
        """Test save method."""
        model = BaseModel()
        prev_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(prev_updated_at, model.updated_at)

    def test_to_dict_method(self):
        """Test to_dict method."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('__class__', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    def test_kwargs_initialization(self):
        """Test initialization of BaseModel with kwargs."""
        kwargs = {
            'id': '1234',
            'created_at': '2022-02-10T12:00:00.000000',
            'updated_at': '2022-02-10T12:00:00.000000',
            'name': 'TestModel'
        }
        model = BaseModel(**kwargs)
        self.assertEqual(model.id, '1234')
        self.assertEqual(model.created_at,
                         datetime.strptime('2022-02-10T12:00:00.000000',
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(model.updated_at,
                         datetime.strptime('2022-02-10T12:00:00.000000',
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(model.name, 'TestModel')


if __name__ == '__main__':
    unittest.main()
