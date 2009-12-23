DRAFT - ENTWURF - DRAFT - ENTWURF - DRAFT - ENTWURF

# Kommunikation inventory control <-> WMS

Im folgenden wird das Kommunikationsprotokoll zwischen einer Warenwirtschaft ("inventory control", IC, ERP)
und einem Lagerverwaltungssystem (LVS, WMS) definiert. Es wird davon ausgegangen, dass Inventory Control
das bestandsführende System ist.

Pro Lager gibt es ein (logisches) WMS. Lager snd mit einem eindeutigen Bezeichner identifiziert, der aber für
die Kommunikation zwischen Inventory Control und einem WMS unbedeutend ist. Inventory Control und WMS
kommunizieren in beide Richtungen asyncron mit Nachrichten und in Richtung Inventory Control -> WMS ->
Inventory contol via REST.

# Nachrichtentypen

Hier ein Überblick über die Nachrichtentypen, die ausgetauscht werden:

* **Warenzugang** von Inventory Control an WMS (asyncron)
* **Kommiauftrag** von Inventory Control an WMS (asyncron)
* **Rücklmeldung** eines Auftrags von WMS an Inventory Control (asyncron)
* **Lieferscheine** von Inventory Control an WMS (asyncron)
* **Prioritaet** update von Inventory Control an WMS (asyncron)
* **Stornierung** von Inventory Control an WMS und **Stornierungsbestaetigung** in Gegenrichtung (asyncron)


# Nachrichten

Im folgenden eine detaillierte Beschreibung der einzelnen Nachrichtentypen.



## Warenzugang

Diese Nachricht wird unmittelbar an das WMS gesendet, wenn die Ware das Lagerphysisch erreicht haben
sollte. Pro Artikel wird eine Nachricht gesendet. GUIDs sollten auf jeden Fall doppelte Zubuchungen
vermeiden. Warenzugänge werden durch das WMS nicht bestätigt. Abweichungen soll/istmenge müssen über
Korrekturbuchungen gelösst werden.

### Pflichtfelder

* **guid** - Eindeutiger Bezeichner der Nachricht. Kann doppelt vorkommen, das WMS darf dann nur
  genau *eine* der Nachrichten verarbeiten.
* **menge** - Integer, repräsentiert die zuzubuchende Menge. Kann vom WMS auf mehrere Ladungsträger
  verteilt werden.
* **artnr** - String, eindeutiger ID der zu lagernden Ware.
* **batchn** - String, der z.B. bei der Identifizierung der Auslagerung genutzt werden kann.

### Zusatzfelder

* **referenzen** - Dict, dass Referenzen enthält, die zur Verarbeitung des Warenzugangs nicht zwingend
  notwendig sind.
* **mui** - Barcode, der bereits auf der Waren angebracht ist. Es wird davon ausgegangen, dass die
  gesammte mit dieser Nachricht zugebuchte Menge auf einem einzigen Ladungsträger ist.


### Beispiel

    {"guid":"3104247-7",
     "menge":7,
     "artnr":"14695",
     "batchnr": "3104247"}


## Kommiauftrag

Die Nachricht wird - möglicherweise viele Tage - vor dem gewünschten Anliefertermin von Incentory Control
an das WMS gesendet.


### Pflichtfelder (Kopf)

* **kommiauftragsnr** - Eindeutiger ID des Kommisionierauftrags. Kann doppelt vorkommen, das WMS
  darf dann nur genau *eine* der Nachrichten verarbeiten.
* **anliefertermin** - Termin, an dem die Ware spätestens beim Kunden sein soll. Wenn der Termin in
  der Vergangenheit liegt, soll sofort ausgeliefert werden.
* **prioritaet** - Dringlichkeit des Auftrags als Wert zwischen 1 bis 10. Niedrige Werte
  bedeuten dringendere Aufträge.


### Zusatzfelder (Kopf)

* **anliefertermin_ab** - Termin ab dem die Ware frühstens beim Kunden sein darf
* **versandtermin** -  Termin an dem die Ware spätestens das Lager verlassen soll
* **versandtermin_ab** - Termin ab dem die Ware das Lager frühstens verlassen darf
* **fixtermin** - Wenn True: Zuspätlieferung kann erhebliche Kosten nach sich ziehen.
* **gewicht** - Netto Gewicht der Ware in Gramm
* **volumen** - Netto Volumen der Ware in Liter
* **kundennr** -  Freitext zur besseren Referenzierung - Nicht eindeutig, kann aber zum Zusammenfassen
  von Komissionierungen genutzt werden, die vermutlich an die gleiche Adresse gehen werden.
