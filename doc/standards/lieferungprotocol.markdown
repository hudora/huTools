# Lieferung Protocol

This is the standard way we encode information about goods beeing send somewhere at HUDORA. The *Lieferung
Protocol* can be implemented in XML, [JSON](http://www.json.org/), as object attributes in your programming
language of choice or whatever. The field names are in german. Consider them a "terminus technicus". This
helps to avoid name clashes with other formats.

The *Lieferung Protocol* ist designed to be easy to encode in a wide range of formats.

## per Lieferung 

### Required Fields

 * all fields required by the [AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown) - they encode the delivery address.

### Optional fields

 * *anlieferdatum* - the date at which point in time the goods should be delivered. 
 * *anlieferdatum_max* - latest date for delivery. If set, _anlieferdatum_ is the first day for delivery.
 * *versanddatum* - date when the goods should be shipped
 * *kundennr* - internal id of the recipient
 * *auftragsnr* - internal order id
 * *auftragsnr_kunde* - id of the order submitted by the customer
 * *lieferscheinnr* - id of the delivery note
 * *volumen* - volume of the whole _Lieferung_ in _liters_ 
 * *gewicht* - weight of the whole _Lieferung_ in _gramms_
 * *paletten* - numbers of [EPAL-Pallets](http://de.wikipedia.org/wiki/Europoolpalette) used for transport.
 * *kartons* - number of export-packages
 * *positionen* - a list of positions/orderlines.

## Per Position

### Required Fields

 * *menge* - quantity of the goods
 * *artnr* - internal id of the goods

### Optional fields

 * *name* - descriptive name of the goods
 * *volumen* - volume of the Position in _liters_
 * *gewicht* - weight of the Position in _gramms_
 * *paletten* - numbers of [http://de.wikipedia.org/wiki/Europoolpalette EPAL-Pallets] used for transport.
 * *kartons* - number of export-packages

## Additional Explanation

Field length is not defined. We have seen that field lengths longer than 32 characters have a high
propability of being truncated.

Dates should be represented in the default [ISO 8601 Format](http://en.wikipedia.org/wiki/ISO_8601) YYYY-MM-DD.

## Examples

### XML

This example encodes the address protocol as [Plain Old XML (POX)](http://en.wikipedia.org/wiki/Plain_Old_XML):

    <lieferung> 
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
      <anlieferdatum>2007-09-23</anlieferdatum>
      <kundennr>4711</kundennr>
      <paletten>2.6</paletten>
      <positionen>
          <menge>234</menge>
          <artnr>08/15</artnr>
          <name>Nasenschoner</name>
      </positionen>
    </lieferung >


### JSON

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
     "email": "nobody@hudora.de",
     "anlieferdatum": "2007-09-23",
     "kundennr": "4711",
     "paletten": 2.6,
     "positionen": {
        "menge: 234,
        "artnr": "08/15",
        "name": "Nasenschoner"}}


## See Also

[AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown#readme) and [VerySimpleOrderProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorderprotocol.markdown#readme).