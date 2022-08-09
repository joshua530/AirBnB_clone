#!/usr/bin/python3
"""Contains FileStorage class"""

import json

from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


class FileStorage:
    """FileStorage class definition"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns objects stored by the class"""
        return FileStorage.__objects

    def new(self, obj):
        """Stores an object in the list of stored objects

        Args:
            obj: object to add"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self, obj=None):
        """Saves stored objects to file in json format"""
        dic = {}
        for k, obj in FileStorage.__objects.items():
            dic[k] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(dic, f)

    def reload(self):
        """deserializes json file(__file_path) to __objects"""
        try:
            with open(FileStorage.__file_path, "r") as f:
                tmp = json.load(f)
                for id, data in tmp.items():
                    # instantiate each individual object using it's
                    # class constructor
                    FileStorage.__objects[id] = \
                        eval(data["__class__"])(**data)
        except FileNotFoundError:
            pass
