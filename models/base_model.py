#!/usr/bin/python3
"""Contains BaseModel definition"""

import uuid
import datetime

import models


class BaseModel:
    """BaseModel class

    Other models will inherit from this class

    Attributes:
        id: generated id of a new instance
        created_at: time of instance creation
        updated_at: time at which the instance was updated
    """

    def __init__(self, *args, **kwargs):
        """Instantiates a BaseModel instance"""
        # use provided values to instantiate an object
        if kwargs:
            for key, val in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at":
                    self.created_at = datetime.datetime.strptime(
                        val, "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.updated_at = datetime.datetime.strptime(
                        val, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    setattr(self, key, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Returns string representation of a BaseModel object"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Saves a BaseModel instance"""
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """Converts instance to dictionary"""
        dic = {}
        dic["__class__"] = self.__class__.__name__
        for key, val in self.__dict__.items():
            if isinstance(val, datetime.datetime):
                dic[key] = val.isoformat()
            else:
                dic[key] = val
        return dic
