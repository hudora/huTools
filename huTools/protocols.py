#!/usr/bin/env python
# encoding: utf-8
"""
protocols.py - handle data confoming the the Hudora standard protocols.
See http://github.com/hudora/huTools/tree/master/doc/standards for details.

Created by Maximillian Dornseif on 2009-12-27.
Copyright (c) 2009 HUDORA. All rights reserved.

Code is based on http://code.activestate.com/recipes/573463/
"""

from xml.etree import ElementTree
import os.path
import simplejson as json
import sys


def dicttoxml(datadict, roottag='data'):
    """Converts a dict representing one of the protocoles described in
    http://github.com/hudora/huTools/tree/master/doc/standards to XML.

    Returns an UTF-8 encoded String.

    >>> data = {"kommiauftragsnr":2103839, "anliefertermin":"2009-11-25", "prioritaet": 7,
    ... "ort": u"Hücksenwagen",
    ... "positionen": [{"menge": 12, "artnr": "14640/XL", "posnr": 1},],
    ... "versandeinweisungen": [{"guid": "2103839-XalE", "bezeichner": "avisierung48h",
    ...                          "anweisung": "48h vor Anlieferung unter 0900-LOGISTIK avisieren"},
    ...]}

    >>> print toxml(data, 'kommiauftrag')
    '''<kommiauftrag>
    <anliefertermin>2009-11-25</anliefertermin>
    <positionen>
        <position>
            <posnr>1</posnr>
            <menge>12</menge>
            <artnr>14640/XL</artnr>
        </position>
    </positionen>
    <ort>H&#xC3;&#xBC;cksenwagen</ort>
    <versandeinweisungen>
        <versandeinweisung>
            <bezeichner>avisierung48h</bezeichner>
            <anweisung>48h vor Anlieferung unter 0900-LOGISTIK avisieren</anweisung>
            <guid>2103839-XalE</guid>
        </versandeinweisung>
    </versandeinweisungen>
    <prioritaet>7</prioritaet>
    <kommiauftragsnr>2103839</kommiauftragsnr>
    </kommiauftrag>'''
    """

    root = ElementTree.Element(roottag)
    _ConvertDictToXmlRecurse(root, datadict)
    return ElementTree.tostring(root, 'utf-8')


# defines how listitems are packaged
_listnames = {'positionen': 'position',
             'versandeinweisungen': 'versandeinweisung'}

def _ConvertDictToXmlRecurse(parent, dictitem):
    assert not isinstance(dictitem, type([]))

    if isinstance(dictitem, dict):
        for (tag, child) in dictitem.iteritems():
            if isinstance(child, type([])):
                # iterate through the array and convert
                listelem = ElementTree.Element(tag)
                parent.append(listelem)
                for listchild in child:
                    elem = ElementTree.Element(_listnames.get(tag, tag))
                    listelem.append(elem)
                    _ConvertDictToXmlRecurse(elem, listchild)
            else:
                elem = ElementTree.Element(tag)
                parent.append(elem)
                _ConvertDictToXmlRecurse(elem, child)
    else:
        parent.text = unicode(dictitem)


def test():
    # warenzugang
    data = {"guid":"3104247-7",
            "menge":7,
            "artnr":"14695",
            "batchnr": "3104247"}
    print dicttoxml(data, roottag='warenzugang')

    # kommiauftrag
    data = {"kommiauftragsnr":2103839,
     "anliefertermin":"2009-11-25",
     "fixtermin": True,
     "prioritaet": 7,
     "info_kunde":"Besuch H. Gerlach",
     "auftragsnr":1025575,
     "kundenname":"Ute Zweihaus 400424990",
     "kundennr":"21548",
     "name1":"Uwe Zweihaus",
     "name2":"400424990",
     "name3":"",
     u"strasse":u"Bahnhofstr. 2",
     "land":"DE",
     "plz":"42499",
     "ort": u"Hücksenwagen",
     "positionen": [{"menge": 12,
                     "artnr": "14640/XL",
                     "posnr": 1},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr": 2},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr": 3}],
     "versandeinweisungen": [{"guid": "2103839-XalE",
                              "bezeichner": "avisierung48h",
                              "anweisung": "48h vor Anlieferung unter 0900-LOGISTIK avisieren"},
                             {"guid": "2103839-GuTi",
                              "bezeichner": "abpackern140",
                              "anweisung": u"Paletten höchstens auf 140 cm Packen"}]
    }
    print dicttoxml(data, roottag='kommiauftrag')

    # Rückmeldung
    data = {"kommiauftragsnr":2103839,
     "positionen": [{"menge": 4,
                     "artnr": "14640/XL",
                     "posnr": 1,
                     "nve": "23455326543222553"},
                    {"menge": 8,
                     "artnr": "14640/XL",
                     "posnr": 1,
                     "nve": "43255634634653546"},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr": 2,
                     "nve": "43255634634653546"},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr": 3,
                     "nve": "23455326543222553"}],
     "nves": [{"nve": "23455326543222553",
               "gewicht": 28256,
               "art": "paket"},
              {"nve": "43255634634653546",
               "gewicht": 28256,
                "art": "paket"}]}

    print dicttoxml(data, roottag='rueckmeldung')

if __name__ == '__main__':
    # test()
    # json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4)
    jsondata = open(sys.argv[1]).read()
    data = json.loads(jsondata)
    print dicttoxml(data, os.path.basename(sys.argv[1].split('.')[0]))
