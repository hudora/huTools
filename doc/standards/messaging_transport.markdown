# Nachrichtenaustausch zwischen Unternehmen

Wir gehen davon aus, dass die automatisierte Kommunikation zwischen Unternehmen folgende Massgaben zu
erfüllen hat:

* **Nachrichten basierte Kommunikation / Batchverarbeitung** - es ist keine unmittelbare Antwort auf die
  Nachrichten erforderlich. Die beteiligten Systeme sind nicht echtzeitfähig. Stattdessen werden Aufträge
  gesendet und deren Erledigung oder Status in der Regel erst Stunden, oder Tage später zurück gemeldet.
* **Zuverlässig** - Das System darf keine Nachrichten verlieren. Nachrichten müssen verarbeitet werden, oder
  es muss eine Fehlermeldung erfolgen. Nachrichten dürfen nie "verloren gehen". Nachrichten dürfen nie
  doppelt verarbeitet werden.
* **Sicher** - Nachrichten dürfen nicht durch Unbefugte erzeugt oder verarbeitet werden können.
* **Performant** - Nachrichten sollten in unter 15 Minuten das System durchlaufen haben
* **Stabil** - Das gesammte Nachrichtenverarbeitungssystem sollte eine Verfügbarkeit von über 99 %
  zu den Betriebsstundnen haben.
* **Unicode clean** - Das Nachrichtenverarbeitungssystem sollte Nicht-ASCII zeichen, wie das Wort
  "Iñtërnâtiônàlizætiøn" unbeschädigt transportieren können.
* **Wartungsfreundlich** - Das System sollte leicht zu verstehen und zu betreiben sein.
* **Preiswert** - Implementierung und Betrieb sollten möglichst wenig Kosten verursachen.



## Implementierung mit SQS

Diese Anforderuungen werden zur Zeit mit Abstand am besten durch den
[Amazon Simple Queue Service (Amazon SQS)][1] erfüllt. Mit ca. 0.00001 US$ Kosten pro Nachricht
ist der Dienst unschlagbar günstig und gleichzeitig sehr zuverlässig. Amazon SQS ist einfach zu
programmieren und ein Partner muss in der Reglen nur die Funktionen SendMessage, ReceiveMessage und
DeleteMessage implementieren. Zur Not können diese Funktionen auch mit einfachen Kommandozeilen
basierten Programmen, wie [cURL][2] aufgerufen werden. Amazon bietet umfangreiche [Dokumentation][3]
und [Beispielprogramme][4]. Es gibt eine gute [Einführung zur SQS Programmierung bei IBM][5].

[1]: http://aws.amazon.com/sqs/
[2]: http://curl.haxx.se/
[3]: http://developer.amazonwebservices.com/connect/entry.jspa?externalID=2317&categoryID=31 
[4]: http://developer.amazonwebservices.com/connect/kbcategory.jspa?categoryID=8
[5]: http://www.ibm.com/developerworks/library/ar-cloudaws4/

Für die Kommunikation zwischen Unternehmen werden bei Amazon SQS sogenannte "[Shared Queues][6]"
eingesetzt. Queues werden von uns (Hudora) erzeugt und wir fügen den Partner mittels
*[Add Permission][7]* hinzu. Dazu muss der Partner einen bei Amazon AWS einen kostenfreien Account
angelegt haben und uns seinen 12-stelligen AWSAccountId (ohne Bindestriche) übermittelt haben.
Für Jede Nachrichten Art teilen wir dem Partner die [queue URL][8] mit, unter der die entsprechenden
Nachrichten eingestellt oder abgerufen werden können.

[6]: http://docs.amazonwebservices.com/AWSSimpleQueueService/2009-02-01/SQSDeveloperGuide/
[7]: http://docs.amazonwebservices.com/AWSSimpleQueueService/2009-02-01/APIReference/index.html?Query_QueryAddPermission.html
[8]: http://docs.amazonwebservices.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/index.html?ImportantIdentifiers.html

### Beispiel

Für das Beispiel nutzen wir Python Code und die Bibliothek [boto][10], die den Zugriff auf SQS erleichtert.

[10]: http://code.google.com/p/boto/

Dieses Beispiel liest Nachrichten und verarbeitet sie mit der WMS Funktion `process_body()` verarbeiten.

    >>> import boto.sqs.connection, boto.sqs.queue
    >>> conn = boto.sqs.connection.SQSConnection()
    >>> q = boto.sqs.queue.Queue(connection=conn, url='http://queue.amazonaws.com/123456789012/hd.warenzugang.100')
    >>> rs = q.get_messages(visibility_timeout=60)
    >>> if rs:
    ...    for msg in rs:
    ...        body = m.get_body()
    ...        # Nachricht im WMS verarbeiten (sollte nciht länger als 60 Sekunden dauern)
    ...        process_body(body)
    ...        # Verarbeitung erfolgreich, Nachricht entfernen
    ...        q.delete_message(m)
    

## Implementierung mit FTP

Sollte ein Partner nicht in der Lage sein, Nachrichten mit SQS zu senden und zu empfangen, kann als
Notlösung auch unser FTP-Server verwendet werden. FTP ist deutlich weniger zuverlässig und hat deutlich
höheren Wartungs- und Betriebsaufwand.

Insbesondere ist es nicht ohne weiteres möglich, halb geschriebene Nachrichten von komplettne Nachrichten zu
unterscheiden. Von der Nutzung von FTP wird daher dringend zugunsten der Zuverlässigkeit und Wartbarkeit
abgeraten. SQS ist die deutlich professionellere und kostengünstigere Lösung.

Sollte der Partner doch auf der Nutzung von FTP bestehen, bekommt er die Zugangsdaten für den Hudora-FTP
Server übermittelt. Für jede Nachrichtenart muss der Partner ein eigenes Verzeichnis nutzen. Nachrichten
an Hudora werden vom Partner in das entsprechende Verzeichnis hochgeladen und durch Hudora gelöscht.

Nachrichten an den Partner werden in das Entsprechende Verzeichnis von Hudora eingestellt un müssen durch
den Partner nach Verarbeitung gelöscht werden.

Da der FTP-Server von Hudora nur eine Verfügbarkeit von 98 % hat, muss der Partner auf jeden Fall einen
automatischen Retry - möglichst mit [exponential backoff][11] - implementieren. Dies gilt sowohl für
die Sende-, als auch für die Empfangsrichtung.

[11]: http://en.wikipedia.org/wiki/Exponential_backoff