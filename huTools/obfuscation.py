#!/usr/bin/env python
# encoding: utf-8
"""
hutools/obfuscation.py this contains code to hide data from your little sister.

THIS IS NOT INDUSTRIAL-STRENGTH CRYPTO - use OpenSSL abd friends if you need real crypto!

Created by Maximillian Dornseif on 2009-08-31.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

import sys
import random


class RC4:
    """RC4 en-/decription.

    Based on code from Thomas Dixon at http://www.macshadows.com/forums/index.php?showtopic=5766

    >>> RC4('sekrit').decrypt(RC4('sekrit').encrypt('foo'))
    'foo'
    """
    def __init__(self, key):
        """initialize the state table."""
        random.seed()
        (self.x, self.y) = (0, 0)
        self.state_array = [i for i in range(0, 256)]
        for i in range(0, 256):
            self.x = ((ord(key[i % len(key)]) & 0xff) + self.state_array[i] + self.x) & 0xff
            self.state_array[i], self.state_array[self.x] = self.state_array[self.x], self.state_array[i]
        self.x = 0

    def engine_crypt(self, input):
        self.out = []
        for i in range(0, len(input)):
            self.x = (self.x + 1) & 0xff
            self.y = (self.state_array[self.x] + self.y) & 0xff
            self.state_array[self.x], self.state_array[self.y] = \
                self.state_array[self.y], self.state_array[self.x]
            self.out.append(chr((ord(input[i]) ^
                                 self.state_array[(self.state_array[self.x]
                                                   + self.state_array[self.y]) & 0xff])))
        return "".join(self.out)

    def encrypt(self, cleartext, iv=None):
        if not iv:
            iv = chr(random.randint(0, 255)) + chr(random.randint(0, 255))
        return self.engine_crypt(str(iv)[-2:] + str(cleartext))

    def decrypt(self, ciphertext):
        ret = self.engine_crypt(ciphertext)
        return ret[2:]

if __name__ == "__main__":
    import doctest
    failure_count, test_count = doctest.testmod()
    sys.exit(failure_count)
