"""
Container for some common Object types.
"""


import time

from . import utils
from .core import Object, IdentifiedObject


class TimedObject(Object):
    """
    An Object requiring a timstamp at instantiation.
    """

    def __init__(self):
        Object.__init__(self)
        self.__timestamp = time.time()

    def __str__(self):
        return str(self.__timestamp)

    def __repr__(self):
        return 'TimedObject(%f)' % self.__timestamp

    def __lt__(self, obj):
        if isinstance(obj, TimedObject):
            return self.__timestamp < obj.timestamp
        else:
            # Don't support comparisions with other types.
            return NotImplemented

    def __gt__(self, obj):
        if isinstance(obj, TimedObject):
            return self.__timestamp > obj.timestamp
        else:
            # Don't support comparisions with other types.
            return NotImplemented

    @property
    def timestamp(self):
        """
        A timestamp representing the time at the object's instantiation.
        """
        return self.__timestamp


class NamedObject(Object):
    """
    An Object with a name.
    """

    def __init__(self, name):
        Object.__init__(self)

        if self.check_name(name):
            self.__name = name
        else:
            raise TypeError('name must be alphanumeric')

    def __str__(self):
        return self.__name

    def __repr__(self):
        return "NamedObject('%s')" % self.__name

    @staticmethod
    @utils.strict_arg('name', str)
    def check_name(name: str) -> bool:
        """
        Validate the provided name.
        """
        return name.isalnum()

    @property
    def name(self) -> str:
        """
        The name of the object.
        """
        return self.__name

    @name.setter
    def name(self, name):
        """
        The setter for the name property.
        """
        if self.check_name(name):
            self.__name = name
        else:
            raise TypeError("got invalid name: '%s'" % name)


class StrictlyNamedObject(NamedObject):
    """
    An object with an constant name defined at instantiation.
    """

    def __str__(self):
        return self.__name

    def __repr__(self):
        return "StrictlyNamedObject('%s')" % self.__name

    @NamedObject.name.setter
    def name(self, name):
        """
        Blocker for the NamedObject setter.
        """
        raise UserWarning("cannot change object's name")


class ClassicObject(IdentifiedObject, TimedObject, NamedObject):
    """
    The base class for most objects.
    """

    def __init__(self, name):
        IdentifiedObject.__init__(self)
        TimedObject.__init__(self)
        NamedObject.__init__(self, name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "ClassicObject('%s')" % self.name


__all__ = [
    TimedObject,
    NamedObject,
    StrictlyNamedObject,
    ClassicObject,
]
