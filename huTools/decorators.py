#!/usr/bin/env python
# encoding: utf-8
"""
decorators.py

Created by Maximillian Dornseif on 2007-05-10.
Copyright (c) 2007 HUDORA GmbH. All rights reserved.
"""


import cPickle as pickle
import functools
import hashlib
from decorator import decorator


def _getattr_(obj, name, default_thunk):
    "Similar to .setdefault in dictionaries."
    try:
        return getattr(obj, name)
    except AttributeError:
        default = default_thunk()
        setattr(obj, name, default)
        return default

# from http://www.phyast.pitt.edu/~micheles/python/documentation.html
@decorator
def memoize(func, *args):
    """This decorator caches the results of the function it decorates.
    
    See http://en.wikipedia.org/wiki/Memoisation for fare more than ypou ever want to know on that topic.
    """
    
    dic = _getattr_(func, "memoize_dic", dict)
    # memoize_dic is created at the first call
    if args in dic:
        return dic[args]
    else:
        result = func(*args)
        dic[args] = result
        return result


# from somewhere on the internet
def cache_function(length):
    """
    A variant of the snippet posted by Jeff Wheeler at
    http://www.djangosnippets.org/snippets/109/
    
    Caches a function, using the function and its arguments as the key, and the return
    value as the value saved. It passes all arguments on to the function, as
    it should.
    
    The decorator itself takes a length argument, which is the number of
    seconds the cache will keep the result around.
    
    It will put in a MethodNotFinishedError in the cache while the function is
    processing. This should not matter in most cases, but if the app is using
    threads, you won't be able to get the previous value, and will need to
    wait until the function finishes. If this is not desired behavior, you can
    remove the first two lines after the ``else``.
    """
    
    def decorator(func):
        
        def inner_func(*args, **kwargs):
            from django.core.cache import cache
            
            raw = [func.__name__, func.__module__, args, kwargs]
            pickled = pickle.dumps(raw, protocol=pickle.HIGHEST_PROTOCOL)
            key = hashlib.md5(pickled).hexdigest()
            value = cache.get(key)
            if value:
                return value
            else:
                # This will set a temporary value while ``func`` is being
                # processed. When using threads, this is vital, as otherwise
                # the function can be called several times before it finishes
                # and is put into the cache.
                
                class MethodNotFinishedError(Exception):
                    pass
                cache.set(key, MethodNotFinishedError(
                    'The function %s has not finished processing yet. This value will be replaced when it finishes.' % (func.__name__)
                ), length)
                result = func(*args, **kwargs)
                cache.set(key, result, length)
                return result
        return inner_func
    return decorator
    

# from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/425445


def func_once(func):
    "A decorator that runs a function only once."
    
    def decorated(*args, **kwargs):
        try:
            return decorated._once_result
        except AttributeError:
            decorated._once_result = func(*args, **kwargs)
            return decorated._once_result
    return decorated


def method_once(method):
    "A decorator that runs a method only once."
    attrname = "_%s_once_result" % id(method)
    
    def decorated(self, *args, **kwargs):
        try:
            return getattr(self, attrname)
        except AttributeError:
            setattr(self, attrname, method(self, *args, **kwargs))
            return getattr(self, attrname)
    return decorated


def none_on_exception(func):
    """A decorator that returns the return value of a function or None if an exception is raised."""

    @functools.wraps(func)
    def _decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return _decorator