* **info_kunde** - Freitext der für den Empfänger relevanz hat, z.B. Kundenauftragsnummer
* **auftragsnr** - Freitext zur besseren Referenzierung - Nicht eindeutig!
* **kundenname** - Freitext zur besseren Referenzierung - Nicht eindeutig!

Weitere Zusatzfelder können alle Felder des [Address Protokolls] (name1, name2, name3, strasse, land,
plz, ort, tel, fax, mobil, email und iln) sein. Diese dienen lediglich der Information.
Die verbindliche Lieferadresse erscheint auf dem Lieferschein.

[Address Protokolls]: http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown

### Positionen

Ein Kommiauftrag kann eine oder mehrere Auftragspositionen beinhalten. Jede Postition besteht aus mehreren
Feldern.

#### Pflichtfelder

* **menge** - Integer, repräsentiert die zuzubuchende Menge. Kann vom WMS auf mehrere Ladungsträger verteilt werden.
* **artnr** - String, Eindeutiger ID der zu komissionnierenden Ware.
* **posnr** - Ergibt zusammen mit *kommiauftragsnr* einen eindeutigen Bezeichner.

#### Zusatzfelder

* **text** - Artikelbeschriebung
* **EAN** - EAN/Barcode des Artikels (nicht der VE). *artnr* ist das verbindliche Auswahlkriterium.


### Versandanweisungen

Ein *Kommiauftrag* kann keine oder mehr Versandanweisngen beinhalten. Jede Versandanweisung besteht aus
mehreren Feldern.

#### Pflichtfelder

* **guid** - Eindeutiger ID der Versandanweisung.
* **bezeichner** - Ein Bezeichner, der immer für diese Art der Versandanweisung verwendet wird
  (vergleichbar mit der *artnr*)
* **anweisung** - Freitext, beschreibt, was zu tun ist.


### Beispiel

    {"kommiauftragsnr":2103839,
     "anliefertermin":"2009-11-25",
     "prioritaet": 7,
     "info_kunde":"Besuch H. Gerlach",
     "auftragsnr":1025575,
     "kundenname":"Ute Zweihaus 400424990",
     "kundennr":"21548",
     "name1":"Uwe Zweihaus",
     "name2":"400424990",
     "name3":"",
     "strasse":"Bahnhofstr. 2",
     "land":"DE",
     "plz":"42499",
     "ort":"Hücksenwagen",
     "positionen": [{"menge": 12,
                     "artnr": "14640/XL",
                     "posnr", 1},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr", 2},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr", 3}],
     "versandeinweisungen": [{"guid": "2103839-XalE",
                              "bezeichner": "avisierung48h",
                              "anweisung", "48h vor Anlieferung unter 0900-LOGISTIK avisieren"},
                             {"guid": "2103839-GuTi",
                              "bezeichner": "abpackern140",
                              "anweisung", "Paletten höchstens auf 140 cm Packen"}]
    }



## Rückmeldung

Diese Nachricht wird vom WMS an Inventory Control gesendet, *sobald ein Kommiauftrag versendet werden soll*.
Sie ist Voraussetzung für die Liefercheingenerierung. Ein Kommiauftrag kann nur genau
einmal rückgemeldet werden.

* **kommiauftragsnr** - Unique ID des Kommiauftrags, der bei der Kommiauftrag Nachricht übertragen wurde.
* **positionen** - Liste der zurückzumeldenen Positionen. Muss IMMER alle Positionen beinhalten, die 
  im  Kommiauftrag mitgesendet wurden. Jede Position wird als Dictionary abgebildet. Positionen können
  mehrfach vormommen.
  Pflichtfelder in jedem Dictionary sind zur Zeit `posnr`, `menge` und `artnr`. Zusatzfeld ist NVE.
* **nves** - Dictionary der Versandeinheiten. Enthält pro Versandeiheit ein Dictionary mit gewicht in Gramm
  und der Art der Versandeinheit. 

### Beispiel

    {"kommiauftragsnr":2103839,
     "positionen": [{"menge": 4,
                     "artnr": "14640/XL",
                     "posnr", 1,
                     "nve": '23455326543222553'},
                    {"menge": 8,
                     "artnr": "14640/XL",
                     "posnr", 1,
                     "nve": '43255634634653546'},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr", 2},
                     "nve": '43255634634653546'},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr", 3},
                     "nve": '23455326543222553'}],
     "nves": {"23455326543222553": {"gewicht": 28256,
                                    "art": paket},
              "43255634634653546": {"gewicht": 28256,
                                    "art": paket}}
   }



