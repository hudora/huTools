<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output indent="no" omit-xml-declaration="yes" method="text" encoding="UTF-8" media-type="text/x-json"/>
        
    <xsl:template match="/Auftragsliste">
        <xsl:text>{"kommiauftragsnr": </xsl:text>
        <xsl:value-of select="descendant::FremdlieferscheinNr" /><xsl:text>,</xsl:text>

        <xsl:text>"spedition": </xsl:text>
        <xsl:text>"</xsl:text>
        <xsl:apply-templates select="//Versandart" />
        <xsl:text>"</xsl:text>
        <xsl:text>,</xsl:text>
        
        <xsl:text>
            "positionen": [
        </xsl:text>
        <xsl:for-each select="descendant::Auftragspositionen/Position">
            <xsl:text>{</xsl:text>
            <xsl:text>"menge": </xsl:text>
            <xsl:value-of select="descendant::MengeEH1" />
            <xsl:text>, </xsl:text>

            <xsl:if test="descendant::FremdPos1">
                <xsl:text>"posnr": </xsl:text>
                <xsl:value-of select="descendant::FremdPos1" />
                <xsl:text>, </xsl:text>
            </xsl:if>

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

    <xsl:template match="//Versandart">
        <xsl:choose>
            <xsl:when test="//Versandart='MAEIND'">Maeuler</xsl:when>
            <xsl:when test="//Versandart='MAEEXP'">Maeuler</xsl:when>
            <xsl:when test="//Versandart='DPDSTA'">DPD</xsl:when>
            <xsl:when test="//Versandart='DPDUNF'">DPD</xsl:when>
            <xsl:when test="//Versandart='DHL'">DHL</xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="//Versandart" />
            </xsl:otherwise>
        </xsl:choose>
</xsl:template>
</xsl:stylesheet>
