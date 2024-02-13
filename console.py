#!/usr/bin/python3
""" console """

import cmd
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # for splitting the line along spaces except in double quotes

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            print(obj_dict[key])

    def default(self, line):
        """
        Default handler for unknown commands.
        """
        class_method = line.split('.')
        if len(class_method) == 2:
            class_name, method = class_method
            if class_name in classes:
                if method == 'all()':
                    self.do_all(class_name)
                    return
                elif method == 'count()':
                    self.do_count(class_name)
                    return
                elif method.startswith('show'):
                    args = method.split('(')[1].rstrip(')')
                    instance_id = args.strip()  # Extract the instance ID
                    self.do_show(f"{class_name} {instance_id}")
                    return
                elif method.startswith('destroy'):
                    args = method.split('(')[1].rstrip(')')
                    instance_id = args.strip()  # Extract the instance ID
                    self.do_destroy(f"{class_name} {instance_id}")
                    return
                elif method.startswith('update'):
                    args = method.split('(')[1].rstrip(')')
                    update_params = args.split(',')
                    if len(update_params) != 3:
                        print("** value missing **")
                        return
                    instance_id, attribute_name, \
                        attribute_value = [param.strip()
                                           for param in update_params]
                    self.do_update(
                            f"{class_name} {instance_id}\
                            {attribute_name} {attribute_value}")

                    return
                else:
                    print("Method doesn't exist")
            else:
                print("Class doesn't exist")
        else:
            print("Invalid command syntax")

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

    def do_count(self, arg):
        """Count the number of instances of a class"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] in classes:
            count = sum(
                    1 for instance in models.storage.all().values()
                    if type(instance).__name__ == args[0])
            print(count)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints an instance as a string based on the class name and ID"""
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return False
        if args[0] not in classes:
            print("** class doesn't exist **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False

        key = args[0] + "." + args[1]
        if key in models.storage.all():
            print(models.storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        Usage: <class name>.destroy(<id>)
        """
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return False
        if args[0] not in classes:
            print("** class doesn't exist **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False

        key = args[0] + "." + args[1]
        if key in models.storage.all():
            del models.storage.all()[key]
            models.storage.save()
        else:
            print("** no instance found **")
            return

    def do_update(self, arg):
        """
        Updates an instance based on its ID with a new attribute value
        Usage: <class name> <id> <attribute name> <attribute value>
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
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        instance_id = args[1]
        instance = self._validate_class_instance(class_name, instance_id)
        if not instance:
            return
        attribute_value = args[3].strip('"')
        setattr(instance, attribute_name, attribute_value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
