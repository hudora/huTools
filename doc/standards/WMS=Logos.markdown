# Mapping Hudora - Gigatron Logos

Dieses Dokument erläutert das Feldmapping zwischen den [Hudora
Kommunikationsstandards][hudorastd] und den Gigaron Logos
[Fulfillment-Schnittstellen][fullfillmentstd]. Grundlage ist die Gigaton
Dokumentation Fulfillment-Schnittstellen_2.1.doc vom 2009-02-23 und die
Version ffbedc6a vom 2009-12-23 der Hudora Kommunikationsstandards.

[fullfillmentstd]: https://docs.google.com/fileview?id=0B7xPOoNiQG1oMjU3YTkwNmUtMWVjOS00MGNiLTg5ZjEtMzk2ZjM4ZGI5MmEw&hl=de
[hudorastd]: http://github.com/hudora/huTools/tree/master/doc/standards/

Grundsätzlich passen die Schnittstellen sehr gut zusammen. In fast allen
Fällen, ist ein einfaches Feld-Mapping möglich. Neben einem programmatischen
Ansatz können hierzu, können [XSLT Stylesheets][xslt] oder spezielle Mapping
Tools verwendet werden. Tools hierzu sind [Altanova Mapforce][mapforce],
[Stylus Studio XML Mapper][stylusstudio] oder
[Axizon Tiger XSLT Mapper][tiger].

[xslt]: http://de.wikipedia.org/wiki/XSL_Transformation
[mapforce]: http://www.altova.com/mapforce/
[stylusstudio]: http://www.stylusstudio.com/xml_mapper_screenshot.html
[tiger]: http://www.axizon.com/

Grundsätzlich können die con Hudora gelieferten Daten auf die Logos
CSV-, Tabellen- oder XML-Schnittstelle gemappt werden. Rein technisch ist
das XML-Mapping am einfachsten zu realisieren. Die Lizenzisierungspolitik
von gigaton mag aber ein Mapping auf die CSV-Schnittstelle wirtschaftlicher
erscheinen lassen.

Wenn XML verwendet wird, können durch die oben genannten XSLT-Stylesheets
die meisten Konvertierungsanforderungen erfüllt werden, ohne dass
Programmanpassungen nötig sind. Ich habe für den Warenzugang und für
Kommiaufträge je ein Beispiel XSLT-Stylesheet erstellt. Der Zeitaufwand für
beide Stylesheets war knapp dreiviertel Stunde.


## Problembereiche

Ich werde hier nur die Bereiche nennen, die nicht durch ein XSLT Stylesheet
gelöst werden können.

Der Wareneingang kann 1:1 abgebildet werden. Allerdings ist die Bedeutung des
Feldes `EinlagererNr` bisher unklar.

Der Warenausgang kann fast 1:1 abgebildet werden. Die Befüllung des Feldes
`EinlagererNr` ist unklar.

