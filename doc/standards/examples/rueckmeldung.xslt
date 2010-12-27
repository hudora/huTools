<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="Auftrag">
        <rueckmeldung>
            <xsl:apply-templates select="Auftragskopf"/>
            <xsl:apply-templates select="Auftragspositionen"/>
            <nves>
                <xsl:for-each select="Auftragspositionen/Position">
                    <nve>
                        <art>Paket</art>
                        <gewicht>0</gewicht>
                        <nve><xsl:value-of select="Packst&#xFC;cknummer"/></nve>
                    </nve>
                </xsl:for-each>
            </nves>
        </rueckmeldung>
    </xsl:template>
    <xsl:template match="Auftragskopf">
        <guid>
            <xsl:value-of select="FremdlieferscheinNr"/>
        </guid>
    </xsl:template>
    <xsl:template match="Auftragspositionen">
        <positionen>
            <xsl:for-each select="Position">
                <position>
                    <nve>
                        <xsl:value-of select="Packst&#xFC;cknummer"/>
                    </nve>
                    <posnr>
                        <xsl:value-of select="FremdPos1"/>
                    </posnr>
                    <menge>
                        <xsl:value-of select="MengeEH1"/>
                    </menge>
                    <artnr>
                        <xsl:value-of select="ArtikelNr"/>
                    </artnr>
                    <referenzen>
                        <charge>
                            <xsl:value-of select="Charge"/>
                        </charge>
                    </referenzen>
                </position>
            </xsl:for-each>
        </positionen>
    </xsl:template>
</xsl:stylesheet>
