#!/usr/bin/python3
""" Console Class """
import cmd
import json
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """ Declaring a HBNBCommand """
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Handles EOF (Ctrl+D)"""
        print("^D")
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
            return

        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        try:
            with open("file.json", "r") as file:
                objects = json.load(file)
        except FileNotFoundError:
            print("** no instance found **")
            return

        key = args[0] + "." + args[1]
        if key not in objects:
            print("** no instance found **")
            return

        print(objects[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        try:
            with open("file.json", "r") as file:
                objects = json.load(file)
        except FileNotFoundError:
            print("** no instance found **")
            return

        key = args[0] + "." + args[1]
        if key not in objects:
            print("** no instance found **")
            return

        # Delete the instance
        del objects[key]

        # Save the changes back to the JSON file
        with open("file.json", "w") as file:
            json.dump(objects, file)

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        try:
            with open("file.json", "r") as file:
                objects = json.load(file)
        except FileNotFoundError:
            print("** class doesn't exist **")
            return

        if arg:
            class_name = arg.split()[0]
            instances = [
                            v for k, v in objects.items()
                            if k.startswith(class_name + ".")
                        ]
        else:
            instances = list(objects.values())

        if not instances:
            print("** class doesn't exist **")
        else:
            for instance in instances:
                print(instance)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        try:
            with open("file.json", "r") as file:
                objects = json.load(file)
        except FileNotFoundError:
            print("** no instance found **")
            return

        key = args[0] + "." + args[1]
        if key not in objects:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attribute_name = args[2]
        attribute_value = args[3]

        # Update the attribute value
        objects[key][attribute_name] = attribute_value

        # Save the changes back to the JSON file
        with open("file.json", "w") as file:
            json.dump(objects, file)

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        if not arg:
            print("** class name missing **")
            return

        count = 0
        objects = BaseModel().all()
        for key in objects:
            if key.split(".")[0] == arg:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
