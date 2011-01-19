#!/usr/local/bin/bash
#
# Skript zur Übertragung von Kommiaufträgen zu Mäuler
#
# Die Aufträge im huLogi-Format werden per XSLT in das Format von Gigaton LogoS
# konvertiert und dann per FTP hochgeladen.
#
# Die Dateien werden anschließend archiviert.

BASEDIR=${BASEDIR:-"/usr/local/SPEDITION/kommibelege"}

# FTP-Zugangsdaten
HOSTNAME=${HOSTNAME:-"FTPSERVER"}
USERNAME=${USERNAME:-"FTPUSER"}
PASSWORD=${PASSWORD:-"FTPPASSWORD"}

STYLESHEET=${STYLESHEET:-'doc/standards/examples/wms2logos_kommiauftrag.xslt'}

# Verzeichnisse: 
NEWDIR="$BASEDIR/new"         # Verzeichnis mit neuen Dateien
WORKDIR="$BASEDIR/work"       # Verzeichnis mit konvertierten Dateien
ARCHIVDIR="$BASEDIR/archiv"   # Archivverzeichnis

mkdir -p $NEWDIR $WORKDIR $ARCHIVDIR

# nullglob
# If set, Bash allows filename patterns which match no files to expand to a null string, rather than themselves. 
shopt -s nullglob

for file in $NEWDIR/*; do
    outfile="$WORKDIR/$(basename $file).xml"
    xsltproc -o $outfile $STYLESHEET $file
    cp $outfile $ARCHIVDIR
    mv $file $ARCHIVDIR
done

# alle vorhandenen Daten hochladen und aus dem Arbeitsverzeichnis entfernen
echo "--------------------" $(date) >> $BASEDIR/lftp.log
lftp -c "debug 6 ; open -u $USERNAME,$PASSWORD $HOSTNAME; mirror --Remove-source-files --reverse --verbose=1 $WORKDIR in" > /dev/null 2>> $BASEDIR/lftp.log
