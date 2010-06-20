# Artikelstammdatenformat

Dies ist das grundlegende Format für Artikelstammdaten, dass bei [Hudora][1] verwendet wird.

[1]: http://www.hudora.de/

## Pflichtfelder

* **`artnr`** - Eindeuteige Artikelnummer des Artikels. Kann Alphanummerische Zeichen, "/" und "-" beinhalten.
* **`name`** - Beschreibender Name des Artikels. Nicht eindeutig.
* **`ean`** - [EAN/GTIN][1] des Artikels. Nicht eindeutig.

[2]: http://de.wikipedia.org/wiki/European_Article_Number


## Zusatzfelder

* **`name_en`** - Englischer, beschreibener Name des Artikels.
* **`package_weight`** - Bruttogewicht der Produktverpackung in Gramm
* **`package_size_l`** - Länge der Produktverpackung in mm
* **`package_size_b`** - Breite der Produktverpackung in mm
* **`package_size_h`** - Höhe der Produktverpackung in mm
* **`package_volume`** - Volumen der Produktverpackung in Litern
* **`products_per_ve1`** - Artikel pro VE1 (kann auch leer oder "1" sein). Die VE1 ist eine
  "Unterverpackung", mit der bei uns diverse kleinre Artikel inerhalb eines Exportkartons wieter
  strukturiert sind. Eine VE1 ist bei vielen Artikeln *nicht* vorhanden.
* **`ve1_weight`** - Bruttogewicht der VE1 in Gramm
* **`ve1_size_l`** - Länge der VE1 in mm
* **`ve1_size_b`** - Breite der VE1 in mm
* **`ve1_size_h`** - Höhe der VE1 in mm
* **`ve1_volume`** - Volumen der VE1 in Litern
* **`no_export_package`** - Artikel wird ohne Exportkarton verladen
* **`products_per_export_package`** - Artikel pro Exportkarton (kann auch leer oder "1" sein)
* **`export_package_weight`** - Bruttogewicht des Exportkartons in Gramm
* **`export_package_size_l`** - Länge der Exportverpackung in mm
* **`export_package_size_b`** - Breite der Exportverpackung in mm
* **`export_package_size_h`** - Höhe der Exportverpackung in mm
* **`export_package_volume`** - Volumen der Exportverpackung in Litern
* **`export_package_ean`** - EAN der Exportverpackung - Abweichend von der Artikel-EAN
* **`palettenfaktor`** - Anzahl der Artikel pro Palette
* **`export_packages_per_layer`** - Exportkartons pro Lage auf der Palette
* **`pallet_height`** - Palettenhöhe incl. Holz
* **`pallet_weight`** - Palettengewicht in g excl. Holz
* **`to_big_for_pallet`** - "True" Wennd ie ware überstand auf der Palette hat, "False" wenn nicht.
* **`pallet_ean`** - EAN der Palette - Abweichend von der Artikel-EAN
* **`pallet_scheme`** - Gezeichnetes Paletten-Packschema (URL)
* **`pallet_photo`** - Foto einer Korrekt gepacken Palette (URL)
* **`pallet_volume`** - Volumen der Kartons auf einer PAlette in Litern
* **`logistik_info`** - Weitere logistische Informationen. Freitext
* **`statistische_waren_nr`** - Nummer für die Verzollung
* **`warenklassifikation`** - Warenklassifikation nach GS1 Standard
* **`handbook`** - Bedienungsanleitung für den Artikel (URL)
* **`sprengzeichnung`** - Sprengzeichnung des Artikels (URL)
* **`products_in_20ft_container`** - Anzahl der Artikel in einem 20-Fuss Container
* **`products_in_40ft_container`** - Anzahl der Artikel in einem 40-Fuss Container
* **`products_in_40fthq_container`** - Anzahl der Artikel in einem 40-Fuss High-Cube Container
* **`image`** - Produktbild (URL) 

   "set_consiting_of": [], 
   "features": [], 

### Folgende Felder werden in zukünftigen Versionen entfernt:

* **`einheit`** - Mengeneinheit wie Stück, Paar usw.


