# User interface guidelines 

This are guidelines for User interfaces we develop. It mostly concerns HTML GUIs created with
[jQuery][jQuery] 1.4.x.

[jQuery]: http://jquery.com/


## Messages

### jGrowl - minor messages

For non essential information we use [Growl Style][growl] notifications via [jGrowl][jGrowl].
To use it add the following Lines to your `<head>` section:
    
    <link rel="stylesheet" href="http://s.hdimg.net/libs/jgrowl-1.2.4/jquery.jgrowl.css" type="text/css">
    <script type="text/javascript" src="http://s.hdimg.net/libs/jgrowl-1.2.4/jquery.jgrowl.js"></script>

Only send messages via Growl for information where there is no harm if they are ignores. Messages are send
like this:

        $.jGrowl("ungültige Menge");

Do not use Growl for "important" messages which should not be ignored. While the `jGrowl` library has
functionality for "sticky" messages, avoid using that. If your application has any mayor messages to use, use
humanmsg instead.

[growl]: http://growl.info/about.php
[jGrowl]: http://www.stanlemon.net/projects/jgrowl.html


### humanmsg - major messages

For all major messages, users schould not ignore we use [Humanized Messages][humanizedmessages] as
implemented by [humanmsg][humanmsg]. To not use jGrowl together with humanmsg, but only one of them!
To use it add the following Lines to your `<head>` section:

    <link rel="stylesheet" href="http://s.hdimg.net/libs/humanmsg-1.0/humanmsg.css" type="text/css">
    <script type="text/javascript" src="http://s.hdimg.net/libs/humanmsg-1.0/humanmsg.js"></script>


[humanizedmessages]: http://humanized.com/weblog/2006/09/11/monolog_boxes_and_transparent_messages/
[humanmsg]: http://code.google.com/p/humanmsg/

Messages can be send like this:

    humanMsg.displayMsg("<strong>Fehler:</strong> ungültige Artikelnummer: '" + artnrraw + "'");


## Formulare

Wir verwenden die HTML 5 Attribute `placeholder` `autofocus` und `required`. Hilfe dazu gibt es z.B. im
Artikel "[A Form of Madness][pilgrim]". Da Firefox momentan diese attribute incht korrekt unterstützt,
nutzen wir ein [jQuery Plugin][formhelper], um die Funktionalität nachzurüsten. Aktiviert wird das so:

    <script type="text/javascript" src="http://s.hdimg.net/libs/nmcFormHelper.js"></script>
    <script type="text/javascript">
        $(document).ready(function() { nmcFormHelper.init(); });
    </script>

[pilgrim]: http://diveintohtml5.org/forms.html
[formhelper]: http://www.newmediacampaigns.com/page/nmcformhelper

### Field Validation

Fehler in Feldern zeigen wir durch

    $("#artnr").effect('pulsate', {}, 100);

## Icons

<img src="http://static.23.nu/md/Pictures/ZZ2E01098C.png" width="78" height="72" alt="" align="left">Wir
versuchen Piktogramme einheitlich zu nutzen. Nebenan ein Beispiel aus dem "anbietr" System. Die einzige
Piktogrammnutzung, die sich vieleicht nicht auf Anhieb erschliesst ist "Protokoll".

Rot würde sich für "Fehler", orange für "Warnung" und Grün für "OK" anbieten. Oder ist Grün erledigt, Orange
in Arbeit und "Rot" wartet auf etwas anderes? Wir sollten uns auf eine eigene Farbe für "clickable" Links
nehmen. Die Wahl von "Orange" in anbietr war vieleicht nicht so gut, weil orange sich so gut für "Warnung"
eignet. Alternativen wären <img src="http://www.hudora.de/media/chameleon/blue/new.gif" /> <img
src="http://www.hudora.de/media/chameleon/black/new.gif" /> und <img
src="http://www.hudora.de/media/chameleon/silver/new.gif" />. Eigentlich macht Blau ja Sinn, aber das setzt
sich natürlich kaum von unserem sonstigen, bläulichen Design ab. Silver/grau ist elegant aber vielleicht ein
bisschen unauffällig?

Auch im Auge behalten: Bei uns arbeiten aus statistischer Sicht 2-3 Farbenblinde. Das ist generell ein
Problem, wenn man sich mal die icons bei "simulierter Farbenblindheit" anschaut:

<img src="http://static.23.nu/md/Pictures/ZZ609E1EAB.png" width="153" height="159" alt="" /><img
src="http://static.23.nu/md/Pictures/ZZ0E8EC602.png" width="153" height="159" alt="" />

So gesehen können wir wohl NUR rot und grün zur Unterscheidung vergessen.

Die bisher verwendeten Icons sind:

* <img src="http://www.hudora.de/media/chameleon/blue/bookmark.gif" alt="Historie" /> Protokoll
* <img src="http://www.hudora.de/media/chameleon/blue/edit.gif" alt="bearbeiten" /> bearbeiten
* <img src="http://www.hudora.de/media/chameleon/blue/copy_paste.gif" alt="Kopieren" /> kopieren
* <img src="http://www.hudora.de/media/chameleon/blue/trash.gif" /> löschen (entgültig)
* <img src="http://www.hudora.de/media/chameleon/green/check.gif" /> True / OK
* <img src="http://www.hudora.de/media/chameleon/red/close.gif" /> False / Problem
* <img src="http://www.hudora.de/media/chameleon/silver/remove.gif" /> weniger / entfernen
* <img src="http://www.hudora.de/media/chameleon/silver/add.gif" /> neu / mehr
* <img src="http://www.hudora.de/media/chameleon/silver/email.gif" /> KEP / Senden
* <img src="http://www.hudora.de/media/chameleon/silver/time.gif" /> Fixtermin
* <img src="http://www.hudora.de/media/chameleon/silver/new.gif" /> generisch (die Farbe machts hier, aber s.o.)
* <img src="http://www.hudora.de/media/chameleon/blue/user.gif" /> öffentliche Web-Seite
* <img src="http://www.hudora.de/media/chameleon/blue/clipboard.gif" /> Prüfen
* <img src="http://www.hudora.de/media/chameleon/blue/calculator.gif" /> Berechnen / Bewerten

Ein bisschen unklar ist Anbruch Exportkarton, Anbruch VE1 und und Komissionierung mit Stapler (Pick) von
Hand (Retrieval). Ein (ehr schlechter) Vorschlag:

* <img src="http://www.hudora.de/media/chameleon/silver/unlocked.gif" /> Anbruch Exportkarton
* <img src="http://www.hudora.de/media/chameleon/orange/unlocked.gif" /> Anbruch VE1 (schlimmer)
* <img src="http://www.hudora.de/media/chameleon/silver/shopping_cart.gif" /> Komissionierung von Hand
