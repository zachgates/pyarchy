"""
Container for Conditional.
"""


import types

from . import  utils


class __MetaConditional(type):
    """
    A metaclass for any object that requires that a function returns True to
    call its functions.
    """

    @staticmethod
    def status_checker(func):
        """
        A decorator for functions that require the status attribute to be
        True for the function to be executed.
        """
        def func_wrapper(self, *args, **kwargs):
            if self.status:
                return func(self, *args, **kwargs)
            else:
                return None

        return func_wrapper

    def __new__(cls, name, bases, attrs):
        """
        Decorate all public methods with the status_checker function.
        """
        for k, v in attrs.items():
            if not k.startswith('__') and isinstance(v, types.FunctionType):
                attrs[k] = cls.status_checker(v)

        return type.__new__(cls, name, bases, attrs)


class Conditional(object, metaclass = __MetaConditional):
    """
    An object that requires a condition to be True to call its functions.
    """

    def __init__(self, func: types.FunctionType = lambda: True):
        self.condition = func

    @property
    def status(self):
        """
        The status of the condition.
        """
        return bool(self.__conditional_func())

    @property
    def condition(self):
        """
        A callable object.
        """
        return self.__conditional_func

    @condition.setter
    @utils.strict_arg('func', types.FunctionType)
    def condition(self, func):
        self.__conditional_func = func


__all__ = [
    Conditional,
]
