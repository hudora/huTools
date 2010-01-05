# Very Simple Status Protocol

Das 'Very Simple Status Protocol' ist ein Weg Statusmeldungen zu Aufträgen von HUDORA zu erhalten. Es wird in der Regel in Verbindung mit dem [VerySimpleOrderProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorderprotocol.html) für Dreiecksgeschäfte eingesetzt.

Das *Very Simple Status Protocol* wurde entwickelt, um in möglichst vielen Umgebungan abbildbar zu sein. Das bevorzugte Format ist jedoch XML.

Das Protokoll besteht aus einer Reihe von `<event>` Elemententen, die Sendugsereignisse kodieren.

## Pflichtfelder

* __guid__ - Eindeutiger ID des Vorgangs, darf niemals doppelt verwendet werden
* __order/guid__ - Eindeutiger ID der zugehörigen Bestellung des [VerySimpleOrderProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorderprotocol.markdown)
* __timestamp__ - Zeitstempel des Ereignisses  im [RfC 3339](http://www.ietf.org/rfc/rfc3339) format
* __type__ - Art des Ereignisses. "processing", "delivered" oder "error". Bei "delivered" Ereignissen kann der Vorgang als kaufmännisch abgeschlossen angesehen werden. Bei "error" Ereignissen ist manuelle Intervention nötig.
* __detail__ - Natursprachliche Ereignisbeschreibung (ein Wort). Ist mit einem dreistelligen Attribut namens code versehen, das das Ereignis detailliert beschreibt. Zum Code siehe unten.
* __description__ - Satz, der das Ereignis natursprachlich bestimmt. 

## Optionale Felder 

* __order/kundenauftragsnr__ - wurde über das [VerySimpleOrderProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorderprotocol.markdown) eine Kundenauftragsnummer übergeben, wird dieses Feld befüllt.
* __reference__ - HUDORA-interne Referenznummer - für Rückfragen
* __further information__ - Die URL einer Resouche mit mehr Informationen zu diesem und möglicherweise anderen, vrwandten Events. ie Resouchen können XHTML oder PDF sein. 

## Codes 

Bestimmten ereignissen werden Codes zugeordnet. Mit der Übergabe eines Codes über 200 kann die Ware als auf dem Weg gelten. Ein Code größer gleich 400 bedeutet eine erfolgreiche Zustellung.

* *100* - Auftrag empfangen
* *200* - Lieferschein erzeugt
* *201* - An Frachtführer übergeben
* *300* - Anlieferversuch
* *400* - an Empfänger übergeben
* *401* - Ablieferbeleg online
* *500* - Sendung retouniert 

## Beispiele

    <events>
        <event> 
            <guid>65c11532-fda5-11dd-9ebb-131726d62c43</guid>
            <order><guid>2008-08-21T15:16:17-id1222</guid><kundenauftragsnr>XQ03244231</kundenauftragsnr></order>
            <timestamp>2008-08-22T15:16:17.123324</timestamp>
            <type>processing</type>
            <detail code="200">Verschickt</detail>
            <reference>SL13456</reference>
            <description>Die Ware wurde bei HUDORA gepackt und zum Versand bereitgestellt.</description>
            <further_information>http://hulog.hudora.biz/e42bb8c4d2/</further_information>
        </event>
        <event> 
            <guid>65c11532-fda5-11dd-9ebb-131726d62c43</guid>
            <order><guid>2008-08-21T15:16:17-id1222</guid><kundenauftragsnr>XQ03244231</kundenauftragsnr></order>
            <timestamp>2008-08-22T16:16:17</timestamp>
            <type>processing</type>
            <detail code="201">Verladen</detail>
            <reference>DPD:0123124354322435</reference>
            <description>Die Ware wurde DPD mit der Trackingnummer 0123124354322435 übergeben.</description>
            <further_information>http://tracking.dpd.net/1235/</further_information>
        </event>
        <event> 
            <guid>65c11532-fda5-11dd-9ebb-131726d62c43</guid>
            <order><guid>2008-08-21T15:16:17-id1222</guid><kundenauftragsnr>XQ03244231</kundenauftragsnr></order>
            <timestamp>2008-08-23T10:16</timestamp>
            <type>processing</type>
            <detail code="300">Anlieferversuch</detail>
            <reference>DPD:0123124354322435</reference>
            <further_information>http://hulog.hudora.biz/e42bb8c4d2/</further_information>
        </event>
        <event> 
            <guid>65c11532-fda5-11dd-9ebb-131726d62c43</guid>
            <order><guid>2008-08-21T15:16:17-id1222</guid><kundenauftragsnr>XQ03244231</kundenauftragsnr></order>
            <type>delivered</type>
            <detail code="400">Ablieferung</detail>
            <reference>DPD:0123124354322435</reference>
            <description>Die Ware wurde übergeben und vonn "MUELLER" quittiert.</description>
        </event>
        <event> 
            <guid>65c11532-fda5-11dd-9ebb-131726d62c43</guid>
            <order><guid>2008-08-21T15:16:17-id1222</guid><kundenauftragsnr>XQ03244231</kundenauftragsnr></order>
            <timestamp>2008-08-23T22:00:12</timestamp>
            <type>delivered</type>
            <detail code="401">Ablieferbeleg</detail>
            <reference>DPD:0123124354322435</reference>
            <description>Die Ware wurde übergeben und vonn "MUELLER" quittiert.</description>
            <further_information>http://hulog.hudora.biz/e42bb8c4d2/POD.pdf</further_information>
        </event>
    </events>

## Siehe auch

* [VerySimpleOrderProtocol](http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorderprotocol.markdown)
* EDIFACT  [ORDRSP](http://www.edifactory.de/msginfo.php?s=D08A&m=ORDRSP)  [DESADV](http://www.edifactory.de/msginfo.php?s=D08A&m=DESADV)  [IFTSTA](http://www.edifactory.de/msginfo.php?s=D08A&m=IFTSTA) 

