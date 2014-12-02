# Implementierungsleitfaden Datenaustausch mit HUDORA

HUDORA ist sehr interessiert an elektronischen Geschäftsprozessen. Wir bieten unseren Partnern dazu zwei unterscheidliche Plattformen mit untershceidlichen Möglichkeiten.


## HUDORA EDIhub

EDIhub ist die Plattform zum Austausch elektronischer Geschäftsvorfälle bei HUDORA. EDIhub unterstützt Legacy-EDIFACT/EANCOM Nachrichten, bevorzugt aber den NAchrichtenaustausch über moderne Formate und Protokolle von PDF über E-Mail bis zu XML über HTTPS. Darüber hinaus beitet EDIhub eine Plattform zum Einsehen von Produktstammdaten udn Werbedaten, wie zB Bildern. In EDIhub können Rechungen, Lieferscheine udn Auftragsbestätigungen eingesehen und herunter geladen werden.


## HUDORA Express

HUDORA Express ist unsere neue Platform zur effizienten Abwicklung von E-Commerce. HUDORA Express wird permanent weiterentwickelt und bietet zahlreiche innovative und experimentelle Features zur Unterstützung innovativer, moderner Geschäuftsmodelle. Die features von HUDORA Express sind ein Superset von EDIhub.


# Auftragsdaten

Aufträge bzw. Bestellungen können im *[Very Simple Order Protocol][1]* an HUDORA geschickt werden. Der Transportweg dazu ist das *[Frugal Message Trasfer Protocol (FMTP)][2]*.

Zur Datenübertragung bekommen Sie von HUDORA einen Benutzernamen (zB `u10001o4bd1a3`), ein Passwort (`DZE3UZVLO4FMOQ`) und einen Endpunkt (zB `https://edihub.hudora.de/SC10001/orders/`) mitgeteilt.

Wie in der Dokumentation zum [Very Simple Order Protocol (FMTP)][1] beschrieben, können auch kundeneigene Lieferscheine übwrtragen werden. Diese Möglichkeit wird im folgenen nicht näher erörtert - es sei hierzu auf die [FMTP][1] Dokumentation verwiesen.


## Nachrichtenformat

Zunächst muss eine [Very Simple Order Protocol][1] Nachricht erstellt werden. Diese wird üblicherweise als UTF-8 codiertes XML von ihrem Warenwirtschaftssystem oder Webshop erstellt. Sie können diese Nachricht aber auch für Testzwecke einfach mit einem Texteditor erstellen.


## Beispiel-Nachricht `order.xml`

```
    <orders>
      <order>
        <guid>2008-08-21T15:16:17-id1222</guid>
        <name1>HUDORA GmbH</name1>
        <name2>Abt. Cybernetics</name2>
        <strasse>Jägerwald 13</strasse>
        <land>DE</land>
        <plz>42897</plz>
        <ort>Remscheid</ort>
        <tel>+49 2191 60912 0</tel>
        <orderline>
           <guid>2008-08-21T15:16:17-id1222-pos1</guid>
           <menge>1</menge>
           <ean>4005998651698</ean>
           <infotext_kunde>Gartentrampolin ArtNr 65123</infotext_kunde>
        </orderline>
        <kundenauftragsnr>XQ03244231</kundenauftragsnr>
        <infotext_kunde>Lieferung im Auftrag der "Kawuschel Sportausrüstung AG"</infotext_kunde>
      </order>
    </orders>
```


## Nachrichtentransport

Die Nachricht kann nun mittels des  *[Frugal Message Trasfer Protocol (FMTP)][2]* an HUDORA übertragen werden. Dies wird übelciherweise vollautomatisch durch ihr Warenwirtschaftssystem oder ihren Webshop erledigt.

Es kann für Testzwecke aber auch von Hand erfolgen, in dem  die Daten mit mannuell (zB mit [restclient-tool][3] oder [cURL][4])hochgeladen werden.


## Beispiel-Übertragung

Als Beispiel wird das Kommandozeilen-Werkzeug [cURL][4], dass für Mac, Unix und Microsoft Windows kostenfrei erhältlich ist, verwendet.


    >>> curl -i -u u10001o4bd1a3:DZE3UZVLO4FMOQ -X POST -H 'Content-Type: application/xml' --data-binary=@order.xml
    <<< 201 Created

Die Übertragung muss so lange erneut versucht werden, bis vom Server der Code `201`, `409` oder `410` zurück gegeben wird. Vorher ist die Bestellung nicht erfolgreich transportiert worden.

[`fmtp-client/push.py`][5] ist die Referenz-Implementierung eines FTMP-Push-Clients in Python


## Alternativen

Falls Sie keine der oben beschriebenen automatisierten Schnittstelle implementieren können, können wir ihnen folgende Möglichkeiten anbieten, Daten halbautomatisch zu übrtragen:

* Upload der XML-Dateien von Hand in einem Web-Formular.
* Eingabe der Aufträge von Hand in ein Web-Formular.
* Upload von CSV-Dateien in einem Web-Formular.
* Upload von Exel (XLS und XLSX) Dateien in einem Web-Formular.

Bitte beachten Sie, dass für diese Transportwege ereheblicher Implementierungs- und Betriebsmehraufwand auf beiden Seiten entstehen. Damit sind diese Transportwege auch kostspieliger.



[1]: http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorder.markdown
[2]: http://github.com/hudora/huTools/blob/master/doc/standards/fmtp.markdown
[3]: https://code.google.com/a/eclipselabs.org/p/restclient-tool/
[4]: http://curl.haxx.se
[5]: https://github.com/hudora/FMTP/blob/master/fmtp-client/push.py
