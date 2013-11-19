# encoding: utf-8
"""
Client for Google Cloud Print

Created by Christian Klein on 2013-11-04.
Copyright (c) 2013 HUDORA. All rights reserved.
"""
import base64
import httplib2
import json
import mimetools
import mimetypes
import pprint
import urlparse

import huTools.http
from huTools.http.poster_encode import multipart_encode

from oauth2client.client import SignedJwtAssertionCredentials


BASE_URL = 'https://www.google.com/cloudprint/'


def get_http(userid, keyfile):
    """Return authorized HTTP class"""
    key = open(keyfile).read()
    credentials = SignedJwtAssertionCredentials(
        userid,
        key,
        scope="https://www.googleapis.com/auth/cloudprint")

    connection = credentials.authorize(httplib2.Http())
    return connection


def list_jobs(connection, printerid=None):
    """List printjobs"""
    url = urlparse.urljoin(BASE_URL, 'jobs')
    if printerid:
        url = huTools.http.tools.add_query(url, {'printerid': printerid})
    response, content = connection.request(url)
    data = json.loads(content)
    return data


def list_printers(connection):
    """List all printers"""
    url = urlparse.urljoin(BASE_URL, 'search')
    response, content = connection.request(url)
    data = json.loads(content)
    return data


def info(connection, printerid):
    """Retrieve information on printer"""
    url = huTools.http.tools.add_query(urlparse.urljoin(BASE_URL, 'printer'), {'printerid': printerid})
    response, content = connection.request(url)
    data = json.loads(content)
    return data


def share_printer(connection, printerid, email, role='USER'):
    """Share printer with user"""

    url = huTools.http.tools.add_query(urlparse.urljoin(BASE_URL, 'share'),
                                       {'printerid': printerid, 'scope': email, 'role': role})
    response, content = connection.request(url)
    data = json.loads(content)
    return data


def encode(fileobj):
    """Kodiere Datei für GCP-Druckauftrag"""
    mimetype = mimetypes.guess_type(fileobj.name)[0]
    # PDF-Dateien müssen zu Data-URL konvertiert werden
    if mimetype == 'application/pdf':
        content = 'data:%s;base64,' % mimetype
        content += base64.b64encode(fileobj.read())
        mimetype = 'dataUrl'
    else:
        content = fileobj.read()

    return mimetype, content


def create_printer(connection, name, fileobj, proxy='LvP'):
    """Create printer"""

    filedata = fileobj.read().decode('utf-8')
    params = {
        'printer': name,
        'proxy', proxy,
        'status': 'OK',
        'defaults': filedata,
        'capabilities': filedata,
    }

    url = urlparse.urljoin(BASE_URL, 'register')
    datagen, headers = multipart_encode(params)
    response, content = connection.request(url, method='POST', body=''.join(datagen), headers=headers)
    data = json.loads(content)
    return data


def submit_job(connection, printerid, fileobj, title=''):
    """Submit printjob to printer"""

    mimetype, content = encode(fileobj)

    params = {
        'printerid': printerid,
        'title': title,
        'contentType': mimetype,
        'content': content,
        'capabilities': '{"capabilities":[]}'
    }

    url = urlparse.urljoin(BASE_URL, 'submit')
    datagen, headers = multipart_encode(params)
    response, content = connection.request(url, method='POST', body=''.join(datagen), headers=headers)
    data = json.loads(content)
    return data


if __name__ == '__main__':
    MY_FIRST_PRINTER = 'ad13cf5a-e21a-3c19-0e33-deb9cfea8011'

    userid = 'userid'
    filename = '/Users/cklein/Downloads/keyid-privatekey.p12'
    httpconnection = get_http(userid, filename)
    # create_printer('TEST', open('/Users/cklein/Desktop/Brother HL-2030 series CUPS'))
    # print info(httpconnection, MY_FIRST_PRINTER)
    # pprint.pprint(list_printers(httpconnection))
    # print list_jobs(httpconnection)
    # print list_jobs(httpconnection, MY_FIRST_PRINTER)
    response = submit_job(httpconnection, NAPSTER, open('/Users/cklein/Desktop/lena.pdf'))
    print response
