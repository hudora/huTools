# Lieferung Protocol

This is the standard way we encode information about goods beeing send somewhere at HUDORA. The *Lieferung
Protocol* can be implemented in XML, [JSON](http://www.json.org/), as object attributes in your programming
language of choice or whatever. The field names are in German. Consider them a "terminus technicus". This
helps to avoid name clashes with other formats.
The *Lieferung Protocol* ist designed to be easy to encode in a wide range of formats.

The following description is in German.

## Grundsätzliches

Für alle Nachrichten gilt, das unbekannte Felder (also alle hier nicht spezifizierten XML-Tags) ignoriert
werden müssen. So kann es bspw. vorkommen, das sich Felder zu statistischen Zwecken in der Nachricht
befinden. Diese haben jedoch keine Auswirkung auf die Funktion und dürfen deshalb nicht behandelt werden.


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

Die ist ein minimales Beispiel in [Plain Old XML (POX)](http://en.wikipedia.org/wiki/Plain_Old_XML): Als umgebener Container wird hier "kommiauftrag" verwendet.

    <kommiauftrag>
     <guid>93655290_65aaL11e0_ac31Q6fca6bf812354</guid>
     <name1>Mega-Sport</name1>
     <name2>GmbH &amp; Co KG</name2>
     <strasse>Zusestraße 6</strasse>
     <land>BE</land>
     <plz>5613</plz>
     <ort>Eupen</ort>
     <positionen>
      <position>
       <menge>4</menge>
       <artnr>10800</artnr>
       <guid>916008efc09116e7a0a2e237dd64c709</guid>
      </position>
     </positionen>
    </kommiauftrag>

Ein etwas umfangreicheres Beispiel:

    <kommiauftrag>
     <guid>KA3185120</guid>
     <name1>Mega-Sport</name1>
     <name2>GmbH &amp; Co KG</name2>
     <strasse>Zusestraße 6</strasse>
     <land>BE</land>
     <plz>5613</plz>
     <ort>Eupen</ort>
     <anliefertermin>2011-02-21</anliefertermin>
     <anliefertermin_ab>2011-02-21</anliefertermin_ab>
     <auftragsnr>SO1173959</auftragsnr>
     <info_kunde />
     <komminr>KA3185120</komminr>
     <kundennr>SC0350</kundennr>
     <palettenzahl>1.0476190476190477</palettenzahl>
     <gewicht>190000</gewicht>
     <volumen>235<volumen>
     <prioritaet>7</prioritaet>
     <kostenrechnung>
      <einzelstueck>0</einzelstueck>
      <gewichtszuschlaege>0</gewichtszuschlaege>
      <paletten>0</paletten>
      <ve1>0</ve1>
      <ve2>18</ve2>
     </kostenrechnung>
     <packanweisungen>
      <buendelungsvorgaenge>7</buendelungsvorgaenge>
      <originalkartons>0</originalkartons>
      <palettenversand>False</palettenversand>
      <sammelkartons>0</sammelkartons>
     </packanweisungen>
     <positionen>
      <position>
       <artnr>12566</artnr>
       <guid>3185120-001-001</guid>
       <menge>16</menge>
       </position>
      <position>
       <artnr>14910</artnr>
       <guid>3185120-002-002</guid>
       <menge>3</menge>
       </position>
      <position>
       <artnr>76999</artnr>
       <guid>3185120-003-004</guid>
       <menge>12</menge>
       </position>
      <position>
       <artnr>71653</artnr>
       <guid>3185120-004-003</guid>
       <menge>5</menge>
       </position>
     </positionen>
     <versandanweisungen>
      <versandanweisung>
       <anweisung>Versand unfrei</anweisung>
       <bezeichner>unfrei</bezeichner>
       <guid>KA3185120-unfrei</guid>
      </versandanweisung>
    </versandanweisungen>
   </kommiauftrag>


## Referenzen

[AddressProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown#readme) and [VerySimpleOrderProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorderprotocol.markdown#readme).
