#!/usr/bin/python

"""Module for Communication via NetStrings.

This module holds a single class named NetStringIO which wraps
about a file handle and uses NetStrings vor all Communication via
this filehandle.  For more information in netstrings see
http://cr.yp.to/proto/netstrings.txt
    

Authors:

This Software was written by drt@un.bewaff.net for the twisd AG,
Bonn, Germany. The twisd AG kindly donated it as Freie Software.


"""

__version__ = '$Id: NetStringIO.py,v 1.5 2001/05/03 22:05:57 drt Exp$'
  
__copyright__ = """(c) 2001 twisd AG, Bonn - http://www.twisd.de/
further distribution is granted under the terms of LGPL or classical
MIT Licence."""



# * Im not sure at the moment what NetStringIO has to implement to
#   qualify as an file-like object.
#
# * Should I define an own error object for this module instead of using
#   IOerror?
#
# * Should I implement readline(), readlines() and writelinesU()? 
#   They do not realy make sense withe netstrings, do they?

import os, sys, string

class NetStringIO:
    __doc__ = """Warping arround a file object changing all I/O to netstrings.

    I use this class to warp it arround filehandles obtained by a call
    to socket.makefile(). With this I can build protocols using
    netstrings with ease. For more information in netstrings see
    http://cr.yp.to/proto/netstrings.txt
    
    I like sending an '\n' after every netstring. This makes
    inspection of data on the wire much more readable. You can change
    this behaviour by calling the constructor with an optional empty
    string argument. You even can specify another delimiter than '\n'
    """

    def __init__(self, fileo, delim = '\n'):
        __doc__ = """Create a Netstring object warping a file-like object.
        
        n = NetStringIO.NetStringIO(file [, delimiter])

        The returned object should work like reading or writing
        directly from file while the difference that all reading or
        writing is preformed via netstrings. If you leave out
        'delimiter' every netstring will be followed by '\n' while
        writing and is expected to be followed by '\n' while
        reading. By passing a second parameter to the constructor you
        can change '\n' to something else. By passing '' as second
        parameter you can get the behaviour which is used in bernstein
        protocols: no delimiter between netstrings.
        """

        self.file = fileo
        self.delim = delim

        
    def close(self):
        __doc__ = "Closes the underlying file object."

        self.file.close()


    def isatty(self):
        __doc__ = """Checks if the underlying file Object is a tty.

        I guess using ttys with netstrings is of limited use but who
        knows.
        """
        
        return self.file.isatty()


    def read(self):
        """Read from the underlying file object.

        If the data does not contain a valid netstring or is not
        followed by the delimiter we raise IOerror.

        This is more or less an 1:1 port of the code in
        http://cr.yp.to/proto/netstrings.txt - any more pythonish ways
        to do this?
        """
        
        # read length of netstring
        l = ''
        c = self.file.read(1)
        while c:
            if c == ':':
                # we are ready reading the length
                break
            elif not c:
                raise IOError, "short netstring read at length specification"
            elif c not in string.digits:
                raise IOError, "not a valid netstring: %s is not digit" % c
            l += c
            c = self.file.read(1)

        if not c:
            return None
        
        strlen = int(l)

        # reading from a socket can take multiple attempts . see
        # any text about socket programming - XXX but doesn't
        # handle read this already for us? To check!
        s = ""
        while len(s) < strlen:
            s1 = self.file.read(strlen - len(s))
            if s1 == "":
                raise IOError, "short netstring read at netstring body" 
            s = s + s1
                            
        c = self.file.read(1 + len(self.delim))
        if c != "," + self.delim:
            raise IOError, "not a valid netstring: wrong termination"

        return s

    
    def write(self, s):
        __doc__ = """Writes a Netstring to the underlying fileobject."""

        # XXX check if we have to check for short writes
        self.file.write("%lu:%s,%s" % (len(s), s, self.delim))
        self.file.flush()


def test():
    __doc__ = """A little test suite."""

    import StringIO

    testtext = 'Netstrings rule'
    inf = StringIO.StringIO()
    outf = StringIO.StringIO()

    print "Writing a Netstring ... ",
    f = NetStringIO(outf)
    f.write(testtext)
    print outf.getvalue(),

    inf = StringIO.StringIO(outf.getvalue())
    f.close()

    print "Reading this Netstring ... ",
    
    fz = NetStringIO(inf)
    ret = fz.read()
    assert ret == testtext, "String is different after reading"
    print ret
    fz.close()

if __name__ == '__main__':
	test()
