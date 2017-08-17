"""
A container for custom data containers.
"""


from .utils import make_deep_copy, raise_key_index_error


class HardKeySet(object):
    """
    A set of key-value pairs that allows mutable objects to be keys. They are
    copied on addition to the set, and will remain unchanged.
    """

    def __init__(self):
        object.__init__(self)
        self.__items = {}

    def __contains__(self, key):
        return id(key) in self.__items

    def __getitem__(self, key):
        for id_, (k, v) in self.__items.items():
            if id_ == id(key):
                return make_deep_copy(v)
        else:
            raise_key_index_error(key)

    def __setitem__(self, key, value):
        for id_, (k, v) in self.__items.items():
            if id_ == id(key):
                del self.__items[id_]
                break

        self.__items[id(key)] = (make_deep_copy(key), make_deep_copy(value))

    def __delitem__(self, key):
        for id_, (k, v) in self.__items.items():
            if id_ == id(key):
                del self.__items[id_]
                break
        else:
            raise_key_index_error(key)

    def __iter__(self):
        for id_, (k, v) in self.__items.items():
            yield (k, v)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.__class__.__name__ + '([%i])' % len(self.__items)

    def get(self, key):
        return self.__getitem__(key, value)

    def add(self, key, value):
        self.__setitem__(key, value)
        return 

    def remove(self, key):
        self.__delitem__(key)

    def update(self, key, value):
        self.__setitem__(key, value)
        return (key, value)


__all__ = [
    HardKeySet,
]
