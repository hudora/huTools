FMTP - einfacher, sicherer, robuster, automatisierter Datenaustausch
====================================================================

Wie kriegt man eine elektronische Bestellung von Firma A zu Firma B? [SOAP][2]? [DE-Mail][3]? [E-Post][4]? [AS/2][5]? Mit nichten! In der Praxis werden Daten ganz überwiegend per [FTP][6] transportiert. Ein 40 Jahre altes Protokoll, das Probleme mit so ziemlich allen Netztechniken der letzten 15 Jahre hat: Firewalls: problematisch. NAT: nur mit Hacks. Verschlüsselung: [verschiedene, inkompatible Ansätze][7]. Transaktionen: Nur mit Upload-Rename Akrobatik.

Aber: Für fast jedes Betriebssystem gibt es FTP-Server und ein FTP-Client ist eigentlich immer schon mitgeliefert. Jeder [MCP][8] kann FTP bedienen und denken, er versteht es. Es spricht also viel für FTP.

In der Praxis spricht allerdings auch viel gegen FTP. Einen robusten FTP Client oder Server zu implementieren ist eine Riesenarbeit. Vorhandene Software lässt sich nicht zuletzt wegen der FTP-eigenen Netzwerksanforderungen schlecht in Applikationsserver integrieren. Und wir haben schon sehr oft unsere Partner angerufen, sie sollten bitte mal ihren [WS_FTP Server][9] neu starten.

Lange wurde in Messaging Services, wie dem [Amazon Simple Queue Service (Amazon SQS)][11], die Lösung zu sehen. Aber letztendlich fehlt es an Möglichkeiten in die Nachrichtenwartenschlangen hineinzuschauen, es gibt keine Standard-Tools um mit dem System zu interagieren und dann bleiben Probleme, wie dass Nachrichten nach 4 Tagen (ein langes Wochenende) nicht-Abholen verschwinden. Auch die beschränkte Nachrichtengrösse in den meissten Messaging-Systemen erfordert Klimmzüge.

Also selber definieren. Anforderungen sind Sicherheit und Vertraulichkeit, garantierte Nachrichtenlieferung, Verhinderung von Dubletten, Binärfähigkeit (Umlaute und Grafiken können übertragen werden) und Auditierbarkeit.

Ergebnis ist das Frugal Message Trasfer Protocol (FMTP), dass bei HUDORA seit 2009 im Produktivbetrieb ist und bereit viele Millionen NAchrichten zwischen uns und unseren Partnern üebrtragen hat.


Frugal Message Trasfer Protocol (FMTP)
--------------------------------------

FMTP dient dem zuverlässigen, Austausch von Nachrichten per HTTP nach [REST][12] Prinzipien. Nachrichten können im Push (sendend), oder Pull (empfangend) Modus transportiert werden. Für den Tansfer einer Nachrichtenart von einem Sender an einem Empfänger wird ein Endpunkt definiert, der mit einer Queue in einer [MOM][13] vergleichbar ist. In den folgenden Beispielen wird der Endpunkt `https://example.com/q` verwendet. Nachrichten müssen einen eindeutigen Bezeichner haben, der pro Endpunkt nur einmal vorkommen darf. Wenn das sendene System keine GUIDs erzeugen kann, können auch andere eindeutige Bezeichner, wie Rechungsnummer etc verwendet werden. GUIDs sollten mit dem Regular Expression `/[a-zA-Z0-9_-]+/` matchen. Der Eindeutige Bezeichner verhindert die Übertragungen von Dubletten.


Daten Senden (Push)
-------------------

Gesetzt eine Nachricht hat den GUID `guid`, den Inhalt `'content'` und den content-type `application/xml`, dann kann die Nachricht folgendermassen in den Endpunkt `https://example.com/q` eingespeist werden:

    >>> POST https://example.com/q/guid HTTP/1.1
    >>> Host: example.com
    >>> Content-Type: application/xml
    >>>
    >>> 'content'

In der Regel antwortet der Server mit folgenden Nachrichten:

* **201 Created** Die Nachricht wurde auf dem Server gespeichert
* **409 Conflict** Es existiert bereits eine Nachricht mit dem gleichen GUID
* **410 Gone** Es existierte bereits eine Nachricht mit dem gleichen GUID, die aber bereits verarbeitet/gelöscht wurde.


Daten Empfangen (Pull)
----------------------

Das Protokoll unterstützt kein Locking. Das bedeutet, dass entweder nur ein Client lesend zugreifen darf, oder das Locking auf der Client Seite implementiert werden muss. Der Empfang gliedert sich in in drei Schritte, die in einer Schleife ausgeführt werden.

* Abruf einer Liste der bereitstehenden Nachrichten
* Abruf einer Nachricht
* Löschen der abgerufenen Nachricht

Die Liste der bereitstehenden Nachrichten kann in verschiedenen Formaten empfangen werden. Für FMTP müssen die Formate Text, JSON und XML unterstützt werden. Die folgenden Beispiele nutzen das Text Format. Durch GET Abruf des Endpunktes bekommt der Empfänger eine Liste mit URLs von Nachrichten. Die URLs sind durch '\n' (ASCII 10) voneinander getrennt.

    >>> GET https://example.com/q
    >>> Host: example.com

    <<< 200 OK
    <<< Content-Type: text/plain
    <<<
    <<< https://example.com/q/guid
    <<< https://example.com/q/otherguid

Aufgrund der Informationen in dieser Liste kann nun eine Nachricht abgerufen werden.

    >>> GET https://example.com/q/guid
    >>> Host: example.com

    <<< 200 OK
    <<< Content-Type: application/json
    <<<
    <<< 'content'

