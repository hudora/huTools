#!/usr/bin/env python
# encoding: utf-8
"""
decorators.py

Created by Maximillian Dornseif on 2007-05-10.
Copyright (c) 2007 HUDORA GmbH. All rights reserved.
"""


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
