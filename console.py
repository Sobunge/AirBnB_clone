#!/usr/bin/env python3

import cmd

class HBNBCommand(cmd.Cmd):
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

if __name__ == "__main__":
    prompt = HBNBCommand()
    prompt.cmdloop()

