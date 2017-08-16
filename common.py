"""
Container for some common Object types.
"""


import time

from .core import Object, IdentifiedObject, NamedObject


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
            return self.timestamp < obj.timestamp
        else:
            # Don't support comparisions with other types.
            return NotImplemented

    def __gt__(self, obj):
        if isinstance(obj, TimedObject):
            return self.timestamp > obj.timestamp
        else:
            # Don't support comparisions with other types.
            return NotImplemented

    @property
    def timestamp(self):
        """
        A timestamp representing the time at the object's instantiation.
        """
        return self.__timestamp


class StrictlyNamedObject(NamedObject):
    """
    A NamedObject with an constant name defined at instantiation.
    """

    def __str__(self):
        return self.__name

    def __repr__(self):
        return "StrictlyNamedObject('%s')" % self.__name

    @property
    def name(self) -> str:
        """
        The name of the object.
        """
        return self.__name


class ClassicObject(IdentifiedObject, TimedObject, StrictlyNamedObject):
    """
    An Object with an ID, timestamp, and constant name.
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
    StrictlyNamedObject,
    ClassicObject,
]
