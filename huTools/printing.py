#!/usr/bin/env python
# encoding: utf-8
"""
printing.py simple minded toolkit for printing on CUPS.

Created by Maximillian Dornseif on 2006-11-19. BSD Licensed.
"""

import logging
from subprocess import Popen, PIPE, call
import os

__revision__ = "$Revision$"

LOG_FILENAME = '/tmp/huTools_lplog.%d' % os.geteuid()
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)


def print_file(filename, jobname=None, printer=None, copies=1):
    """Print a file."""
    args = ['/usr/local/bin/lpr', '-#%d' % copies]
    if printer:
        args.append('-P%s' % str(printer))
    args.append('"%s"' % filename)
    logging.info(' '.join(args))
    call(args)

def print_data(data, jobname=None, printer=None, copies=1, printserver='printserver.local.hudora.biz'):
    """Print a datastream."""
    args = ['/usr/local/bin/lpr', '-#%d' % copies]
    if printer:
        args.append('-P%s' % str(printer))

    #if printserver:
    #    args.append('-H %r' % str(printserver))
    #if jobname:
    #    args.append('-J %r' % jobname.replace("'\";./ ", "_"))

    logging.info(' '.join(args))
    pipe = Popen(args, shell=False, stdin=PIPE).stdin
    pipe.write(data)
    pipe.close()
