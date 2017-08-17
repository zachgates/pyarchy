"""
Container for the most basic Object types.
"""


import re
import types
import uuid

from .meta import MetaNamedObject, MetaSingleton, MetaConditional
from .utils import StrictArg


class Object(object):
    """
    A basic object.
    """

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__ + '()'


class Identity(Object, uuid.UUID):
    """
    A UUID Object.
    """

    def __init__(self):
        Object.__init__(self)
        uuid.UUID.__init__(self, uuid.uuid4().hex)


class IdentifiedObject(Object):
    """
    An object with an ID.
    """

    def __init__(self):
        Object.__init__(self)
        self.__id = Identity()

    def __str__(self):
        return self.id

    @property
    def id(self):
        """
        The object's UUID as a hex string.
        """
        return self.__id.hex


class NamedObject(Object, metaclass = MetaNamedObject):
    """
    An Object with a name.
    """

    def __init__(self, name):
        Object.__init__(self)

        if self.check_name(name):
            self.__name = name
        else:
            raise TypeError('name must be alphanumeric or empty')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__class__.__name__ + "('%s')" % self.name

    @staticmethod
    @StrictArg('name', str)
    def check_name(name: str) -> bool:
        """
        Validate the provided name.
        """
        return bool(re.fullmatch('^[\w\d_]+|', name))

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


class SingletonObject(Object, metaclass = MetaSingleton):
    pass


class ConditionalObject(Object, metaclass = MetaConditional):
    """
    An object that requires a condition to be True to call its functions.
    """

    @property
    def _condition(self):
        return self.__condition

    @_condition.setter
    @StrictArg('func', types.FunctionType)
    def _condition(self, func):
        self.__condition = func

    def __init__(self, func: types.FunctionType):
        Object.__init__(self)
        self.__condition = func

    @property
    def status(self):
        """
        The status of the condition.
        """
        return bool(self.__condition(self))


__all__ = [
    Object,
    Identity,
    IdentifiedObject,
    NamedObject,
    SingletonObject,
    ConditionalObject,
]
