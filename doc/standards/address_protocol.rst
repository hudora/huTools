Very Simple Address Protocol
============================

This is the standard way we encode addresses at Hudora_. The *Address Protocol* can be implemented in XML,
JSON_, as object attributes in your programming language of choice or whatever.
The field names are in german. Consider them a "terminus technicus". This helps to avoid name clashes with
other formats.

.. _Hudora: http://www.hudora.de/
.. _JSON: http://www.json.org/

The *Address Protocol* ist designed to be easy to encode in a wide range of formats.

Required Fields
---------------

 * **name1** - primary name identifying the recipient 
 * **name2** - additional information identifying the recipient or additional adressing information. May be empty.
 * **strasse** - addressing information, usually the street address. might be empty. 
 * **land** - country (`ISO 3166`, 2-letter country code)
 * **plz** - zip code, might be empty (e.g. in Ireland_. Note that even `in the US the ZIP code is sufficient for adressing`_, the name of the State is redundant)
 * **ort** - city name

.. _`ISO 3166`: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
.. _Ireland: http://en.wikipedia.org/wiki/Postal_code#Ireland
.. _`in the US the ZIP code is sufficient for adressing`: http://en.wikipedia.org/wiki/ZIP_Code#By_geography

Optional fields
---------------

 * **name3** - additional information identifying the recipient or additional adressing information. May be dropped during processing. *Put noting important in here*!
 * **tel** - phone number relevant to the address/delivery (formated like `DIN 5008`_ or `E.123`_)
 * **fax** - fax number relevant to the address/delivery (formated like DIN 5008 or E.123)
 * **mobil** - additional phone number relevant to the address/delivery (formated like DIN 5008 or E.123)
 * **mail** - E-Mail address relevant to the address/delivery
 * **iln** - GLN_, the worldwide uniqe number of that company/address `allocated by GS1`_

.. _`DIN 5008`: http://de.wikipedia.org/wiki/Rufnummer#Schreibweise_in_Deutschland_und_.C3.96sterreich
.. _`E.123`: http://en.wikipedia.org/wiki/E.123
.. _GLN: http://en.wikipedia.org/wiki/ILN
.. _`allocated by GS1`: http://www.gs1.org/glnrules/storyboard/

Additional Explanation
----------------------

Field length is not defined. We have seen that field lengths longer than 32 characters have a high propability
of beeing truncated. Based on E.164 Phone, Fax and Mobile Numbers should
not be longer than 19 characters (15 digits  and one '+' one '-' and two spaces). PLZ should `never be longer than 10 characters`_.

.. _`never be longer than 10 characters`: http://de.wikipedia.org/wiki/Postleitzahl#Postleitzahlen_in_der_Datenverarbeitung

All information should be related to the (delivery) address. If we for example talking about an order, the
Phone Number should not be the person who ordered (e.g. the office) but the person who can give information about
delivery (e.g. the warehouse). In practice this is often the same.

The E-Mail address might be used to send delivery status messages.

*ISO 3166-1 alpha-2* country codes are the the codes you now from internet top level domain names. FR, BE, CH, AT, UK, US, DE, etc.



Examples
--------

XML
~~~

This example encodes the address protocol as [http://en.wikipedia.org/wiki/Plain_Old_XML Plain Old XML (POX)]::

    <address> 
      <name1>HUDORA GmbH</name1>
      <name2>Abt. Cybernetics</name2>
      <name3>Anlieferung: Tor 2</name3>
      <strasse>Jägerwald 13</strasse>
      <land>DE</land>
      <plz>42897</plz>
      <ort>Remscheid</ort>
      <tel>+49 2191 60912 0</tel>
      <fax>+49 2191 60912 50</fax>
      <mobil>+49 175 00000xx</mobil>
      <email>nobody@hudora.de</email>
      <iln>4005998000007</iln>
    </address>

HTML
~~~~

This example combines the adress protocol and [http://microformats.org/wiki/hcard hCard] microformat
into Plain Old Semantic HTML (POSH). This can be created from the XML-Example above by using an
XSLT stylesheet::


    <div id="hcard-example" class="vcard deHudoraAddress">
      <div>
        <span class="name1 org fn">HUDORA GmbH</span><br />
        <span class="name2 extended-address">Abt. Cybernetics</span><br/>
        <span class="name3 extended-address">Anlieferung: Tor 2</span>
      </div>
      <div class="adr">
        <div class="street-address strasse">Jägerwald 13</div>
        <div>
          <span class="country-name land">DE</span>
          <span class="postal-code plz">42897</span>
          <span class="locality ort">Remscheid</span>
        </div>
      </div>
      
      <br/>
      
      <div>
        <div>Tel.:  <span class="tel work">+49 2191 60912 0</span></div>
        <div>Fax:   <span class="tel fax" type="fax">+49 2191 60912 50</span></div>
        <div>Mobil: <span class="tel mobil" type="cell">+49 175 00000xx</span></div>
        <div>Mail:  <a class="email" href="mailto:nobody@hudora.de">nobody@hudora.de</a></div>
        <div>ILN:   <span class="iln">4005998000007</span></div>
      </div>
    </div>


JSON
~~~~

Address encoded in JSON Syntax::

    {"iln": "4005998000007",
     "name1": "HUDORA GmbH",
     "name2": "Abt. Cybernetics",
     "name3": "Anlieferung: Tor 2",
     "strasse": "J\\u00e4gerwald 13", 
     "ort": "Remscheid",
     "plz": "42897",
     "land": "DE",
     "tel": "+49 2191 60912 0",
     "fax": "+49 2191 60912 50",
     "mobil": "+49 175 00000xx",
     "email": "nobody@hudora.de"}



Python
~~~~~~

Address encoded in Python Syntax::

    address = {
      'name1':   'HUDORA GmbH',
      'name2':   'Abt. Cybernetics',
      'name3':   'Anlieferung: Tor 2',
      'strasse': 'Jägerwald 13',
      'land':    'DE',
      'plz':     '42897',
      'ort':     'Remscheid',
      'tel':     '+49 2191 60912 0',
      'fax':     '+49 2191 60912 50',
      'mobil':   '+49 175 00000xx',
      'email':   'nobody@hudora.de',
      'iln':     '4005998000007',
    }


Alternatives
~~~~~~~~~~~~

 * vCard_ and hCard_.
 * EDIFACT NAD_, LOC_ or ADR Segments.

.. _vCard: http://www.imc.org/pdi/vcardoverview.html
.. _hCard: http://microformats.org/wiki/hcard
.. _NAD: http://www.glimbh.eu/edifact/m_1002/m_A/trsd/trsdnad.htm
.. _LOC: http://www.edifactory.de/seginfo.php?s=D07A&g=LOC
.. _ADR: http://www.edifactory.de/seginfo.php?s=D07A&g=ADR


See Also
~~~~~~~~

VerySimpleOrderProtocol and LieferungProtocol.
