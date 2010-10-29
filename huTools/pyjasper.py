#!/usr/bin/env python
# encoding: utf-8

"""
pyJasper client.py - Way to a pyJasper Server.
See http://pypi.python.org/pypi/pyJasper/ for further enligthenment.

You must tell the code where the pyJasper Servlet is running. Either give the URL via
instatntion `JasperGenerator(serverurl='MYURL')`.

Alternatively the code tries to import a module config and find in the the constant
`PYJASPER_SERVLET_URL`. If that fails it tries to read `PYJASPER_SERVLET_URL` from the environment.
Finally it falls back to `http://localhost:8080/pyJasper/jasper.py`.
"""

# Created by Maximillian Dornseif on 2007-10-12.
# Moved into huTools in 2010
# Consider it BSD licensed.


from cStringIO import StringIO
from httplib2 import Http
import logging
import os
import os.path
import time
import uuid
import xml.etree.ElementTree as ET


try:
    import config
except:
    config = None


def fetch_httplib2(url, content, content_type):
    """Fetch an url with httplib2"""
    resp, content = Http().request(url, 'POST', body=content, headers={"Content-Type": content_type})
    return resp.get('status'), content


def fetch(url, content, content_type):
    "fetch an url via appengine"
    try:
        result = urlfetch.fetch(url=url,
                                payload=content,
                                method=urlfetch.POST,
                                headers={'Content-Type': content_type},
                                deadline=10)
    except urlfetch.DownloadError, msg:
        logging.error('Error during access to %s: %s' % (url, msg))
        raise
    return str(result.status_code), result.content


# Try to use appengine specific code to incerase appengine default timeout of 5 sec to 10 sec
try:
    from google.appengine.api import urlfetch
    logging.info("using urlfetch for pyJasper")
except ImportError:
    fetch = fetch_httplib2
    logging.info("using httplib2 for pyJasper")


class JasperException(RuntimeError):
    """This exception indicates Jasper Server problem."""
    pass


def encode_multipart_formdata(fields):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    # Based on From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
    boundary = '----------ThIs_Is_tHe_bouNdaRY_$%s' % (uuid.uuid4())
    out = []
    # if it's dict like then use the items method to get the fields
    if hasattr(fields, "items"):
        fields = fields.items()
    for (key, value) in fields:
        out.append('--' + boundary)
        out.append('Content-Disposition: form-data; name="%s"' % key)
        out.append('')
        out.append(value)
    out.append('--' + boundary + '--')
    out.append('')
    body = '\r\n'.join([str(x) for x in out])
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body


def get_reportname(base, *args):
    """
    Construct path for report file relative to base

    In most cases, this will be JasperGenerator.__file__
    """
    path = os.path.join(os.path.dirname(base), 'reports', *args)
    return os.path.abspath(path)


class JasperGenerator(object):
    """Abstract class for generating Documents out with Jasperreports.

    You have to overwrite generate_xml to make meaningfull use of this class. Then call
    YourClass.generate(yourdata). Yourdata is passed to generate_xml() and hopfully you will get
    the generated report back.
    """

    def __init__(self, serverurl=None, debug=False):
        super(JasperGenerator, self).__init__()
        self.reportname = None
        self.xpath = None
        self.debug = debug
        self.serverurl = serverurl
        if not self.serverurl:
            try:
                self.serverurl = config.PYJASPER_SERVLET_URL
            except:
                self.serverurl = os.getenv('PYJASPER_SERVLET_URL',
                                           default='http://localhost:8080/pyJasper/jasper.py')

    def generate_xml(self, data=None):
        """To be overwritten by subclasses.

        E.g.
        def generate_xml(self, movement):
            ET.SubElement(self.root, 'generator').text = __revision__
            ET.SubElement(self.root, 'generated_at').text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            xml_movement  =  ET.SubElement(xmlroot, 'movement')
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
        url = self.serverurl
        if multi:
            content_type, content = encode_multipart_formdata(fields=dict(designs=design, xpath=xpath,
                                                                      xmldata=xmldata))
        else:
            content_type, content = encode_multipart_formdata(fields=dict(design=design, xpath=xpath,
                                                                      xmldata=xmldata))

        logging.info('POSTing %d bytes to %s' % (len(content), url))
        start = time.time()
        status, content = fetch(url, content, content_type)
        logging.debug('POSTing to %s took %f seconds' % (url, time.time() - start))

        if not status == '200':
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
