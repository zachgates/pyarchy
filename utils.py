"""
Container for useful functions.
"""


def raise_type_error(arg_name, correct_type):
    """
    Raise a template TypeError.
    """
    raise TypeError("'%s' must be of type %s" % (
                    arg_name,
                    correct_type))


def strict_arg(arg_name, arg_types, inner_types=()):
    """
    Decorator for any function requiring an argument of a specific type.
    """
    def func_wrapper(func):
        if hasattr(func, "wrapped_args"):
            wrapped_args = getattr(f, "wrapped_args")
        else:
            code = func.__code__
            wrapped_args = list(code.co_varnames[:code.co_argcount])

        try:
            arg_index = wrapped_args.index(arg_name)
        except ValueError:
            raise NameError('missing required argument: ' + arg_name)

        def wrapper(*args, **kwargs):
            if len(args) > arg_index:
                arg = args[arg_index]
                if not isinstance(arg, arg_types):
                    raise_type_error(arg_name, type(arg))
            else:
                if arg_name in kwargs:
                    arg = kwargs[arg_name]

                    if not isinstance(arg, arg_types):
                        raise_type_error(arg_name, type(arg))
                    elif inner_types and isinstance(arg, (tuple, list)):
                        if any(not isinstance(v, inner_types) for v in arg):
                            raise_type_error(arg_name, '[%s]' % type(arg))
                    elif inner_types and isinstance(arg, dict):
                        if any(not isinstance(v, inner_types) for v in arg.values()):
                            raise_type_error(arg_name, '{:%s}' % type(arg))

            return func(*args, **kwargs)

        wrapper.wrapped_args = wrapped_args
        return wrapper

    return func_wrapper


__all__ = [
    raise_type_error,
    strict_arg,
]
