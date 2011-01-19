# Lieferung Protocol

This is the standard way we encode information about goods beeing send somewhere at HUDORA. The *Lieferung
Protocol* can be implemented in XML, [JSON](http://www.json.org/), as object attributes in your programming
language of choice or whatever. The field names are in German. Consider them a "terminus technicus". This
helps to avoid name clashes with other formats.
The *Lieferung Protocol* ist designed to be easy to encode in a wide range of formats.

The following description is in German.


## pro Lieferung 

### Pflichtfelder

 * *guid* - eindeutiger Bezeichner der Lieferung. Ein Bezeichner kann doppelt vorkommen, das empfangende System darf dann nur genau eine der Nachrichten verarbeiten.
 * alle Pflichtfelder des [AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown), wie name1, strasse, land,plz, ort.
   Dies kodiert die Lieferadresse
 * *positionen* - Liste der Lieferscheinpositionen, s.u.

### Zusatzfelder

 * *anliefertermin* - Termin, an dem die Ware **spätestens** dem Empfänger übergeben werden muss
 * *anliefertermin_ab* - Termin, an dem die Ware **frühstens** dem Empfänger übergeben werden muss
 * *prioritaet* - Dringlichkeit des Auftrags zwischen 1 und 10, wobei niedrigere Werte dringendere Aufträge bedeuten
 * *gewicht* - Nettogewicht der Waren in Gramm
 * *volumen* - Nettovolumen der Waren in Liter
 * *palettenzahl* - kalkulatorische Zahl der Versandpaletten
 * *packanweisungen/buendelungsvorgaenge* - Zahl der Pakete, die durch Bündeln entstehen sollen
 * *packanweisungen/sammelkartons* - geschätzte Zahl der Sammelkartons
 * *packanweisungen/originalkartons* - Zahl der Pakete, die unverändert versendet werden sollen
 * *kostenrechnung/paletten* - kalkulatorische Zahl der auszulagernden Paletten
 * *kostenrechnung/ve2* - kalkulatorische Zahl der auszulagernden VE2
 * *kostenrechnung/ve1* - kalkulatorische Zahl der auszulagernden VE1
 * *kostenrechnung/einzelstuecke* - kalkulatorische Zahl der auszulagernden Einzelstücke
 * *kostenrechnung/gewichtszuschlaege* - kalkulatorische Zahl der Packstücke, für die ein Gewichtszuschlag fällig wird
 * *kundennr* - Freitext zur besseren Referenzierung, nicht eindeutig, kann aber zum Zusammenfassen von Aufträgen verwendet werden, die vermutlich an die gleiche Adresse gehen.
 * *infotext_kunde* - Freitext, der für den Empfänger Relevanz hat
 * *auftragsnr* - Freitext zur besseren Referenzierung, nicht eindeutig
 * *kundenname* - Freitext zur besseren Referenzierung, nicht eindeutig
 * *auftragsnr_kunde*  - Freitext, der für den Empfänger Relevanz hat
 * *versandanweisungen* - Liste mit Versandanweisungen

## Pro Position

### Pflichtfelder

 * *guid* - eindeutiger Bezeichner der Position
 * *menge* - Menge der Position
 * *artnr* - Artikelnummer der Position

### Zusatzfelder

 * *name* - descriptive name of the goods

### Versandanweisungen
 * *guid* - eindeutiger Bezeichner der Position
 * *bezeichner* - bilateral vereinbarter Leistungsbezeichner (z.B. *avisierung48h*, *selbstabholer*, *hebebuehne*)
 * *anweisungen* - Freitext, der die Packanweisungen beschreibt

## Hinweise

Die Feldlängen sind nicht definiert.
Datumsfelder sollen im [ISO 8601 Format](http://en.wikipedia.org/wiki/ISO_8601) angegeben werden: YYYY-MM-DD

## Beispiele

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


## Referenzen

[AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown#readme) and [VerySimpleOrderProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorderprotocol.markdown#readme).