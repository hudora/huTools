# Very Simple Order Protocol Version 3a

Das *Very Simple Order Protocol* ist ein Weg, Lieferaufträge an HUDORA zu senden. In der Regel ist es auf Dreiecksgeschäfte gerichtet, wo unsere Kunden nicht nur die Ware bei uns kaufen, sondern als zusätzliche Dienstleistung das Fullfillment Endverbrauchern gegenüber ("Dropshipping"). Das Protokoll baut auf dem [AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown) auf.

Das *Very Simple Order Protocol* wurde entwickelt, um in möglichst vielen Umgebungan abbildbar zu sein. Das bevorzugte Format ist jedoch XML oder JSON. Der bevorzugte Transportweg ist [FMTP](http://github.com/hudora/huTools/blob/master/doc/standards/fmtp.markdown).


## Pflichtfelder

* Pflichtfelder des [AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown)
 * __name1__ - Primärer Name, der den Empfänger identifiziert
 * __name2__ - weitere Informationen zum Empfänger. Muss vorhanden sien, kann aber leer bleiben
 * __strasse__ - addressing information, usually the street address. might be empty.
 * __land__ - Empfängerland (ISO 3166, 2-letter country code)
 * __plz__ - Postleitzahl, kann leer bleiben (z.B.. in Irland).
 * __ort__ - Stadt des Empfängers
* __guid__ - Eindeutiger ID des Vorgangs, darf niemals doppelt verwendet werden - der inhalt des Feldes ist beliebig, Zeitstempel+Auftragsnummer funktionieren z.B. recht gut als GUID.
* __orderline/guid__ - Eindeutiger ID der Position. GUID des Auftrags + Positionsnummer funktionieren ganz gut.
* __orderline/menge__ - Menge des durch *ean* bezeichneten Artikels, die versendet werden soll.
* __orderline/ean__ - EAN des zu versendenen Artikels.


## Optionale Felder

* optionale Felder des [AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown)
 * __tel__ - Telefonnummer für die Anlieferung ([DIN 5008][6] or [E.123][7])
 * __fax__ - Faxnummer für die Anlieferung ([DIN 5008][6] or [E.123][7])
 * __mail__ - E-Mail address relevant to the address/delivery
 * [GLN][8], die eindeutige Nummer der Firma/Lieferadresse [vergeben von GS1][9]
* __kundenauftragsnr__ - Freitext, den der Kunde bei der Bestellung mit angegeben kann, 20 Zeichen. Erscheint auf allen weiteren Belegen.
* __infotext_kunde__ - Freitext, der sich an den Warenempfänger richtet. Kann z.B. auf einem Lieferschein angedruckt werden. Der Umbruch des Textes kann durch das Backendsystem beliebig erfolgen, deshalb sollte der Text keine Zeilenumbrüche beinhalten. Sollte nciht luanger als 256 Zeichen sein.
* __orderline/infotext_kunde__ - Freitext, der sich an den Warenempfänger richtet. Wird nicht bei allen Versandwegen angedruckt.
* **wunschdatum_von** und **wunschdatum_bis** Timestamps im [RfC 3339](http://www.ietf.org/rfc/rfc3339) format. Dieses Feld kann nur nach gesonderter Vereinbarung befüllt werden. Die Verwendung des Feldes zieht zusätzliche Kosten nach sich.
* __dokumente__ - Eine Liste von PDFs, die ausgedruckt und mit der Ware versendet werden sollen. Details siehe untern.

[6]: http://de.wikipedia.org/wiki/Rufnummer#Schreibweise_in_Deutschland_und_.C3.96sterreich
[7]: http://en.wikipedia.org/wiki/E.123
[8]: http://en.wikipedia.org/wiki/Global_Location_Number
[9]: http://www.gs1.org/glnrules/storyboard/

## Beispiele

### XML

Dieses Beispiel codiert das Order Protocol als  [Plain Old XML (POX)](http://en.wikipedia.org/wiki/Plain_Old_XML). Bei der Verpackung in XML können mehrere Bestellungen in einer einzigen Datei transportiert werden, indem die `<order>` Elemente als Kinder eines `<orders>` Elementes angeordnet werden. Das Vorhandensein eines `<orders>` Elementes ist verpflichtend, auch wenn nur ein `<order>` Element übertragen wird.

    <orders>
      <order>
        <guid>2008-08-21T15:16:17-id1222</guid>
        <name1>HUDORA GmbH</name1>
        <name2>Abt. Cybernetics</name2>
        <name3></name3>
        <strasse>Jägerwald 13</strasse>
        <land>DE</land>
        <plz>42897</plz>
        <ort>Remscheid</ort>
        <tel>+49 2191 60912 0</tel>
        <fax></fax>
        <mobil></mobil>
        <email>nobody@hudora.de</email>
        <orderline>
           <guid>2008-08-21T15:16:17-id1222-pos1</guid>
           <menge>1</menge>
           <ean>4005998651698</ean>
           <infotext_kunde>Gartentrampolin ArtNr 65123</infotext_kunde>
        </orderline>
        <kundenauftragsnr>XQ03244231</kundenauftragsnr>
        <infotext_kunde>Lieferung im Auftrag der "Kawuschel Sportausrüstung AG"</infotext_kunde>
        <wunschdatum>
            <von>2009-08-21T00:00:00</von>
            <bis>2009-08-24T23:59:59</bis>
        </wunschdatum>
        <dokumente>
            <file name="rechnung.pdf" contenttype="application/pdf">R0lGODlhZABqA...</file>
            <file name="garantieschein.pdf" contenttype="application/pdf">GODlhZABqA...</file>
        </dokumente>
      </order>
    </orders>

#### PDF Dateien in XML

Per XML können keine oder mehrere PDF-Dateien mit übergeben werden. Dazu kann ein `<dokumente>` Element verwendet werden, in dem ein oder mehrere `<file>` Elemente PDF Dateien kodieren. Jedes File Element muss ein Attribut `contenttype="application/pdf"` haben und ein `name` Attribut. Das Name Attribut darf nur die Zeichen A-Za-z0-9._- beinhalten. Innerhalb einer `<order>` darf kein `name` Attribut doppelt vorkommen.

Die Daten selbst werden BASE-64 kodiert. Der Inhalt sollte kompatibel zu PDF-1.3 / ISO 15930-2001 und nicht grösser als 1 MB sein. Es dürfen maximal 5 Dateien pro `<order>` übertragen werden.


### CSV

Das Order Protocol kann *zur Not* auch als CSV kodiert werden. Gennerell ist jedoch davon abzuraten, weil es zu Kodierungsproblemen mit Umlauten und Sonderzeichen, wie ";:`,.'| kommen kann. Weiterhin kann nur eine Orderline pro Auftrag per CSV übertragen werden.

Wenn doch CSV verwendet wird, ist UTF-8 Kodierung zu verwenden. Das Trennzeichen ist `,` Quoting erfolgt durch `"`. Soll das Quotingzeichen in einem String vorkommen ist es zu verdoppeln. Zeilen werden durch \r\n (Hex: 0a0d) beendet. Die erste Zeile muss eine Formatbeschreibung beinhalten und mit # beginnen. Alle weiteren Zeilen, die mit # beginnen, werden ignoriert. Wir verwenden den [Python CSV Parser](http://docs.python.org/lib/module-csv.html) zum Einlesen der Daten.

    # guid,name1,name2,name3,strasse,land,plz,ort,tel,fax,mobil,email,menge,ean,kundenauftragsnr,infotext_kunde
    "2008-08-21T15:16:17-id1222","HUDORA GmbH","Abt. Cybernetics","","Jägerwald 13","DE","42897","Remscheid","+49 2191 60912 0","","","nobody@hudora.de","1","4005998651698","XQ03244231","Lieferung im Auftrag der ""Kawuschel Sportausrüstung AG"""

## Unterscheide zu Version 1

* Das guid Feld ist hinzugekommen
* das `<orders>` Element in der XML Repräsentation wurde hinzugefügt.

## Unterscheide zu Version 2

* es muss ein oder mehrere `<orderline>` Elemente geben.
* orderline hat guid und infotext_kunde felder hinzubekommen
* `<wunschtermin>`

## Unterscheide zu Version 3

Version 3a hat `<wunschtermin>` in `<wunschdatum_von>` und `<wunschdatum_bis>` umbenannt.

## Siehe auch

* [AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown)
* [VerySimpleStatusProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/verysimplestatusprotocol.markdown)
* [LieferungProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/lieferungprotocol.markdown)
* UBL [Ordering](http://docs.oasis-open.org/ubl/cs-UBL-2.0/UBL-2.0.html#d0e1620)
* EDIFACT [ORDERS](http://www.edifactory.de/msginfo.php?s=D08A&m=ORDERS)
