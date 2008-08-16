#!/usr/bin/env python
# encoding: utf-8
"""
luids.py

Tools for generating various local unique IDs.

This module tries to generate IDs which are guaranteed to be unique on a machine. Compared with the fine uuid
module in python 2.5 we try to be unique only on a single host and not globally. In turn we provide stronger
guarantees that no ID will be ever duplicate on a machine. Therfor our IDs are perfect for generating unique
filenames in a directory used by severall processes/threads.

See http://docs.python.org/lib/module-uuid.html and http://zesty.ca/python/uuid.py for the Python standard
uuid module.

Created by Maximillian Dornseif on 2006-11-08. BSD Licensed.
"""

import os, time, socket
import unittest

try:
    import thread as _thread
except ImportError:
    import dummy_thread as _thread

__revision__ = "$Revision$"

_counter = 0
_counter_lock = _thread.allocate_lock()
def unique_machine32():
    """
    Generate an ID which has a low probability of repeating on this machine.
    
    What goes where:
    
      PP ^
    TTtt ^
    c
    
    So the first byte is an combination of a counter (c) and the first byte of the least significant 
    (and thus fastest changing) word (TT) of the current timestamp. This is followed by the next byte of the 
    least significant word of the current timestamp (TT). The next two bytes are the PID (PP) and the most 
    significant word of the current timestamp (tt) XORed.
    
    Assuming 16bit PIDs this should result in unique IDs on a machine even with multi-threading. But there 
    are degenerated scenarios (more than 2**16 concurrent/fast spawning processes, while there are more than 
    2**8 threads bussy generating unique IDs) where the IDs might not be unique.
    To avoid these use unique_machine64.
    """

    global _counter
    try: # Entering critical section.
        _counter_lock.acquire()
        now      = time.time()
        intnow   = long(now)
        _counter = (_counter + 1) % 0xff
        # shift more significant bytes of time up so they don't overlap PID
        ret = (os.getpid() ^ (intnow << 16) ^ (intnow >> 16)  ^ (_counter << 24)) % 0xffffffff
    finally:
        _counter_lock.release()
    return ret
    
def unique_machine64():
    """
    Generate an ID which should never repeat on this machine.
    
    This function is suggested as the base for generating filenames and the like. Processes/Threads 
    running on the same machine should never be able to generate the same ID and no ID should be created 
    twice.
    
    What goes where:
    TTTT     ^
        PP   ^
        cccc
        
    The first two words are the current timestamp. The next word is the current  PID xored with the most
    significant word of a counter. The last byte is the most significant word of a counter. 
    The counter is being increased by 1 in every call. This should make this function thread 
    save unless you call it more than 2**16 times per second.
    """
    
    global _counter
    try: # Entering critical section.
        _counter_lock.acquire()
        now      = time.time()
        intnow   = long(now)
        _counter = (_counter + 1) % 0xffffffff
        ret = ((intnow << 32) ^ (os.getpid() << 16) ^ (_counter)) % 0xffffffffffff
    finally:
        _counter_lock.release()
    return ret
    
_hostname = None
def luid():
    """Generate an ID which should be globally unique.
    
    This only works if gethostname() returns an unique name. This usually is true to a certain degree if you 
    use your machine in an NIS/NFS configuration. So this function is mainly usefull to generate unique
    filenames for NFS-shared filesystems.
    
    So this is very well suited for generationg IDs in a setup where you controll all the machines and thus
    hostnames."""
    
    global _hostname
    if not _hostname:
        _hostname = socket.gethostname()
    return "%s%x" % (_hostname, unique_machine64())

# Testcases

class _uuidsTests(unittest.TestCase):
    """Simple Testcases for uuid generation."""
    
    def test_unique_machine32(self):
        """Basic tests for unique_machine32."""
        seen = set()
        for i in range(250):
            uuid = unique_machine32()
            self.assertTrue((uuid <= 0xffffffff) and (uuid >= 0))
            self.assertFalse(uuid in seen)
            seen.add(uuid)
        time.sleep(1) # avois wrap arround of counter
        for i in range(250):
            uuid = unique_machine32()
            self.assertTrue((uuid <= 0xffffffff) and (uuid >= 0))
            self.assertFalse(uuid in seen)
            seen.add(uuid)
    
    def test_unique_machine64(self):
        """Basic tests for unique_machine64."""
        seen = set()
        for i in range(30000):
            uuid = unique_machine64()
            self.assertFalse(uuid in seen)
            self.assertTrue((uuid <= 0xffffffffffff) and (uuid >= 0))
            seen.add(uuid)
    
if __name__ == '__main__':
    unittest.main()