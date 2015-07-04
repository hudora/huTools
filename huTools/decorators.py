#!/usr/bin/env python
# encoding: utf-8
"""
decorators.py

Created by Maximillian Dornseif on 2007-05-10.
Copyright (c) 2007, 2015 HUDORA GmbH. All rights reserved.
"""
import cPickle as pickle
import functools
import hashlib
import threading
import time

from _decorator import decorator
from collections import namedtuple
from functools import update_wrapper


# TODO: können wir _decorator durch "from functools import wraps" ersetzen?


def _getattr_(obj, name, default_thunk):
    "Similar to .setdefault in dictionaries."
    try:
        return getattr(obj, name)
    except AttributeError:
        default = default_thunk()
        setattr(obj, name, default)
        return default

# from https://github.com/carlsverre/wraptor/blob/master/wraptor/decorators/memoize.py

class memoize(object):
    """ Memoize the results of a function.  Supports an optional timeout
        for automatic cache expiration.
        If the optional manual_flush argument is True, a function called
        "flush_cache" will be added to the wrapped function.  When
        called, it will remove all the timed out values from the cache.
        If you use this decorator as a class method, you must specify
        instance_method=True otherwise you will have a single shared
        cache for every instance of your class.
        This decorator is thread safe.
    """
    def __init__(self, timeout=None, manual_flush=False, instance_method=False):
        self.timeout = timeout
        self.manual_flush = manual_flush
        self.instance_method = instance_method
        self.cache = {}
        self.cache_lock = threading.RLock()

    def __call__(self, fn):
        if self.instance_method:
            @functools.wraps(fn)
            def rewrite_instance_method(instance, *args, **kwargs):
                # the first time we are called we overwrite the method
                # on the class instance with a new memoize instance
                if hasattr(instance, fn.__name__):
                    bound_fn = fn.__get__(instance, instance.__class__)
                    new_memoizer = memoize(self.timeout, self.manual_flush)(bound_fn)
                    setattr(instance, fn.__name__, new_memoizer)
                    return getattr(instance, fn.__name__)(*args, **kwargs)

            return rewrite_instance_method

        def flush_cache():
            with self.cache_lock:
                for key in self.cache.keys():
                    if (time.time() - self.cache[key][1]) > self.timeout:
                        del(self.cache[key])

        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            kw = kwargs.items()
            kw.sort()
            key_str = repr((args, kw))
            key = hashlib.md5(key_str).hexdigest()

            with self.cache_lock:
                try:
                    result, cache_time = self.cache[key]
                    if self.timeout is not None and (time.time() - cache_time) > self.timeout:
                        raise KeyError
                except KeyError:
                    result, _ = self.cache[key] = (fn(*args, **kwargs), time.time())

            if not self.manual_flush and self.timeout is not None:
                flush_cache()

            return result

        if self.manual_flush:
            wrapped.flush_cache = flush_cache

        return wrapped


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
                result = func(*args, **kwargs)
                cache.set(key, result, length)
                return result
        return inner_func
    return decorator


# from http://code.activestate.com/recipes/578078-py26-and-py30-backport-of-python-33s-lru-cache/

_CacheInfo = namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"])


class _HashedSeq(list):
    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


def _make_key(args, kwds, typed,
              kwd_mark=(object(),),
              fasttypes={int, str, frozenset, type(None)},
              sorted=sorted, tuple=tuple, type=type, len=len):
    """Make a cache key from optionally typed positional and keyword arguments"""
    key = args
    if kwds:
        sorted_items = sorted(kwds.items())
        key += kwd_mark
        for item in sorted_items:
            key += item
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for k, v in sorted_items)
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)


