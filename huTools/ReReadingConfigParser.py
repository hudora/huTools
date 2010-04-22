#!/usr/bin/env python
# encoding: utf-8
"""ReReadingConfigParser is designed to be mainly compatible with
ConfigParser but checks before access to values if the
configuration file on disk has changed and re-reads the file if
necessary.

The detection of filechange is done by comparing the mtime of the
file with the mtime the file had when it was last read.

A big difference to the original ConfigParser is that
ReReadingConfigParser does not support setting Values or writing the
configuration to disk.

ReReadingConfigParser.read() only work with a single file not with
lists of filenames. ReReadingConfigParser.readfp() only works with
file like objects which have a name associated and can be
os.stat()ed.

add_section(), set(), write(), remove_option() and
remove_section() are not supported.


Authors:

This Software was written by md@hudora.de for the twisd AG,
Bonn, Germany. The twisd AG kindly donated it as Freie Software.
"""

__version__ = '$Id$'

__copyright__ = """(c) 2001 twisd AG, Bonn - http://www.twisd.de/
further distribution is granted under the terms of LGPL or classical
MIT Licence."""

__revision__ = "$Revision$"

from ConfigParser import ConfigParser
import os
import stat


class ReReadingConfigParser(ConfigParser):

    def ReReadIfChanged(self):
        mtime = os.stat(self.config_name)[stat.ST_MTIME]
        if mtime > self.config_mtime:
            self.read(self.config_name)

    def read(self, fpname):
        # try to find out last modified date of file
        self.config_mtime = os.stat(fpname)[stat.ST_MTIME]
        self.config_name = fpname
        return ConfigParser.read(self, fpname)

    def readfp(self, fdescriptor, filename=None):
        if filename is None:
            filename = fdescriptor.name
            ConfigParser.read(self, filename)

    def sections(self):
        self.ReReadIfChanged()
        return ConfigParser.sections(self)

    def options(self, section):
        self.ReReadIfChanged()
        return ConfigParser.options(self, section)

    def get(self, section, option, raw=0, myvars=None):
        self.ReReadIfChanged()
        return ConfigParser.get(self, section, option, raw, myvars)

    # ReReadingConfigParser is read only, so overwrite configuration
    # changing commands
    def add_section(self, section):
        raise NotImplementedError

    def set(self, section, option, value):
        raise NotImplementedError

    def write(self, fdescriptor):
        raise NotImplementedError

    def remove_option(self, section, option):
        raise NotImplementedError

    def remove_section(self, section):
        raise NotImplementedError


def test():
    import time

    cparser = ReReadingConfigParser()
    fdescriptor = open('ReReadingConfigParser.TESTFILE', 'w')
    fdescriptor.write('[TESTSECTION]\nvalue: 1\n')
    fdescriptor.close()

    cparser.read('ReReadingConfigParser.TESTFILE')
    assert cparser.get('TESTSECTION', 'value') == '1'

    # to be sure mtime has changed
    time.sleep(2)
    fdescriptor = open('ReReadingConfigParser.TESTFILE', 'w')
    fdescriptor.write('[TESTSECTION]\nvalue: 2\n')
    fdescriptor.close()

    assert cparser.get('TESTSECTION', 'value') == '2'
    os.unlink('ReReadingConfigParser.TESTFILE')


if __name__ == '__main__':
    test()
