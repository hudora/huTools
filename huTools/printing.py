#!/usr/bin/env python
# encoding: utf-8
"""
printing.py simple minded toolkit for printing on CUPS.

Created by Maximillian Dornseif on 2006-11-19. BSD Licensed.
"""

import logging
import tempfile
from subprocess import Popen, PIPE, call
import os

__revision__ = "$Revision$"

LOG_FILENAME = '/tmp/huTools_lplog.%d' % os.geteuid()
logging.basicConfig(format="%(asctime)-15s  %(message)s", filename=LOG_FILENAME, level=logging.INFO)


def print_file(filename, jobname=None, printer=None, copies=1):
    """Print a file."""
    args = ['/usr/local/bin/lpr', '-#%d' % copies]
    if printer:
        args.append('-P%s' % str(printer))
    args.append('"%s"' % filename)
    assert(filename)
    assert(filename.strip())
    logging.info(' '.join(args))
    call(args)


def print_data(data, jobname=None, printer=None, copies=1,
        printserver='printserver.local.hudora.biz', debug=True):
    """Print a datastream."""
    args = ['/usr/local/bin/lpr', '-#%d' % copies]
    if printer:
        args.append('-P%s' % str(printer))

    # debugging output to track this f*ckn cups error
    if debug:
        tmpname = tempfile.mktemp(dir='/tmp/')
        open(tmpname, 'w').write(data)
        logging.info('wrote printerstream to file: ' + tmpname)

    #if printserver:
    #    args.append('-H %r' % str(printserver))
    #if jobname:
    #    args.append('-J %r' % jobname.replace("'\";./ ", "_"))

    logging.info(' '.join(args))
    pipe = Popen(args, shell=False, stdin=PIPE).stdin
    pipe.write(data)
    pipe.close()

