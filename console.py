#!/usr/bin/python3
""" console """

import cmd
import models
from models.base_model import BaseModel
import shlex

classes = {"BaseModel": BaseModel}


class HBNBCommand(cmd.Cmd):
    """HBNH console"""

    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """Overwriting the emptyline method"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _parse_key_value_pairs(self, args):
        """Parses key-value pairs from arguments"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split('=', 1)
                value = value.strip('"')
                new_dict[key] = value
        return new_dict

    def _validate_class_instance(self, class_name, instance_id):
        """Validates class name and instance ID"""
        if class_name not in classes:
            print("** class doesn't exist **")
            return None
        key = f"{class_name}.{instance_id}"
        instance = models.storage.all().get(key)
        if not instance:
            print("** no instance found **")
            return None
        return instance

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        new_dict = self._parse_key_value_pairs(args[1:])
        instance = classes[class_name](**new_dict)
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """Prints an instance as a string based on the class name and ID"""
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        instance = self._validate_class_instance(class_name, instance_id)
        if instance:
            print(instance)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        instance = self._validate_class_instance(class_name, instance_id)
        if instance:
            del models.storage.all()[f"{class_name}.{instance_id}"]
            models.storage.save()

    def do_all(self, arg):
        """Prints all string representation of all class name"""
        args = arg.split()
        if args and args[0] not in classes:
            print("** class doesn't exist **")
            return
        if args:
            instances = [
                str(instance) for instance in models.storage.all().values()
                if type(instance).__name__ == args[0]
            ]
        else:
            instances = [
                str(instance) for instance in models.storage.all().values()
            ]
        print(instances)

    def do_update(self, arg):
        """
        Updates an instance based on its ID with a new attribute value
        Usage: <class name> <id> <attribute name> "<attribute value>"
        """
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        instance = self._validate_class_instance(class_name, instance_id)
        if not instance:
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_value = args[3].strip('"')
        setattr(instance, attribute_name, attribute_value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
