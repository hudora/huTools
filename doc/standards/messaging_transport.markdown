# Nachrichtenaustausch zwischen Unternehmen

Wir gehen davon aus, dass die automatisierte Kommunikation zwischen Unternehmen, folgede Massgaben zu
erfüllen hat:

* **Nachrichten basierte Kommunikation / Batchverarbeitung** - es ist keine Unmittelbare Antowrt auf die
  Nachrichten erforderlich. Die Beteiligten Systeme sind nicht echtzeitfähig. Stattessen werden Aufträge
  gesendet und deren Erledigung oder Status in der Regel erst Stunden, oder Tage spuater zurück gemeldet.
* **Zuverlässig** - Das System darf ekine Nachrichten verlieren. Nachrichten müssen verarbeitet werden, oder
  es muss eine Fehlermeldung erfolgen. Nachrichten dürfen nie "verloren gehen". Nachrichten dürfen nie
  doppelt verarbeitet werden.
* **Sicher** - Nachrichten dürfen nicht durch Unbefugte erzeugt oder verarbeitet werden kuonnen.
* **Performat** - Nachrichten sollten in unter 15 Minuten das System durchlaufen haben
* **Stabil** - Das gesammte Nachrichtenverarbeitungssystem sollte eine Verfügbarkeit von über 99 %
  zu den Betriebsstundnen haben.
* **Unicode clean** - Das Nachrichtenverarbeitungssystem sollte Nicht-ASCII zeichen, wie das Wort
  "Iñtërnâtiônàlizætiøn" unbeschdigt transportieren können.
* **Wartungsfreundlich** - Das System sollte leicht zu verstehen und zu betreiben sein.
* **Preiswert** - Implementierung und Betrieb sollten möglichst wenig Kosten verursachen.


## Implementierung mit SQS

Diese Anforderuungen werden zur Zeit mit Abstand am besten durch den
[Amazon Simple Queue Service (Amazon SQS)][1] erfüllt. Mit ca. 0.00001 US$ Kosten pro Nachricht
ist der dienst unschlagbar günstung und gleichzeitig sehr zuverlässig. Amazon SQS ist einfach zu
programmieren und ein Partner muss in der Reglen nur die Funktionen SendMessage, ReceiveMessage und
DeleteMessage implementieren. Zur Not können diese Funktionen auch mit einfachen Kommandozeilen
basierten Programmen, wie [cURL][2] aufgerufen werden. Amazon bietet Umfangreiche [Dokumentation][3]
und [Beispielprogramme][4]

[1]: http://aws.amazon.com/sqs/
[2]: http://curl.haxx.se/
[3]: http://developer.amazonwebservices.com/connect/entry.jspa?externalID=2317&categoryID=31 
[4]: http://developer.amazonwebservices.com/connect/kbcategory.jspa?categoryID=8