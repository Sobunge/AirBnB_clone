#!/usr/bin/python3
""" A test state module"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """ Declaring a test state class """

    def __init__(self, *args, **kwargs):
        """ Declaring a constructor"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ Declaring the test for name"""
        new = self.value()
        self.assertEqual(type(new.name), str)
