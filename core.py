"""
Container for the most basic Object types.
"""


import types
import uuid

from . import utils
from .meta import MetaConditional


class Object(object):
    """
    A basic object.
    """
    pass


class ObjectPool(Object):
    """
    A container for Objects. I didn't subclass set, because I didn't want
    all the functionality of a set accessible to the ObjectPool.
    """

    object_type = Object

    def __init__(self, *objs):
        self.readonly = False
        self.protected = False
        self.__objects = set(o for o in objs if isinstance(e, Object))

    def __str__(self):
        return 'ObjectPool[%i]' % len(self)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        """
        The iterator for the pool. Can be overridden by subclasses.
        """
        for o in self.__objects:
            yield o

    def __len__(self):
        return len(self.__objects)

    def create(self, *args, **kwargs) -> Object:
        """
        Base function for creating new Objects in the pool.
        """
        obj = self.object_type(*args, **kwargs)
        self.add(obj)
        return obj

    @property
    def protected(self):
        """
        A boolean representing whether Objects in the pool can be modified.
        """
        return self.__protected

    @protected.setter
    @utils.strict_arg('mode', bool)
    def protected(self, mode: bool):
        self.__protected = mode

    def protect_objects(func):
        """
        A decorator for functions that require the instance have the ability
        to modify objects in the pool.
        """
        def wrapper(self, *args, **kwargs):
            if self.protected:
                raise UserWarning('cannot modify pool elements')
            else:
                return func(self, *args, **kwargs)
        return wrapper

    @property
    def readonly(self):
        """
        A boolean representing whether the pool itself can be modified.
        """
        return self.__readonly

    @readonly.setter
    @utils.strict_arg('mode', bool)
    def readonly(self, mode):
        self.__readonly = mode

    def protect_pool(func):
        """
        A decorator for functions that require the instance be mutable.
        """
        def wrapper(self, *args, **kwargs):
            if self.readonly:
                raise UserWarning('cannot modify pool')
            else:
                return func(self, *args, **kwargs)
        return wrapper

    @protect_objects
    @utils.strict_arg('func', types.FunctionType)
    def map(self, func: types.FunctionType):
        """
        Apply a function to all objects in the pool.
        """
        if not isinstance(func, types.FunctionType):
            raise TypeError('function must be a function')
        else:
            for o in self:
                func(o)

    @utils.strict_arg('func', types.FunctionType)
    def filter(self, func: types.FunctionType):
        """
        Return a subset of the pool where only an object, o, where func(o) is
        True is included.
        """
        if func(Object(dummy=True)) is not None:
            raise UserWarning('cannot modify elements with filter')
        else:
            return ObjectPool(*filter(func, self))

    @protect_objects
    def add(self, obj: Object):
        """
        Add the provided object to the pool.
        """
        if not isinstance(obj, self.object_type):
            raise TypeError('object must be of type %s' % self.object_type)
        else:
            self.__objects.add(obj)

    @protect_pool
    def update(self, *pools):
        """
        Add to the pool all objects in the provided pool.
        """
        if self.strict and any(not isinstance(p, self.__class__) for p in pools):
            raise TypeError('pools must be of same type')
        else:
            self.__objects.update(*(pool.objects for pool in pools))

    def remove(self, obj: Object):
        """
        Remove the provided object from the pool.
        """
        if not isinstance(obj, self.object_type):
            raise TypeError('object must be of type %s' % self.object_type)
        else:
            self.__objects.remove(obj)

    @protect_pool
    def disjoint(self, pool):
        """
        Remove from the pool any objects that are also in the provided pool.
        """
        self.__objects.difference_update(pool)

    @protect_pool
    def clear(self, func: types.FunctionType = None):
        """
        Remove all objects from the pool. If a function is provided, only an
        object, o, where func(o) is True will be removed from the pool.
        """
        if callable(func):
            for obj in self.filter(func):
                self.remove(obj)
        else:
            self.__objects.clear()

    @protect_pool
    def pop(self):
        """
        Remove and return an object from the pool.
        """
        if len(self) > 0:
            obj = self[-1]
            self.remove(obj)
            return obj
        else:
            raise IndexError("can't pop from empty pool")


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

    @property
    def id(self):
        """
        The object's UUID as a hex string.
        """
        return self.__id.hex


class ConditionalObject(Object, metaclass = MetaConditional):
    """
    An object that requires a condition to be True to call its functions.
    """

    @property
    def _condition(self):
        return self.__condition

    @_condition.setter
    @strict_arg('func', types.FunctionType)
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
    ObjectPool,
    Identity,
    IdentifiedObject,
    ConditionalObject,
]