## Beispiel

    <articles>
     <article>
      <artnr>01104</artnr>
      <name>joey's Skate Set, Gr&#xF6;&#xDF;e 30-33 mit Rucksack und Protektoren</name>
      <name_en>joey's Skate Set, size 30-33, backpack+protectors</name_en>
      <ean>4005998011041</ean>
      <package_weight>2440</package_weight>
      <package_size_l>200</package_size_l>
      <package_size_b>270</package_size_b>
      <package_size_h>300</package_size_h>
      <package_volume>16.2</package_volume>
      <products_per_ve1/>
      <ve1_weight/>
      <ve1_size_l/>
      <ve1_size_b/>
      <ve1_s ize_h/>
      <ve1_volume/>
      <no_export_package>False</no_export_package>
      <export_package_ean>4005998000854</export_package_ean>
      <export_package_weight>11760</export_package_weight>
      <export_package_size_l>527</export_package_size_l>
      <export_package_size_b>267</export_package_size_b>
      <export_package_size_h>432</export_package_size_h>
      <export_package_volume>60.786288</export_package_volume>
      <products_per_export_package>4</products_per_export_package>
      <export_packages_per_layer/>
      <export_packages_per_pallet>24</export_packages_per_pallet>
      <pallet_height/>
      <palettenfaktor>96</palettenfaktor>
      <pallet_weight>282240</pallet_weight>
      <to_big_for_pallet>False</to_big_for_pallet>
      <pallet_ean>4005998041468</pallet_ean>
      <pallet_scheme/>
      <pallet_photo/>
      <pallet_volume>1458.870912</pallet_volume>
      <logistik_info/>
      <statistische_waren_nr>95067030</statistische_waren_nr>
      <warenklassifikation>4495</warenklassifikation>
      <handbook/>
      <catalog_page/>
      <sprengzeichnung/>
      <products_in_20ft_container>1960</products_in_20ft_container>
      <products_in_40ft_container>4000</products_in_40ft_container>
      <products_in_40fthq_container>4400</products_in_40fthq_container>
      <image>http://www.hudora.de/media/,/-/product/image/188c2b81cefa798fd5e6702700604d0a.jpg/svga.jpeg</image>
      <image></images>
     </article>
    </articles>


## JSON

## Artikels

### Beispiel

    {"artnr": 01104,
     "name": "joey's Skate Set, Gr&#xF6;&#xDF;e 30-33 mit Rucksack und Protektoren",
     "name_en": "joey's Skate Set, size 30-33, backpack+protectors",
     "einheit": "stueck",
     "ean": 4005998011041,
     "package_weight": 2440,
     "package_size_l": 200,
     "package_size_b": 270,
     "package_size_h": 300,
     "package_volume": "16.2",
     "products_per_ve1": "",
     "ve1_weight": "",
     "ve1_size_l": "",
     "ve1_size_b": "",
     "ve1_size_h": "",
     "ve1_volume": "",
     "no_export_package": "False",
     "export_package_ean": 4005998000854,
     "export_package_weight": 11760,
     "export_package_size_l": 527,
     "export_package_size_b": 267,
     "export_package_size_h": 432,
     "export_package_volume": "60.786288",
     "products_per_export_package": 4,
     "export_packages_per_layer": "",
     "export_packages_per_pallet": "24",
     "pallet_height": "",
     "palettenfaktor": 96,
     "pallet_weight": 282240,
     "to_big_for_pallet": "False",
     "pallet_ean": 4005998041468,
     "pallet_scheme": "",
     "pallet_photo": "",
     "pallet_volume": "1458.870912",
     "logistik_info": "",
     "statistische_waren_nr": 95067030,
     "warenklassifikation": 4495,
     "handbook": "",
     "catalog_page": "",
     "sprengzeichnung": "",
     "products_in_20ft_container": 1960,
     "products_in_40ft_container": 4000,
     "products_in_40fthq_container": 4400,
     "image":
     "http://www.hudora.de/media/,/-/product/image/188c2b81cefa798fd5e6702700604d0a.jpg/svga.jpeg",
     "image": ""}
