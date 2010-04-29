#!/usr/local/bin/bash

BASEDIR=${BASEDIR:-"/usr/local/SPEDITION/kommibelege"}

HOSTNAME=${HOSTNAME:-"FTPSERVER"}
USERNAME=${USERNAME:-"FTPUSER"}
PASSWORD=${PASSWORD:-"FTPPASSWORD"}

STYLESHEET='doc/standards/examples/wms2logos_kommiauftrag.xslt'

UPLOADDIR="$BASEDIR/uploads"
WORKDIR="$BASEDIR/work"
ARCHIVDIR="$BASEDIR/archiv"

mkdir -p $UPLOADDIR
mkdir -p $ARCHIVDIR

# Valide xml Dateien in entsprechendes Format konvertieren und ins Upload Verzeichnis stellen
for file in $WORKDIR/*
do
    if xmllint "$file" > /dev/null 2>&1
    then
        outfile="$UPLOADDIR/$(basename $file)"
        xsltproc -o $outfile.xml $STYLESHEET $file
        mv $file $ARCHIVDIR
    fi
done

# alle vorhandenen Daten hochladen und aus dem Uploaddir entfernen
lftp -c "debug 6 ; open  -u $USERNAME,$PASSWORD $HOSTNAME; mirror --Remove-source-files --reverse --verbose=1 $UPLOADDIR in" > /dev/null 2>> $BASEDIR/lftp.log
