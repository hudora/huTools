#!/usr/bin/env python
# encoding: utf-8
"""
huTools/structured_xls.py - csv.py compatible Excel Export.

Created by Maximillian Dornseif on 2014-02-24.
Copyright (c) 2014, 2015 HUDORA. All rights reserved.
"""
import datetime
from cStringIO import StringIO
from xlwt import Workbook, XFStyle


datestyle = XFStyle()
datestyle.num_format_str = 'YYYY-MM-DD'


class XLSwriter(object):
    """csv-Modul kompatibles Interface zum Erzeugen von Excel Dateien.

    Es muss allerdings save() oder getvalue() aufgerufen werden, um die XLS
    Datei zu erzeugen."""

    def __init__(self, output=None, sheetname='Dieses Sheet'):
        self.book = Workbook()
        self.sheet = self.book.add_sheet(sheetname)
        self.rownum = 0
        self.output = output

    def writerow(self, row):
        """Eine Zeile schreiben. Row ist eine Liste von Werten."""
        col = 0
        for coldata in row:
            if isinstance(coldata, (datetime.datetime, datetime.date, datetime.time)):
                self.sheet.write(self.rownum, col, coldata, datestyle)
            else:
                if len(coldata) > 8192:
                    # übergroße Felder RADIKAL verkürzen
                    self.sheet.write(self.rownum, col, "%s ..." % coldata[:64])
                else:
                    self.sheet.write(self.rownum, col, coldata)
            col += 1
        self.rownum += 1

    def save(self, fd=None):
        """Datei nach fd schreiben."""
        if not fd:
            fd = self.output
        assert fd
        self.book.save(fd)
        return fd

    def getvalue(self):
        """Dateiinhalt direkt zurück geben."""
        fd = StringIO()
        self.book.save(fd)
        return fd.getvalue()