def lru_cache(maxsize=64, typed=False, ttl=None):
    """Least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.

    if *ttl* is set, cache entries are only served for `ttl` seconds.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize) with
    f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used

    """

    # Users should only access the lru_cache through its public API:
    #       cache_info, cache_clear, and f.__wrapped__
    # The internals of the lru_cache are encapsulated for thread safety and
    # to allow the implementation to change (including a possible C version).

    def decorating_function(user_function):

        cache = dict()
        maxage = dict()                 # stores the timestamp after wich result should be regeneratd
        stats = [0, 0]                  # make statistics updateable non-locally
        HITS, MISSES = 0, 1             # names for the stats fields
        make_key = _make_key
        cache_get = cache.get           # bound method to lookup key or return None
        maxage_get = maxage.get
        _len = len                      # localize the global len() function
        lock = threading.RLock()                  # because linkedlist updates aren't threadsafe
        root = []                       # root of the circular doubly linked list
        root[:] = [root, root, None, None]      # initialize by pointing to self
        nonlocal_root = [root]                  # make updateable non-locally
        PREV, NEXT, KEY, RESULT = 0, 1, 2, 3    # names for the link fields

        if maxsize == 0:

            def wrapper(*args, **kwds):
                # no caching, just do a statistics update after a successful call
                result = user_function(*args, **kwds)
                stats[MISSES] += 1
                return result

        elif maxsize is None:

            def wrapper(*args, **kwds):
                # simple caching without ordering or size limit
                key = make_key(args, kwds, typed)
                result = cache_get(key, root)   # root used here as a unique not-found sentinel
                if result is not root:
                    if maxage_get(key, 0) < time.time():
                        stats[HITS] += 1
                        return result
                result = user_function(*args, **kwds)
                cache[key] = result
                if ttl:
                    maxage[key] = int(time.time() + ttl)
                stats[MISSES] += 1
                return result

        else:

            def wrapper(*args, **kwds):
                # size limited caching that tracks accesses by recency
                key = make_key(args, kwds, typed) if kwds or typed else args
                with lock:
                    link = cache_get(key)
                    if link is not None:
                        if maxage_get(key, None) < time.time():
                            # record recent use of the key by moving it to the front of the list
                            root, = nonlocal_root
                            link_prev, link_next, key, result = link
                            link_prev[NEXT] = link_next
                            link_next[PREV] = link_prev
                            last = root[PREV]
                            last[NEXT] = root[PREV] = link
                            link[PREV] = last
                            link[NEXT] = root
                            stats[HITS] += 1
                            return result
                result = user_function(*args, **kwds)
                if ttl:
                    maxage[key] = int(time.time() + ttl)
                with lock:
                    root, = nonlocal_root
                    if key in cache:
                        # getting here means that this same key was added to the
                        # cache while the lock was released.  since the link
                        # update is already done, we need only return the
                        # computed result and update the count of misses.
                        pass
                    elif _len(cache) >= maxsize:
                        # use the old root to store the new key and result
                        oldroot = root
                        oldroot[KEY] = key
                        oldroot[RESULT] = result
                        # empty the oldest link and make it the new root
                        root = nonlocal_root[0] = oldroot[NEXT]
                        oldkey = root[KEY]
                        oldvalue = root[RESULT]
                        root[KEY] = root[RESULT] = None
                        # now update the cache dictionary for the new links
                        del cache[oldkey]
                        cache[key] = oldroot
                    else:
                        # put result in a new link at the front of the list
                        last = root[PREV]
                        link = [last, root, key, result]
                        last[NEXT] = root[PREV] = cache[key] = link
                    stats[MISSES] += 1
                return result

        def cache_info():
            """Report cache statistics"""
            with lock:
                return _CacheInfo(stats[HITS], stats[MISSES], maxsize, len(cache))

        def cache_clear():
            """Clear the cache and cache statistics"""
            with lock:
                cache.clear()
                root = nonlocal_root[0]
                root[:] = [root, root, None, None]
                stats[:] = [0, 0]

        wrapper.__wrapped__ = user_function
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return update_wrapper(wrapper, user_function)

    return decorating_function


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
