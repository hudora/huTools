<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:output method="html"/>
    <xsl:output method="xml" indent="yes" version="1.0"/>
    <xsl:template match="/Auftragsliste">
        <rueckmeldung>
            <kommiauftragsnr><xsl:value-of select="descendant::FremdlieferscheinNr" /></kommiauftragsnr>
            <positionen>
                <xsl:for-each select="descendant::Auftragspositionen/Position">
                    <position>
                        <nve><xsl:value-of select="descendant::Packstücknummer" /></nve>
                        <posnr><xsl:value-of select="descendant::FremdPos1" /></posnr>
                        <menge><xsl:value-of select="descendant::MengeEH1" /></menge>
                        <artnr><xsl:value-of select="descendant::ArtikelNr" /></artnr>
                    </position>
                </xsl:for-each>
            </positionen>
        </rueckmeldung>
    </xsl:template>
</xsl:stylesheet>