## Lieferschein

Der Lieferschein ist das Finale Versanddokument und lösst die Abbuchung der Ware aus dem Lager und die
Rechnungsstellung aus. Er wird auf die Rückmeldung hin erzuegt. Der Lieferschein kann als PDF und/oder als
Datenstruktur an das WMS gesendet werden.

### Lieferschein als PDF

Lieferscheine werden nach Rückmeldung als PDF zur Verfügung gestellt. Dabei sind die Dateien nach der
*kommiauftragsnr* benannt. Für obiges Beispiel z.B. "2103839.pdf". Die Erzeugung von Lieferscheinen dauert
1-2 Minuten.


## Prioritaet

Mit der Prioritaet kann die Priorität von noch-nicht zurückgemeldeten Kommiaufträgen geändert werden.
Die Priorität kann einen Wert zwischen 1 und 9 sein. Niedrigere Werte bei der Priorität bedeuten, dass
der Kommiauftrag dringender ist. Prioritäten haben lediglich Hinweischarakter. Es gibt keine Rückmeldung,
ob die Prioritätsänderung erfolgreich war. 

### Pflichtfelder

* **kommiauftragsnr** - Nummer des Auftrags, dessen Priorität geändert werden soll.
* **prioritaet** - neue Priorität

### Beispiel

    {"kommiauftragsnr":2103839,
     "prioritaet": 3}
  

## Stornierung

Mit einer Storno Nachricht teilt Inventory Control dem WMS den Wunsch mit, dsas ein Kommiauftrag nicht
ausgeführt werden soll. Es liegt beim WMS zu entscheiden, ob ein Storno ausgeführt werden kann. Zu jeder
*Stornierung* muss das WMS eine *Stornierungsbestaetigung* zurück an Inventory Control senden. diese sollte 
spätestens 30 Minuten nach Absenden der *Stornierung* Nachricht bei Inventory Control eintreffen.

Einzelne Positionen in einem Kommiauftrag können nicht storniert oder verändert werden. Es können immer
nur komplette Aufträge storniert werden.


### Pflichtfelder

* **kommiauftragsnr** - Nummer des Auftrags, dessen Priorität geändert werden soll.

### Zusatzfelder

* **verantwortlicher** - Freitext, der die Person, die die Stornierung veranlaßt hat, identifiziert.
* **text** - Weitere Erklärung zur Stornierung.

### Beispiel

    {"kommiauftragsnr":2103839,
     "verantwortlicher": "Hans Mustermann",
     "text": "Kunde hatte sich vertan"}



## Stornierungsbestaetigung

Eine *Stornierungsbestaetigung* wird vom WMS als Antwort auf jede *Stornierung* hin an Inventory Control
gesendet. Die Nachrichst sollte sehr Zeitnah zum Emfang der *Stornierung* Nachricht gesendet werden.

In Notfällen kann das WMS auch selbst eine Stornierungsbestätigung ohne vorherige Stornierungsnachricht
auslösen. Das ist beispielsweise der Fall, wenn eine Unterdeckung vorliegt.


### Pflichtfelder

* **kommiauftragsnr** - Nummer des Auftrags, dessen Priorität geändert werden soll.
* **status** - Ob die Stornierung erfolgt ist. Kann ausschliesslich die Werte "storniert" oder
  "unveraendert" annehmen. Wenn der Kommiauftrag aus dem WMS entfernt wurde und nicht zum Versand kam,
  wird "storniert" zurückgesendet. Wenn ein Storno nicht möglich ist, weil z.B. die Ware schon versendet
  wurden, wird der Status "unveraendert" zurückgemeldet.


### Beispiel

    {"kommiauftragsnr":2103839,
     "status": "storniert"}




# Unspezifizierte Nachrichten

Beständsveränderungen ausserhalb von Warenzugängen, z.B. durch Korrekturbuchungen, sind nicht Teil dieser
Spezifikation. Auch ein Bestandsabgleich ist nicht Teil dieser Spezifikation.




# Datenformate

