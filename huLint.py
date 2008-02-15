#!/usr/bin/env python
"""
Credit System for Python Code

This program analyzes Python code with pylint
and calculates a credit for the code, depending
on a miimum required score and the previous run.
"""

import sys
from pylint.lint import PyLinter
from pylint import checkers, config
import sqlobject

DATABASE_URI = "sqlite:/Users/chris/Desktop/database.db"
MINIMUM_SCORE = 8.0

#from sqlobject import SQLObject, StringCol, FloatCol, sqlhub, connectionForURI

class PythonScore(sqlobject.SQLObject):
    """
    OO mapping of the score for a Python file
    """
    username = sqlobject.StringCol()
    pathname = sqlobject.StringCol()
    revision = sqlobject.StringCol()
    score = sqlobject.FloatCol()
    old_score = sqlobject.FloatCol()
    credit = sqlobject.FloatCol()
    date = sqlobject.DateTimeCol(default=sqlobject.DateTimeCol.now)


def process_file(filename):
    """
    Analyze the file with pylint and write the result
    to a database
    """
    linter = PyLinter()

    checkers.initialize(linter)
    linter.read_config_file()
    linter.quiet = 1

    filemods = linter.expand_files((filename,))
    if filemods:
        old_stats = config.load_results(filemods[0].get('basename'))
        old_score = old_stats.get('global_note', 0.0)

    linter.check(filename)
    score = eval(linter.config.evaluation, {}, linter.stats)

    # Calculate the credit for both scores
    if score < 0:
        credit = 2.0 * score
    elif score < old_score:
        score = -1.5 * (old_score - score)
    elif score < MINIMUM_SCORE:
        credit = -1.5 * (MINIMUM_SCORE - score)
    else:
        credit = score - old_score

    return score, old_score, credit

def main(args):
    """
    Main function, pass the filename of the file/module
    that should be analyzed.
    """
    conn = sqlobject.connectionForURI(DATABASE_URI)
    sqlobject.sqlhub.processConnection = conn
    #PythonScore.createTable()

    score, old_score, credit = process_file(args[0])
    PythonScore(username="test", pathname=args[0], revision="1",
                score=score, old_score=old_score, credit=credit)
    

if __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        sys.stderr.write("Usage: %s filename\n" % (sys.argv[0]))
        sys.exit()

    main(sys.argv[1:])