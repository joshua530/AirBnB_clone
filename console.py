#!/usr/bin/python3
"""Contains HBNBCommand class"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """HBNB console entry point"""

    prompt = "(hbnb) "
    __allowed_classes = (
        "BaseModel", "User", "State", "Place", "Review", "City", "Amenity"
    )

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Quit command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Empty line function"""
        pass

    def do_create(self, arg):
        """Creates a new instance"""
        if len(arg) == 0:
            print("** class name missing **")
        elif arg not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        else:
            instance = eval(arg)()
            instance.save()
            print(instance.id)

    def do_show(self, arg):
        """Displays string representation of an instance"""
        if len(arg) == 0:
            print("** class name missing **")
            return
        args = split_arg(arg)
        if args[0] not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        id = construct_key(args[0], args[1])
        stored_instances = storage.all()
        if id not in stored_instances.keys():
            print("** no instance found **")
            return
        instance = stored_instances[id]
        print(instance)

    def do_destroy(self, arg):
        """Deletes an instance"""
        if len(arg) == 0:
            print("** class name missing **")
            return
        args = split_arg(arg)
        if args[0] not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = construct_key(args[0], args[1])
        if not key_in_storage(key):
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based or
        not on the class name
        """
        objs = []
        # print all objects
        if len(arg) == 0:
            for k, v in storage.all().items():
                objs.append(str(v))
        else:
            # print objects from a specific class
            args = split_arg(arg)
            if args[0] not in HBNBCommand.__allowed_classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if args[0] in k:
                    objs.append(str(v))
        print(objs)

    def do_update(self, arg):
        """Updates a stored object's properties

        Format: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = split_arg(arg)
        key = ""

        # check class
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
            return

        # check id
        if len(args) == 1:
            print("** instance id missing **")
            return
        id = args[1]
        key = construct_key(class_name, id)
        if key not in storage.all().keys():
            print("** no instance found **")
            return

        # check attribute name
        if len(args) == 2:
            print("** attribute name missing **")
            return
        attribute_name = args[2]

        # check attribute value
        if len(args) == 3:
            print("** value missing **")
            return
        attribute_value = args[3]

        # command matches format
        # get the type that provided value should be cast to
        cast_type = type(eval(attribute_value))
        # remove quotation marks used to represent string on command
        # line so that we're left with actual string
        attribute_value = attribute_value.strip("'\"")
        # set instance attributes
        setattr(storage.all()[key], attribute_name, cast_type(attribute_value))
        storage.all()[key].save()

    def default(self, line):
        """Runs if no default command is provided"""
        args = tuple(line.split("."))
        if len(args) < 2:
            print("** invalid command **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
            return
        method = args[1]
        if method == "all()":
            objs = []
            for k, v in storage.all().items():
                if class_name in k:
                    objs.append(v)
            print(objs)
        elif method == "count()":
            num = 0
            for k, v in storage.all().items():
                if class_name in k:
                    num += 1
            print(num)
        else:
            # 'method(args)' split up into method and arguments
            method_and_args = method.split("(")  # ['method', '<args>)']
            method = method_and_args[0]
            args = method_and_args[1].split(")")[0]

            if method == "show":
                HBNBCommand.do_show(self, "{} {}".format(class_name, args))
            elif method == "destroy":
                HBNBCommand.do_destroy(self, "{} {}".format(class_name, args))
            elif method == "update":
                # <id>, <attribute name>, <attribute value>
                args = args.split(",")
                if len(args) < 3:
                    print("** invalid format **")
                    return
                # remove quotes and whitespace
                id = args[0].strip(" \"'")
                attribute = args[1].strip(" \"'")
                value = args[2]
                HBNBCommand.do_update(
                    self, "{} {} {} {}".format(class_name, id, attribute, value))


def key_in_storage(id):
    """Checks whether a given key has been stored"""
    stored_instances = storage.all()
    if id not in stored_instances.keys():
        return False
    return True


def construct_key(class_name, id):
    """Utility key construction function"""
    return "{}.{}".format(class_name, id)


def split_arg(arg):
    """splits given argument using spaces"""
    return tuple(arg.split())


if __name__ == "__main__":
    HBNBCommand().cmdloop()
