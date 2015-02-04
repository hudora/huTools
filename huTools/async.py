#!/usr/bin/env python
# encoding: utf-8
"""
async.py - functions for asyncrounous code

Created by Maximillian Dornseif on 2009-02-15.
Copyright (c) 2009 HUDORA. All rights reserved.
parts based on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/84317
"""

import copy
import logging
import sys
import time
import threading


class Future:
    """This calls a function in a separate thread and returns a function waiting for that thread to finish.

    Typical use:

    tagfuture = Future(get_slow_tagcount, 'parameter') # starts a separate thread
    ... do something else ...
    tagcount = tagfuture() # waits for thread to finish and returns result

    """

    def __init__(self, func, *args, **kwargs):
        # Constructor
        self.__done = False
        self.__result = None
        self.__status = 'working'
        self.__excpt = None
        self.__namecache = func.__name__

        self.__Cond = threading.Condition()   # Notify on this Condition when result is ready

        # Run the actual function in a separate thread
        self.__Thread = threading.Thread(target=self.Wrapper, args=((func, ) + args), **kwargs)
        self.__Thread.setName("FutureThread")
        self.__Thread.start()

    def __repr__(self):
        return '<Future at ' + hex(id(self)) + ':' + self.__status + '>'

    def __call__(self):
        waitstart = time.time()
        self.__Cond.acquire()
        while self.__done is False:
            self.__Cond.wait()
        self.__Cond.release()
        # We deepcopy __result to prevent accidental tampering with it.
        ret = copy.deepcopy(self.__result)
        if self.__excpt:
            raise self.__excpt[0], self.__excpt[1], self.__excpt[2]
        waitend = time.time()
        if waitend - waitstart > 1:
            logging.debug("waited %.1f s for %s", waitend - waitstart, self.__namecache)
        return ret

    def Wrapper(self, func, *args, **kwargs):
        # Run the actual function, and let us housekeep around it
        self.__Cond.acquire()
        try:
            self.__result = func(*args, **kwargs)
        except:
            self.__result = "Exception raised within Future"
            self.__excpt = sys.exc_info()
        self.__done = True
        self.__Cond.notify()
        self.__Cond.release()
