<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output indent="no" omit-xml-declaration="yes" method="text" encoding="UTF-8" media-type="text/x-json"/>
        
    <xsl:output method="xml" indent="yes" version="1.0"/>
    <xsl:template match="/Auftragsliste">
        <xsl:text>{"kommiauftragsnr": </xsl:text>
        <xsl:value-of select="descendant::FremdlieferscheinNr" /><xsl:text>,</xsl:text>
        <xsl:text>
            "positionen": [
        </xsl:text>
        <xsl:for-each select="descendant::Auftragspositionen/Position">
            <xsl:text>{</xsl:text>
            <xsl:text>"menge": </xsl:text>
            <xsl:value-of select="descendant::MengeEH1" />
            <xsl:text>, </xsl:text>

            <xsl:text>"posnr": </xsl:text>
            <xsl:value-of select="descendant::FremdPos1" />
            <xsl:text>, </xsl:text>

            <xsl:text>"artnr": </xsl:text>
            <xsl:text>"</xsl:text>
            <xsl:value-of select="descendant::ArtikelNr" />
            <xsl:text>",</xsl:text>

            <xsl:text>
                "nve":
            </xsl:text>
            <xsl:text>"</xsl:text>
            <xsl:value-of select="descendant::Packstücknummer" />
            <xsl:text>"</xsl:text>
            <xsl:text>}</xsl:text>
            <xsl:if test="following-sibling::*">, </xsl:if>
        </xsl:for-each>
        <xsl:text> ]}</xsl:text>
    </xsl:template>
</xsl:stylesheet>
