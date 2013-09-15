# coding=utf-8
#
# Copyright 2013 Janne Enberg

from functools import wraps


def cached_method(function):
    """Cache results of methods

    class Foo(object):

        @cached_method
        def foo(self, x, y):
            return x + y

    """
    cache = {}

    @wraps(function)
    def wrapper(*args):
        if not args in cache:
            cache[args] = function(*args)

        return cache[args]

    return wrapper