Unklar ist auch noch, wie mit Lieferfenstern und gesonderten
Versandanweisungen umgegangen werden kann. Lieferfenster werden bei Hudora
durch das Feld `liefertermin_ab`` gekennzeichnet.

Problematisch ist die Übermittlung von (mehreren) besonderen
Verandanweisungen. Diese werden von Logos scheinbar in der
Fullfillmentschnittstelle zur Zeit nicht so recht unterstützt. Eine
Möglichkeit wäre, die Anweisungen von Hudora zusammen in das Feld
"Kommissioniertext" zu kopieren. Inweiweit das eine Lösung sein kann,
hagt von den Abläufen im Lager ab.

Bei der Rückmeldung ist unklar, ob und wie Logos die genaue Zuordung von
Artikel zur Ladeeinheit übermitteln kann.

# Die einzelnen Nachrichten

## Warenzugang / Auftragsliste - Wareneingang

Der "Warenzugang" in der *inventory control - WMS* entspricht der
*Auftragsliste-Wareneingang* in Logos. Eine Warenzugangsnachricht entspricht
dem `Auftragsliste/Auftrag/` Pfad in der Logos XMl Schnittstelle.

* Auftragskopf/FremdlieferscheinNr **guid** Die Fremdlieferscheinnummer muss
  absolut eindeutig sein, sodass ein einwandfreier Import der Daten
  gewährleistet ist. 
* Auftragskopf/KundenauftragsNr **batchnr** Die Kundenauftragsnummer kann zur
  zusätzlichen Auftragsreferenzierung angegeben werden.
* Auftragspositionen/Position/MengeEH1 **menge** In diesem Feld muss die
  Menge des einzulagernden Artikel in der kleinsten Einheit angegeben werden.
* Auftragspositionen/Position/ArtikelNr **artnr** In diesem Feld muss die
  Artikelnummer des einzulagernden Artikels übergeben werden. 
* Auftragspositionen/Position/Charge  **referenzen/charge** In diesem Feld
  kann die Charge des Artikels angegeben werden. 

EinlagererNr und Lieferantenanschrift wird in einer Warenzugangsnachricht
*nicht* übermittelt - diese Daten müssen von einem Converter nachgepflegt
werden.

Nach der Hudora *inventory control - WMS* wird immer nur eine Positin pro
Nachricht erzeugt - d.h. ein Physischer Wareneingang kann zu Mehrereren Duzend
Warenzugangs Nachriten führen. Der `guid` ist aber auf jeden Fall eindeutig.


## Kommiauftrag / Auftragsliste - Warenausgang

Der "Kommiauftrag" in der *inventory control - WMS* erntspricht der
*Auftragsliste-Warenausgang* in Logos. Eine Warenzugangsnachricht entspricht
dem `Auftragsliste/Auftrag/` Pfad in der Logos XMl Schnittstelle.

* Auftragskopf/FremdlieferscheinNr **kommiauftragsnr** Die
  Fremdlieferscheinnummer muss absolut eindeutig sein, so dass ein
  einwandfreier Import der Daten gewährleistet ist. Anhand dieser
  Fremdlieferscheinnummer kann auch ein Auftragsupdate durchgeführt werden,
  dies funktioniert allerdings nur, wenn der Auftrag noch nicht bearbeitet
  wurde. 
* Auftragsinformationen/Liefertermin **anliefertermin** wird im 
  [RfC 3339][rfc3339]
  Format übergeben. Zusammenspiel mit `Terminart` und dem optionalen Feld
  `versandtermin_ab` ist noch unklar **(Konvertierungsbedarf)**
* Auftragsinformationen/Auftragsprioritaet **prioritaet** - ist von Seiten
  Hudora ein nummerischer Wert zwischen 1 und 9, wobei "1" bedeutet, dass
  der Auftrag am dringensten ist.
* Auftragskopf/KundenauftragsNr **auftragsnr**
* Auftragsinformationen/Textcode1 sollte fix mit dem Wert "8" befüllt
  werden
* Auftragsinformationen/Auftragstext **info_kunde**
* Auftragsinformationen/Textcode2 sollte fix mit dem Wert "2" befüllt
  werden
* Auftragsinformationen/Kommissioniertext 
* Auftragsinformationen/EmpfaengerILN **iln**
* Empfaengeranschrift/EmpfaengerkundenNr **kundennr**
* Empfaengeranschrift/EmpfaengerName1 **name1**
* Empfaengeranschrift/EmpfaengerName2 **name2** 
* Empfaengeranschrift/ELaenderkennzeichen **land** ([ISO 3166][iso3166],
  2-letter country code)
* Empfaengeranschrift/EPLZ **plz** das Feld ist optional, da es in manchen
  Ländern (z.B. Irland) keine PLZ gibt
* Empfaengeranschrift/EOrt **ort**
* Empfaengeranschrift/EStrasse **strasse** das Feld ist optional, da es manche
  Adressen ohne Strasse gibt
* Empfaengeranschrift/ETelefonNr **tel**
* Empfaengeranschrift/EEmail **mail**
* Auftragspositionen/Position/ArtikelNr **artnr**
* Auftragspositionen/Position/MengeEH1 **menge**
* Auftragspositionen/Position/FremdPos1 **posnr**
* Auftragspositionen/Position/Warenbezeichnung **text**
* Auftragspositionen/Position/EAN **ean**

[rfc3339]: http://www.faqs.org/rfcs/rfc3339.html
[iso3166]: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

Nicht befüllt:

* Auftragskopf/EinlagererNr **(Klärungs-/Konvertierungsbedarf)**


# Rückmeldung / Rückmeldung Warenausgang 

* Auftragskopf/FremdlieferscheinNr **kommiauftragsnr**
* Auftragspositionen/Position/FremdPos1 **posnr**
* Auftragspositionen/Position/MengeEH1 **menge**
* Auftragspositionen/Position/ArtikelNr **artnr**
* Auftragspositionen/Position/Packstuecknummer **nve**
* Auftragspositionen/Position/Charge **referenzen/charge**

Unklar ist, ob das Fels "Packstuecknummer" ausreicht, um DESADV-äquivalente
Daten zu erstellen. **(Klärungs-/Konvertierungsbedarf)**