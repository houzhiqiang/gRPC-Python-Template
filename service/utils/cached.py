"""缓存"""
import threading
from time import time
from datetime import datetime
from threading import Lock

from .. import app


# pylint: skip-file
# flake8: noqa


# pylint: disable=C0103


# class _Missing(object):
# 
#     def __repr__(self):
#         return 'no value'
# 
#     def __reduce__(self):
#         return '_missing'
# 
# _missing = _Missing()


# class cached_property(property):
# 
#     """A decorator that converts a function into a lazy property.  The
#     function wrapped is called the first time to retrieve the result
#     and then that calculated result is used the next time you access
#     the value::
#         class Foo(object):
#             @cached_property
#             def foo(self):
#                 # calculate something important here
#                 return 42
#     The class has to have a `__dict__` in order for this property to
#     work.
#     """
# 
#     # implementation detail: A subclass of python's builtin property
#     # decorator, we override __get__ to check for a cached value. If one
#     # chooses to invoke __get__ by hand the property will still work as
#     # expected because the lookup logic is replicated in __get__ for
#     # manual invocation.
# 
#     def __init__(self, func, name=None, doc=None):
#         self.__name__ = name or func.__name__
#         self.__module__ = func.__module__
#         self.__doc__ = doc or func.__doc__
#         self.func = func
# 
#     def __set__(self, obj, value):
#         obj.__dict__[self.__name__] = value
# 
#     def __get__(self, obj, type=None):
#         if obj is None:
#             return self
#         value = obj.__dict__.get(self.__name__, _missing)
#         if value is _missing:
#             value = self.func(obj)
#             obj.__dict__[self.__name__] = value
#         return value


class threaded_cached_property(object):
    """
    A cached_property version for use in environments where multiple threads
    might concurrently try to access the property.
    """

    def __init__(self, func):
        self.__doc__ = getattr(func, "__doc__")
        self.func = func
        self.lock = threading.RLock()

    def __get__(self, obj, cls):
        if obj is None:
            return self

        obj_dict = obj.__dict__
        name = self.func.__name__
        with self.lock:
            try:
                # check if the value was computed before the lock was acquired
                return obj_dict[name]

            except KeyError:
                # if not, do the calculation and release the lock
                return obj_dict.setdefault(name, self.func(obj))


class cached_property_with_ttl(object):
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Setting the ttl to a number expresses how long
    the property will last before being timed out.
    """

    def __init__(self, ttl=None):
        if callable(ttl):
            func = ttl
            ttl = None
        else:
            func = None
        self.ttl = ttl
        self._prepare_func(func)

    def __call__(self, func):
        self._prepare_func(func)
        return self

    def __get__(self, obj, cls):
        if obj is None:
            return self

        now = time()
        obj_dict = obj.__dict__
        name = self.__name__
        try:
            value, last_updated = obj_dict[name]
        except KeyError:
            pass
        else:
            ttl_expired = self.ttl and self.ttl < now - last_updated
            if not ttl_expired:
                return value

        value = self.func(obj)
        obj_dict[name] = (value, now)
        return value

    def __delete__(self, obj):
        obj.__dict__.pop(self.__name__, None)

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = (value, time())

    def _prepare_func(self, func):
        self.func = func
        if func:
            self.__doc__ = func.__doc__
            self.__name__ = func.__name__
            self.__module__ = func.__module__


# Aliases to make cached_property_with_ttl easier to use
cached_property_ttl = cached_property_with_ttl
timed_cached_property = cached_property_with_ttl


class threaded_cached_property_with_ttl(cached_property_with_ttl):
    """
    A cached_property version for use in environments where multiple threads
    might concurrently try to access the property.
    """

    def __init__(self, ttl=None):
        super(threaded_cached_property_with_ttl, self).__init__(ttl)
        self.lock = threading.RLock()

    def __get__(self, obj, cls):
        with self.lock:
            return super(threaded_cached_property_with_ttl, self).__get__(obj, cls)


# Alias to make threaded_cached_property_with_ttl easier to use
threaded_cached_property_ttl = threaded_cached_property_with_ttl
timed_threaded_cached_property = threaded_cached_property_with_ttl
