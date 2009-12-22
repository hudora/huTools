DRAFT $Date$ $Revision$

=======================================
Kommunikation inventory control <-> WMS
=======================================

Pro Lager gibt es ein WMS. Inventory Control und WMS komunizieren in beide Richtungen asyncron mit
Nachrichten und in Richtung Inventory Control -> WMS -> Inventory contol via REST.

Nachrichtentypen
================

Hier ein Überblick über die Nachrichtentypen, die ausgetauscht werden:

* Warenzugang von Inventory Control an WMS (asyncron)
* Kommiauftrag von Inventory Control an WMS (asyncron)
* Priorität update von Inventory Control an WMS (asyncron)
* Stornierung von Inventory Control an WMS (syncron)
* Rücklmeldung eines Auftrags von WMS an Inventory Control (asyncron)
* Lieferscheine von Inventory Control an WMS (asyncron)

Nachrichten
===========

TBD

Warenzugang
-----------

Diese Nachricht wird unmittelbar an das WMS gesendet, wenn die Ware das Lagerphysisch erreicht haben
sollte. Pro Artikel wird eine Nachricht gesendet. GUIDs sollten auf jeden Fall doppelte Zubuchungen
vermeiden.

Pflichtfelder:

:guid:
    Eindeutiger Bezeichner der Nachricht. Kann doppelt vorkommen, dsa Zielsiestem darf dann nur
    genau EINE der Nachrichten verarbeiten.

:menge: 
    Integer, repräsentiert die zuzubuchende Menge. Kann vom WMS auf mehrere Ladungsträger
    verteilt werden.

:artnr: String, Eindeutiger ID der zu lagernden Ware.

:batchnr: String, der z.B. bei der Identifizierung der Auslagerung genutzt werden kann.

Zusatzfelder:

:referenzen:
    Dict, dass Referenzen enthält, die zur Verarbeitung des Warenzugangs nicht zwingend
    notwendig sind.

:mui:
        Barcode, der bereits auf der Waren angebracht ist. Es wird davon ausgegangen, dass die gesammte
        mit dieser Nachricht zugebuchte Menge auf einem einzigen Ladungsträger ist.


Beispiel::

    {
       "guid":"3104247-7"
       "menge":7,
       "artnr":"14695",
       "batchnr": "3104247",
    }


Kommiauftrag
------------

Pflichtfelder:

:kommiauftragsnr: e
    Eindeutiger ID des Kommisionierauftrags. Kann doppelt vorkommen, dsa Zielsiestem darf dann nur
    genau EINE der Nachrichten verarbeiten.

:anliefertermin: Termin, an dem die Ware spätestens beim Kunden sein muß

Zusatzfelder:

:anliefertermin_ab: Termin ab dem die Ware frühstens beim Kunden sein darf

:versandtermin:  Termin an dem die Ware spätestens das Lager verlassen soll

:versandtermin_ab: Termin ab dem die Ware das Lager frühstens verlassen darf

:fixtermin: Wenn True: Zuspätlieferung kann erhebliche Kosten nach sich ziehen.

:gewicht: Netto Gewicht der Ware in Gramm

:volumen: Netto Volumen der Ware in Liter

:info_kunde: Freitext der für den Empfänger relevanz hat, z.B. Kundenauftragsnummer

:auftragsnr: Freitext zur besseren Referenzierung - Nicht eindeutig!

:kundenname: Freitext zur besseren Referenzierung

:kundennr: Freitext zur besseren Referenzierung

Weitere Zusatzfelder können alle Felder des Address Protokolls sein. Diese dienen lediglich der Information.
Die Verbindliche Lieferadresse erscheint auf dem Lieferschein.

Pro Position:

Pflichtfelder:

:menge:
       Integer, repräsentiert die zuzubuchende Menge. Kann vom WMS auf mehrere Ladungsträger
       verteilt werden.

:artnr: String, Eindeutiger ID der zu komissionnierenden Ware.

:auftragsposition: Nummer der Auftragsposition

Versandanweisungen:

Beispiel::

    {
        "kommiauftragsnr":2103839,
        "anliefertermin":"2009-11-25",
        "info_kunde":"Herr Gerlach",
        "auftragsnr":1025575,
        "kundenname":"Ute Zweinnhaus 400424990",
        "kundennr":"21548",
        "name1":"Uwe Heinhaus",
        "name2":"400424990",
        "name3":"",
        "strasse":"Bahnhofstr. 2"
        "land":"DE",
        "plz":"42499",
        "ort":"Hückesckeswagen",
    }



Rückmeldung
-----------

Diese Nachricht wird vom WMS an Central Services gesendet, sobald ein Komissionierauftrag zuende
bearbeitet wurde. Sie ist Voraussetzung für den Lieferscheindruck. Ein Kommiauftrag kann nur genau
einmal zurukgemeldet werden.

Warteschlangen:
 * `erp.cs-wms.rueckmeldung#normal` für Rückmeldungen ohne Mengenänderungen
 * `erp.cs-wms.rueckmeldung#spezial` für Rückmeldungen mit Mengenänderungen, Stornos etc.

:kommiauftragsnr: Unique ID des Kommiauftrags, der bei der Kommiauftrag Nachricht übertragen wurde.

:positionen:
	Liste der zurückzumeldenen Positionen. Muss IMMER alle Positionen beinhalten, die 
	im  Kommiauftrag mitgesendet wurden. Jede Position wird als Dictionary abgebildet.
	Pflichtfelder in jedem Dictionary sind zur Zeit `posnr`, `menge` und `artnr`.