Warenzugang, Kommiauftrag und Rückmeldung lassen sich sowohl als [JSON][JSON], als auch als XML darstellen.
Oben wurde bereits die (bevorzugte) JSON Darstellung gezeigt. Werdend ie Nachrichten in XML dargestellt,
sähen sie in etwa folgendermaßen aus.

[JSON]: http://www.json.org/

## Warenzugang

### Beispiel 
    
    <warenzugang>
      <datensatz>
	<guid>3104247-7</guid>
	<menge>7</menge>
	<artnr>14695</artnr>
	<batchnr>3104247</batchnr>
      </datensatz>
    </warenzugang>

## Kommiauftrag

### Beispiel

    <kommiauftrag>
      <datensatz>
	<kommiauftragsnr>2103839</kommiauftragsnr>
	<anliefertermin>2009-11-25</anliefertermin>
	<prioritaet>7</prioritaet>
	<info_kunde>Besuch H. Gerlach</info_kunde>
	<auftragsnr>1025575</auftragsnr>
	<kundenname>Ute Zweihaus 400424990</kundenname>
	<kundennr>21548</kundennr>
	<name1>Uwe Zweihaus</name1>
	<name2>400424990</name2>
	<name3/>
	<strasse>Bahnhofstr. 2</strasse>
	<land>DE</land>
	<plz>42499</plz>
	<ort>Hücksenwagen</ort>
	<positionen>
	  <daten1>
	    <menge>12</menge>
	    <artnr>14640/XL</artnr>
	    <posnr>1</posnr>
	  </daten1>
	  <daten2>
	    <menge>4</menge>
	    <artnr>14640/03</artnr>
	    <posnr>2</posnr>
	  </daten2>
	  <daten3>
	    <menge>2</menge>
	    <artnr>10105</artnr>
	    <posnr>3</posnr>
	  </daten3>
	</positionen>
	<versandeinweisungen>
	  <daten1>
	    <guid>2103839-XalE</guid>
	    <bezeichner>avisierung48h</bezeichner>
	    <anweisung>48h vor Anlieferung unter 0900-LOGISTIK
	      avisieren</anweisung>
	  </daten1>
	  <daten2>
	    <guid>2103839-GuTi</guid>
	    <bezeichner>abpackern140</bezeichner>
	    <anweisung>Paletten höchstens auf 140 cm
	      Packen</anweisung>
	  </daten2>
	</versandeinweisungen>
      </datensatz>
    </kommiauftrag>

## Rückmeldung

### Beispiel

    <rueckmeldung>
      <datensatz>
	<kommiauftragsnr>2103839</kommiauftragsnr>
	<positionen>
	  <daten1>
	    <menge>4</menge>
	    <artnr>14640/XL</artnr>
	    <posnr>1</posnr>
	    <nve>23455326543222553</nve>
	  </daten1>
	  <daten2>
	    <menge>8</menge>
	    <artnr>14640/XL</artnr>
	    <posnr>1</posnr>
	    <nve>43255634634653546</nve>
	  </daten2>
	  <daten3>
	    <menge>4</menge>
	    <artnr>14640/03</artnr>
	    <posnr>2</posnr>
	    <nve>43255634634653546</nve>
	  </daten3>
	  <daten4>
	    <menge>2</menge>
	    <artnr>10105</artnr>
	    <posnr>3</posnr>
	    <nve>23455326543222553</nve>
	  </daten4>
	</positionen>
	<nves>
	  <23455326543222553>
	    <gewicht>28256</gewicht>
	    <art>paket</art>
	  </23455326543222553>
	  <43255634634653546>
	    <gewicht>28256</gewicht>
	    <art>paket</art>
	  </43255634634653546>
	</nves>
      </datensatz>
    </rueckmeldung>

## Priorität 

### Beispiel

    <lieferschein>
      <datensatz>
	<kommiauftragsnr>2103839</kommiauftragsnr>
	<prioritaet>3</prioritaet>
      </datensatz>
    </lieferschein>


## Stornierung

### Beispiel

    <stornierung>
      <datensatz>
	<kommiauftragsnr>2103839</kommiauftragsnr>
	<verantwortlicher>Hans Mustermann</verantwortlicher>
	<text>Kunde hatte sich vertan</text>
      </datensatz>
    </stornierung>

## Stornierungsbestaetigung

### Beispiel

    <stornierungsbestaetigung>
      <datensatz>
	<kommiauftragsnr>2103839</kommiauftragsnr>
	<status>storniert</status>
      </datensatz>
    </stornierungsbestaetigung>
