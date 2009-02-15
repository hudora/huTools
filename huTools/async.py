#!/usr/bin/env python
# encoding: utf-8
"""
async.py - functions for asyncrounous code

Created by Maximillian Dornseif on 2009-02-15.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

import copy
import threading
# from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/84317
class Future:
    """This calls a finction in e separate thread and returns a function waiting for that thread to finish.
    
    Typical use:
    
    tagfuture = Future(get_slow_tagcount, 'parameter') # starts a separate thread
    ... do something else ...
    tagcount = tagfuture() # waits for thread to finish and returns result
    
    """
    
    def __init__(self, func, *args, **kwargs):
        # Constructor
        self.__done=0
        self.__result=None
        self.__status='working'
        self.__excpt = None
        
        self.__C=threading.Condition()   # Notify on this Condition when result is ready
        
        # Run the actual function in a separate thread
        self.__T=threading.Thread(target=self.Wrapper,args=((func,) + args), **kwargs)
        self.__T.setName("FutureThread")
        self.__T.start()
    
    def __repr__(self):
        return '<Future at '+hex(id(self))+':'+self.__status+'>'
    
    def __call__(self):
        self.__C.acquire()
        while self.__done==0:
            self.__C.wait()
        self.__C.release()
        # We deepcopy __result to prevent accidental tampering with it.
        a=copy.deepcopy(self.__result)
        if self.__excpt:
            raise self.__excpt[0], self.__excpt[1], self.__excpt[2]
        return a
    
    def Wrapper(self, func, *args, **kwargs):
        # Run the actual function, and let us housekeep around it
        self.__C.acquire()
        try:
            self.__result=func(*args, **kwargs)
        except:
            self.__result="Exception raised within Future"
            self.__excpt = sys.exc_info()
        self.__done=1
        self.__status=self.__result
        self.__C.notify()
        self.__C.release()
