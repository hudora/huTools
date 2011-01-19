#!/usr/bin/env python
# encoding: utf-8

"""
pyJasper client.py - Way to talk to a pyJasper Server.
See http://pypi.python.org/pypi/pyJasper/ for further enligthenment.

Created by Maximillian Dornseif on 2007-10-12.
Moved into huTools in 2010
Consider it BSD licensed.
"""


from cStringIO import StringIO
from huTools.http import fetch
import os
import os.path
import re
import unittest
import warnings
import xml.etree.ElementTree as ET


config = object()
try:
    from django.conf import settings
    # trigger the lazy importer
    getattr(settings, 'DUMMY', None)
except (ImportError, EnvironmentError):
    settings = object()

try:
    import config
except:
    config = object()


class JasperException(RuntimeError):
    """This exception indicates Jasper Server problem."""
    pass


def get_reportname(base, *args):
    """
    Construct path for report file relative to base

    In most cases, this will be JasperGenerator.__file__
    """
    warnings.warn("pyjasper.get_reportname is deprecated", DeprecationWarning, stacklevel=2)
    path = os.path.join(os.path.dirname(base), 'reports', *args)
    return os.path.abspath(path)


def _find_server(serverurl):
    if not serverurl:
        serverurl = getattr(settings, 'PYJASPER_SERVLET_URL', None)
    if not serverurl:
        serverurl = getattr(config, 'PYJASPER_SERVLET_URL', None)
    if not serverurl:
        serverurl = os.environ.get('PYJASPER_SERVLET_URL', None)
    if not serverurl:
        raise JasperException('set PYJASPER_SERVLET_URL')
    return serverurl


class JasperGenerator(object):
    """Abstract class for generating PDF Documents with Jasperreports.

    You have to overwrite generate_xml to make meaningfull use of this class. Then call
    YourClass.generate(yourdata). Yourdata is passed to generate_xml() and hopfully you will get
    the generated report back.
    """

    def __init__(self, serverurl=None, debug=False):
        super(JasperGenerator, self).__init__()
        self.reportname = None
        self.xpath = None
        self.debug = debug
        self.serverurl = _find_server(serverurl)
        warnings.warn("huTools.pyjasper.JasperGenerator() is deprecated use huTools.pyjasper.generate_report() instead.", DeprecationWarning, stacklevel=2)

    def generate_xml(self, data=None):
        """To be overwritten by subclasses.

        E.g.
        def generate_xml(self, movement):
            xmlroot = ET.Element('report')
            ET.SubElement(xmlroot, 'generator').text = __revision__
            ET.SubElement(xmlroot, 'created_at').text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            xml_movement = ET.SubElement(xmlroot, 'movement')
            ET.SubElement(xml_movement, "location_from").text = unicode(movement.location_from)
            return xmlroot
        """
        raise NotImplementedError

    def get_xml(self, data=None):
        """Serializes the XML in the ElementTree to be send to JasperReports."""
        root = self.generate_xml(data)
        tree = ET.ElementTree(root)
        buf = StringIO()
        tree.write(buf, encoding="utf-8")
        ret = buf.getvalue()
        buf.close()
        return ret

    def get_report(self):
        """Get JasperReport template"""
        return open(self.reportname).read()

    def generate_pdf_server(self, design, xpath, xmldata, multi=False):
        """Generate report via pyJasperServer."""
        if multi:
            content = dict(designs=design, xpath=xpath, xmldata=xmldata)
        else:
            content = dict(design=design, xpath=xpath, xmldata=xmldata)
        status, _headers, content = fetch(self.serverurl, content, 'POST')

        if not status == 200:
            raise JasperException("%s -- %r" % (content, status))
        return content

    def generate_pdf(self, data=None):
        """Generates a PDF document by using Jasper-Reports."""
        design = self.get_report()
        xmldata = self.get_xml(data)
        if self.debug:
            open('/tmp/pyjasper-%s-debug.xml' % os.path.split(self.reportname)[-1], 'w').write(xmldata)
        return self.generate_pdf_server(design, self.xpath, xmldata)

    def generate(self, data=None):
        """Generates a report, returns the PDF."""
        return self.generate_pdf(data)


def generate_report(reportdesign, xpath, xmldata, url=None, sign_keyname='', sign_reason='',
                    callback='', metadata=None):
    """Generates a report, returns the PDF.

    reportdesign, xpath and xmldata - necessary data to generate a JasperReport.
    url - points to a jasper server
    sign_keyname - key for the signature lying on the server
    sign_reason - reason to be sent within the signed document
    callback - url to where the generated report will be sent
    metadata - PDF metadata

    Return value is pdf data stripped of timestamps for modification and creaton dates.
    If a callback is given, the server will sent the pdf data to the given URL instead.
    """
    url = _find_server(url)
    content = dict(design=reportdesign, xpath=xpath, xmldata=xmldata)
    if callback:
        content['callback'] = callback
    if sign_keyname:
        content['sign_keyname'] = sign_keyname
        if not sign_reason:
            raise ValueError('reason is needed when signing documents!')
        content['sign_reason'] = sign_reason
    if metadata:
        content['metadata'] = metadata

    status, _headers, content = fetch(url, content, 'POST')
    if not status == 200:
        raise JasperException("%s -- %r" % (content, status))
    # remove Timestamps so the same reports hash the same.
    return re.sub("/(ModDate|CreationDate)\(D:\d{14}[+-]\d{2}'\d{2}'\)", '', content)


_testreport = """<?xml version="1.0" encoding="UTF-8"?>
        <jasperReport xmlns="http://jasperreports.sourceforge.net/jasperreports" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://jasperreports.sourceforge.net/jasperreports http://jasperreports.sourceforge.net/xsd/jasperreport.xsd" name="Lieferschein" pageWidth="595" pageHeight="842" columnWidth="483" leftMargin="56" rightMargin="56" topMargin="70" bottomMargin="28" whenResourceMissingType="Key">
            <queryString language="xPath"><![CDATA[/elements/element]]></queryString>
            <field name="testdata" class="java.lang.String">
                <fieldDescription><![CDATA[*/data]]></fieldDescription>
            </field>
            <detail>
                <band height="32">
                    <staticText>
                        <reportElement x="20" y="20" width="200" height="10"/>
                        <text><![CDATA[Hello World!]]></text>
                    </staticText>
                    <textField isBlankWhenNull="true">
                        <reportElement key="field-1" x="36" y="0" width="300" height="10"/>
                        <textElement><font size="8"/></textElement>
                        <textFieldExpression class="java.lang.String"><![CDATA[$F{testdata}]]></textFieldExpression>
                    </textField>
                </band>
            </detail>
        </jasperReport>
        """


class _TestGenerator(JasperGenerator):

    def generate_xml(self, dummy):
        self.xpath = '/elements/element'
        xmlroot = ET.Element('elements')
        xml_movement = ET.SubElement(xmlroot, 'element')
        ET.SubElement(xml_movement, "data").text = unicode('TESTTEXT')
        return xmlroot

    def get_report(self):
        # unfortunately this example data always generates an empty report. Why?
        # it's at least enough for testing
        self.reportname = 'Nada'
        return _testreport


class testTests(unittest.TestCase):

    def test_legacy_class(self):
        gen = _TestGenerator()
        content = gen.generate()

    def test_function(self):
        content = generate_report(_testreport, 
                                  '/elements/element',
                                  '<elements><element><data>TEST</data></element></elements>',
                                 sign_keyname="hudora-rechnungen", sign_reason='Testreason for generating documents')


if __name__ == '__main__':
    unittest.main()