Der Content-Type ist der gleiche, der von dem Sender mitgegeben wurde. Wenn der Empfänger die Nachricht erfolgreich übernommen hat - z.B. indem er Sie in eine Datenbank geschrieben hat, muss er die Nachricht auf dem Server löschen. Das muss mit dem HTTP Befehl DELETE erfolgen.

    >>> DELETE https://example.com/q/guid
    >>> Host: example.com

    <<< 204 No Content

Nun kann erneut durch Aufruf von `https://example.com/q` geprüft werden, ob neue Nachrichten vorliegen.


### Listenformate

Die Liste der bereitstehenden Nachrichten kann in verschiedenen Formaten abgerufen werden. Welches Format der Server zurückliefert kann anhand des `Accept` Headers, der vom Client geschickt wird, gesteuert werden. Zum einen steht das [JSON][14] Format zur Verfügung:

    >>> GET https://example.com/q
    >>> Host: example.com
    >>> Accept: application/json

    <<< 200 OK
    <<< Content-Type: application/json
    <<<
    >>> {
    >>>  'min_retry_interval': 500,
    >>>  'max_retry_interval': 60000,
    >>>  'messages': [
    >>>   {'url': 'https://example.com/q/guid', 'created_at': '2010-10-13T20:30:40.1234'},
    >>>   {'url': 'https://example.com/q/otherguid', 'created_at': '2010-10-13T20:30:50.6789'},
    >>>  ]
    >>> }


Alternativ kann die Nachrichtenliste als [Plain old XML][15] abgerufen werden:

    >>> GET https://example.com/q
    >>> Host: example.com
    >>> Acceppt: application/xml

    <<< 200 OK
    <<< Content-Type: application/xml
    <<<
    >>> <data>
    >>>  <min_retry_interval>500</min_retry_interval>
    >>>  <max_retry_interval>60000</max_retry_interval>
    >>>  <messages>
    >>>   <message>
    >>>    <url>https://example.com/q/guid</url>
    >>>    <created_at>2010-10-13T20:30:40.1234</created_at>
    >>>   </message>
    >>>   <message>
    >>>    <url>https://example.com/q/otherguid</url>
    >>>    <created_at>2010-10-13T20:30:50.6789</created_at>
    >>>   </message>
    >>>  </messages>
    >>> </data>

Per Default wird die Liste als Text (s.o.) zurück geliefert. Das Text-Format unterstützt jedoch cniht alle Features.


### Retry-Interval

Ein Empfänger muss immer wieder die Liste der bereitstehenden Nachrichten abrufen ("Polling"). Die Frage ist, in welchen Intervallen nach neuen Nachrichten gefragt werden soll. Wird zu häufig gefragt, wird die automatisierte Denial-of-Service Detektion den Client zeitweise sperren und alle Anfragen mit `503 Service Unavailable` beantworten.

Deswegen empfiehlt es sich im Client [Exponential Backoff][16] zu implementieren. D.h. wenn keine neue Nachrichten gefunden wurden, sollte die Wartezeitbis zur nächsten Anfrage verdoppelt werden. Der Server liefert mit `min_retry_interval` und `max_retry_interval` Vorschläge, wie viele Millisekunden der Client minimal und maximal bis zur nächsten Anfrage warten soll.


Analyse
-------

[HTTP ist als Protokoll "des Web" ein weit verbreitetets Protokoll][17] und kann problemlos in allen relevanten Programmiersprachen wie Java, Python, Perl, Ruby, RPG/4 und bash genutzt werden. HTTP stellt die Binärfähigkeit sicher und wird hervorragend von Firewalls und dergleichen unterstützt. Die Nutzung von HTTPS/[Transport Layer Security 1.1][18] stellt die Sicherheit und Vertraulichkeit der Datenübertragung sicher. Der Grad der Authentizitätssicherstellung kann durch [Certificate Pinning][19] und TLS Client Certificates weiter gesteigert werden.

Die Nachrichtenlieferung ist garantiert. Bei einem PUSH-Client ist dies der Fall, wenn der Client dsa Hochladen so lange versucht, bis er den Status `201`, `409`, oder `410` erhält.
Bei einem Pull Client, darf der Client erst das `DELETE` Kommando senden, wenn er die Daten verarbeitet hat, um eine Nachrichtenlieferung zu garantieren.

Dubletten werden von dem Protokoll durch eindeutige Bezeichner verhindert.

Die normal von einem HTTP-Server geführten Protokolldateien reichen aus, um Nachrichtenzustellungsversuche, -erfolge und -verarbeitungsbestätigungen zu auditieren.


[2]: http://de.wikipedia.org/wiki/SOAP
[3]: http://de.wikipedia.org/wiki/De-Mail
[4]: http://de.wikipedia.org/wiki/E-Postbrief
[5]: http://de.wikipedia.org/wiki/AS2
[6]: http://en.wikipedia.org/wiki/File_Transfer_Protocol
[7]: http://en.wikipedia.org/wiki/FTPS
[8]: http://en.wikipedia.org/wiki/Microsoft_Certified_Professional
[9]: http://www.ipswitchft.com/products/WsFtpServer/index.aspx?n=1&k_id=ipshome
[11]: http://aws.amazon.com/sqs/
[12]: http://de.wikipedia.org/wiki/Representational_State_Transfer
[13]: http://de.wikipedia.org/wiki/Message_Oriented_Middleware
[14]: http://www.json.org/
[15]: http://en.wikipedia.org/wiki/Plain_Old_XML
[16]: http://dthain.blogspot.com/2009/02/exponential-backoff-in-distributed.html
[17]: http://de.wikipedia.org/wiki/Hypertext_Transfer_Protocol
[18]: http://de.wikipedia.org/wiki/Transport_Layer_Security
[19]: http://en.wikipedia.org/wiki/Transport_Layer_Security#Certificate_pinning

