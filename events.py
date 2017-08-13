"""
Container for Event Objects.
"""


from .common import ClassicObject, StrictlyNamedObject
from .core import ObjectPool, ConditionalObject
from .utils import strict_arg


class Event(ClassicObject, ConditionalObject):

    _handlers = {}
    _name = ''

    @classmethod
    def handler(cls, func_or_cls):
        if hasattr(func_or_cls, 'name'):
            name = func_or_cls.name
        elif callable(func_or_cls):
            name = func_or_cls.__qualname__
        elif isinstance(func_or_cls, str):
            name = func_or_cls
        else:
            raise TypeError('expected callable with name or explicit name')

        cls._handlers[name] = func_or_cls
        return func_or_cls

    def __init__(self):
        ClassicObject.__init__(self, self._name)
        ConditionalObject.__init__(self, lambda: self.permitted)
        self.permitted = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Event('%s')" % self.name

    def execute(self):
        """
        Execute the code for the event. Override in a subclass.
        """
        pass

    @property
    def permitted(self):
        """
        A boolean representing whether the event should be considered.
        """
        return self.__permitted

    @permitted.setter
    @strict_arg('mode', bool)
    def permitted(self, mode: bool):
        self.__permitted = mode


class EventPool(ObjectPool, StrictlyNamedObject):

    object_type = Event

    def __init__(self, name, *events: Event):
        if any(not isinstance(e, Event) for e in events):
            raise_type_error('events', Event)

        ObjectPool.__init__(self, *events)
        StrictlyNamedObject.__init__(self, name)

    def __str__(self):
        return 'EventPool(%i)' % len(self.__events)

    def __iter__(self):
        """
        Yield the events in the pool in order of creation (newest first).
        """
        objs = ObjectPool.__iter__(self)

        for e in sorted(objs, reverse=True):
            yield e

    def create(self, name, *args):
        event = Event._handlers[name](*args)
        self.add(event)
        return event


__all__ = [
    Event,
    EventPool,
]
