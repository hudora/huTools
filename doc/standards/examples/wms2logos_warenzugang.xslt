<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:output method="html"/>
<xsl:output method="xml" indent="yes" version="1.0"/>

<xsl:template match="child::warenzugang">
<Auftragsliste>
    <Auftrag>
        <Auftragskopf>
            <EinlagererNr>UNKLAR</EinlagererNr>
            <FremdlieferscheinNr><xsl:value-of select="descendant::guid" /></FremdlieferscheinNr>
            <KundenauftragsNr><xsl:value-of select="descendant::batchnr" /></KundenauftragsNr>
        </Auftragskopf>
        <Lieferantenanschrift>
            <LieferantenkundenNr>UNKLAR</LieferantenkundenNr>
            <LieferantenName1>Hudora</LieferantenName1>
            <LLaenderkennzeichen>DE</LLaenderkennzeichen>
            <LPLZ>42897</LPLZ>
            <LOrt>Remscheid</LOrt>
            <LStrasse>Jägerwald</LStrasse>
        </Lieferantenanschrift>
        <Auftragspositionen>
            <Position>
                <MengeEH1><xsl:value-of select="descendant::menge" /></MengeEH1>
                <ArtikelNr><xsl:value-of select="descendant::artnr" /></ArtikelNr>
                <Charge>noch leer</Charge>
            </Position>
        </Auftragspositionen>
    </Auftrag>
</Auftragsliste>
</xsl:template>
</xsl:stylesheet>