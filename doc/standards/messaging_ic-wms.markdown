# Kommunikation zwischen Inventory Control und einem WMS

Im folgenden wird das Kommunikationsprotokoll zwischen einer Warenwirtschaft (*Inventory Control*, IC, ERP)
und einem Lagerverwaltungssystem (LVS, WMS) definiert. Es wird davon ausgegangen, dass Inventory Control
das bestandsführende System ist.

Pro Lager gibt es ein (logisches) WMS. Lager sind mit einem eindeutigen Bezeichner identifiziert, der aber für
die Kommunikation zwischen Inventory Control und einem WMS unbedeutend ist. Inventory Control und WMS
kommunizieren in beide Richtungen per HTTP/REST per [FMTP](http://mdornseif.github.com/2010/11/07/zuverlaessiger-dateitransfer.html).

# Transport

Der Transport erfolgt per [FMTP](http://mdornseif.github.com/2010/11/07/zuverlaessiger-dateitransfer.html).
Eine [Referenzimplementation](https://github.com/cklein/FMTP/blob/master/pull_client/recv_fmtp.py) ist öffentlich verfügbar.

Zur Authentifizierung wird [HTTP Basic Auth](http://tools.ietf.org/html/rfc2617) verwendet.
Die Zugangsdaten können Sie bei HUDORA erfragen.

# Nachrichten

Hier ein Überblick über die Nachrichtentypen, die ausgetauscht werden:

* **Warenzugang** von Inventory Control an WMS
* **Kommiauftrag** von Inventory Control an WMS
* **Rückmeldung** eines Auftrags von WMS an Inventory Control
* **Lieferscheine** von Inventory Control an WMS
* **Korrekturbuchung** vom WMS an Inventory Control
* **Bestandsabgleich** von WMS und Inventory Control

Im folgenden eine detaillierte Beschreibung der einzelnen Nachrichtentypen.

## Warenzugang

Diese Nachricht wird unmittelbar an das WMS gesendet, sobald die Ware das Lager physisch erreicht hat.
Pro Artikel wird eine Nachricht gesendet. GUIDs sollten auf jeden Fall doppelte Zubuchungen
vermeiden. Warenzugänge werden durch das WMS nicht bestätigt. Abweichungen Soll/Istmenge müssen über
Korrekturbuchungen gelöst werden.

### Pflichtfelder

* **guid** - Eindeutiger Bezeichner der Nachricht. Kann doppelt vorkommen, das WMS darf dann nur
  genau *eine* der Nachrichten verarbeiten.
* **menge** - Integer, repräsentiert die zuzubuchende Menge. Kann vom WMS auf mehrere Ladungsträger
  verteilt werden.
* **artnr** - String, eindeutiger ID der zu lagernden Ware.
* **charge** - String, der z.B. bei der Identifizierung der Auslagerung genutzt werden kann.

### Transport
Die Übertragung erfolgt nach dem FMTP-Protokoll.

#### Liste der offenen Warenzugänge abrufen
Auf die HTTP GET-Anfrage an den URL */fmtp/lg200_zugang/* antwortet der Server mit Statuscode 200 und liefert ein XML-Dokument
mit den offenen Warenzugängen.
Das Format wird unten beschrieben.

Im Container-Element ``messages`` gibt es für jeden offenen Warenzugang ein ``message``-Element.
Das Element ``url`` gibt den URL des Warenzugangs an, unter dem dieser im nächsten Schritt abrufbar ist.

#### Abruf eines einzelnen Warenzugangs
Ein Warenzugang wird per HTTP GET abgerufen.
Der Server antwortet mit Statuscode 200 und liefert den Warenzugang als XML-Dokument.
Das Format wird unten beschrieben.

#### Empfangsbestätigung eines Warenzugangs
Nach dem Lesen und Verbuchen des Warenzugangs muss dieser als empfangen markiert werden.
Erst dann gilt der Warenzugang als übertragen.
Dazu wird ein HTTP DELETE Request an den gleichen URL wie beim Abruf geschickt.
Der Webserver antwortet mit Statuscode 204.

### Beispiel

    curl -u username:password -X GET -H 'Accept: application/xml' http://example.com/fmtp/lg200_zugang/
    <data>
     <max_retry_interval>60000</max_retry_interval>
     <messages>
      <message>
       <created_at>2010-12-03 12:17:43.59736</created_at>
       <url>http://hulogi.appspot.com/fmtp/lg200_zugang/3104247-7/</url>
      </message>
     </messages>
     <min_retry_interval>500</min_retry_interval>
    </data>

    curl -u username:password -X GET http://example.com/fmtp/lg200_zugang/3104247-7/
    <warenzugang>
      <guid>3104247-7</guid>
      <menge>7</menge>
      <artnr>14695</artnr>
      <batchnr>3104247</batchnr>
      <charge>LQN4711</charge>
    </warenzugang>

    curl -u username:password -X DELETE http://example.com/fmtp/lg200_zugang/3104247-7/

Eine Beispielnachricht in XML findet sich unter
[http://github.com/hudora/huTools/blob/master/doc/standards/examples/warenzugang.xml][warenzugang.xml].

[warenzugang.xml]: http://github.com/hudora/huTools/blob/master/doc/standards/examples/warenzugang.xml


## Kommiauftrag
Die Nachricht wird - möglicherweise viele Tage - vor dem gewünschten Anliefertermin von Inventory Control
an das WMS gesendet.
Die Nachrichten entsprechen dem [LieferungProtocol](https://github.com/hudora/huTools/blob/master/doc/standards/lieferungprotocol.markdown)
Anbei eine Übersicht.

### Transport
Die Übertragung erfolgt nach dem FMTP-Protokoll.

#### Abruf der Liste der offenen Kommissionieraufträge
Auf die HTTP GET-Anfrage antwortet der Server mit Statuscode 200 und liefert ein XML-Dokument mit den zu bearbeitenden Kommissionieraufträgen.
Das Format wird unten beschrieben.

#### Abruf eines einzelnen Kommissionierauftrags
Ein Kommissionierauftrag wird mit HTTP GET abgerufen.
Der Server antwortet mit Statuscode 200 und liefert den Kommissionierauftrag als XML-Dokument.
Das Format wird unten beschrieben.

#### Empfangsbestätigung eines Kommissionierauftrags
Nach dem Lesen und Speichern des Kommissionierauftrags muss dieser als empfangen markiert werden.
Erst dann gilt der Auftrag als übertragen.
Dazu wird ein HTTP DELETE Request an den gleichen URL geschickt.
Der Webserver antwortet bei erfolgreichem Empfang mit Statuscode 204 und einer leeren Antwort.

### Beispiel
#### Liste der offenen Aufträge

    curl -u username:password -X GET -H 'Accept: application/xml' http://example.com/fmtp/quename/
    <data>
     <max_retry_interval>60000</max_retry_interval>
     <messages>
      <message>
       <created_at>2010-12-03 14:28:15.786318</created_at>
       <url>http://hulogi.appspot.com/fmtp/maeuler/KB3159702/</url>
      </message>
     </messages>
     <min_retry_interval>500</min_retry_interval>
    </data>

Im Container-Element ``messages`` gibt es für jeden offenen Kommissionierauftrag ein ``message``-Element.
Das Element ``url`` gibt den URL des Kommissionierauftrags an, unter dem der Auftrag in nächsten Schritt abrufbar ist.

#### Abruf eines Kommissionierauftrag

    curl -u username:password -X GET http://example.com/fmtp/maeuler/KB3159702/
    <xml>TODO</xml>

#### Empfangsbestätigung eines Kommissionierauftrags
Nach dem Lesen und Speichern des Kommissionierauftrags muss dieser als empfangen markiert werden.
Erst dann gilt der Auftrag als übertragen.
Dazu wird ein HTTP DELETE Request an den gleichen URL wie beim Abruf geschickt.

    curl -u username:password -X DELETE http://example.com/fmtp/maeuler/KB3159702/



## Rückmeldung

Diese Nachricht wird vom WMS an Inventory Control gesendet, *sobald ein Kommiauftrag versendet werden soll*.
Sie ist Voraussetzung für die Lieferscheingenerierung. Ein Kommiauftrag kann nur genau einmal rückgemeldet werden.

### Pflichtfelder

* **guid** - Unique ID (Kommiauftragsnr) des Kommiauftrags, der bei der Kommiauftrag-Nachricht übertragen wurde.
* **positionen** - Liste der zurückzumeldenen Positionen. Muss IMMER alle Positionen beinhalten, die 
  im  Kommiauftrag mitgesendet wurden. Jede Position wird als Dictionary abgebildet. Positionen können
  mehrfach vorkommen. Wenn ein Artikel mit mehreren NVEs transportiert wird, müssen Sie mehrfach vorkommen. 
  Pflichtfelder in jedem Dictionary sind zur Zeit `posnr`, `menge` und `artnr`.
  Zusatzfelder ist `nve` und `referenzen` (siehe Warenzugang), insbesondere `referenzen.charge`.

#### Zusatzfelder pro Rückmeldung

* **nves** - Liste der Versandeinheiten. Enthält pro Versandeiheit ein Dictionary mit Gewicht in Gramm
  und der Art der Versandeinheit. 

### Transport

Die Rückmeldung erfolgt per HTTP POST.
Bei erfolgreicher Übertragung antwortet der Server mit Statuscode 201.
Wird eine Rückmeldenachricht für eine Kommiauftragsnr doppelt geschickt, antwortet der Server mit Statuscode 409.
Bei einer ungültigen Rückmeldenachricht antwortet der Server mit Statuscode 406.

### Beispiel

    curl -u username:password -X POST -H "Content-Type: application/json" http://example.com/fmtp/lg200_rueckmeldung/
    
    {"guid":2103839,
     "positionen": [{"menge": 4,
                     "artnr": "14640/XL",
                     "posnr": 1,
                     "nve": "23455326543222553",
                     "referenzen": {"charge": "LQN4711"}},
                    {"menge": 8,
                     "artnr": "14640/XL",
                     "posnr": 1,
                     "nve": "43255634634653546",
                     "referenzen": {"charge": "LQN4711"}},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr": 2,
                     "nve": "43255634634653546",
                     "referenzen": {"charge": "LQN4711"}},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr": 3,
                     "nve": "23455326543222553",
                     "referenzen": {"charge": "LQN4711"}}],
     "nves": [{"nve": "23455326543222553",
               "gewicht": 28256,
               "art": "paket"},
              {"nve": "43255634634653546",
               "gewicht": 28256,
                "art": "paket"}]}

Eine Beispielnachricht in XML findet sich unter
[http://github.com/hudora/huTools/blob/master/doc/standards/examples/rueckmeldung.xml][rueckmeldung.xml].

[rueckmeldung.xml]: http://github.com/hudora/huTools/blob/master/doc/standards/examples/rueckmeldung.xml

## Lieferschein

Der Lieferschein ist das finale Versanddokument und löst die Abbuchung der Ware aus dem Lager und die
Rechnungsstellung aus. Er wird auf die Rückmeldung hin erzeugt.
Der Lieferschein wird per FMTP als PDF-Dokument an das WMS gesendet.

Lieferscheine werden nach Rückmeldung als PDF zur Verfügung gestellt.
Dabei sind die Dateien nach der *guid* benannt. Für obiges Beispiel z.B. "2103839.pdf".
Die Erzeugung von Lieferscheinen dauert wenige Minuten.


### Implementierung eines Beispiel-Clients

Die [Referenzimplementation](https://github.com/cklein/FMTP/blob/master/pull_client/recv_fmtp.py) des FTMP-Clients
kann als Grundlage verwendet werden.

Der folgende Aufruf speichert alle übertragenen Lieferscheindokumente im Verzeichnis *Lieferscheine*:
    python.exe pull_client/recv_fmtp.py -d Lieferscheine -c username:password -e http://example.com/fmtp/lg200_lieferscheine/


## Stornierung

Wenn ein Auftrag im WMS storniert wurde, muss dies dem Inventory Control gemeldet werden.
Dazu wird eine Rückmeldungsnachricht geschickt, in der die zu stornierenden Positionen mit Menge 0 zurückgemeldet werden.


## Korrekturbuchung
TBD


## Bestandsabgleich
TBD
