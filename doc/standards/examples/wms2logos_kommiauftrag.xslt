<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:output method="html"/>
<xsl:output method="xml" indent="yes" version="1.0"/>

<xsl:template match="kommiauftrag">
<Auftragsliste>
    <Auftrag>
        <Auftragskopf>
            <EinlagererNr>10056</EinlagererNr>
            <FremdlieferscheinNr><xsl:value-of select="descendant::kommiauftragsnr" /></FremdlieferscheinNr>
            <KundenauftragsNr><xsl:value-of select="descendant::auftragsnr" /></KundenauftragsNr>
        </Auftragskopf>
        <Auftragsinformationen>
            <Liefertermin><xsl:value-of select="translate(descendant::anliefertermin, '-:', '')" /></Liefertermin>
            <Textcode1>8</Textcode1>
            <Auftragstext><xsl:value-of select="descendant::info_kunde" /></Auftragstext>
            <Textcode2>2</Textcode2>
            <Kommissioniertext>
                <xsl:for-each select="descendant::versandeinweisung">
                    <xsl:if test="contains('packhoehe
                                            sortenrein
                                            etiketten
                                            etiketten_speicherort',
                                            bezeichner)">
                        <xsl:text>
                        </xsl:text> 
                        <xsl:value-of select="bezeichner" />
                        <xsl:text>: </xsl:text>
                        <xsl:value-of select="anweisung" />
                        <!--FIXME: Hier noch ein Trennzeichen o.ä.? -->
                    </xsl:if>
                </xsl:for-each>
            </Kommissioniertext>
            <EmpfaengerILN><xsl:value-of select="descendant::iln" /></EmpfaengerILN>
            <Auftragsprioritaet><xsl:value-of select="105010 - prioritaet" /></Auftragsprioritaet>
        </Auftragsinformationen>
        <Empfaengeranschrift>
            <EmpfaengerkundenNr><xsl:value-of select="descendant::kundennr" /></EmpfaengerkundenNr>
            <EmpfaengerName1><xsl:value-of select="descendant::name1" /></EmpfaengerName1>
            <EmpfaengerName2><xsl:value-of select="descendant::name2" /></EmpfaengerName2>
            <ELaenderkennzeichen><xsl:value-of select="descendant::land" /></ELaenderkennzeichen>
            <EPLZ><xsl:value-of select="descendant::plz" /></EPLZ>
            <EOrt><xsl:value-of select="descendant::ort" /></EOrt>
            <EStrasse><xsl:value-of select="descendant::strasse" /></EStrasse>
            <ETelefonNr><xsl:value-of select="descendant::tel" /></ETelefonNr>
            <EEmail><xsl:value-of select="descendant::mail" /></EEmail>
        </Empfaengeranschrift>
        <Auftragspositionen>
            <xsl:for-each select="descendant::position">
            <Position>
                <MengeEH1><xsl:value-of select="descendant::menge" /></MengeEH1>
                <ArtikelNr><xsl:value-of select="descendant::artnr" /></ArtikelNr>
                <FremdPos1><xsl:value-of select="descendant::posnr" /></FremdPos1>
                <Warenbezeichnung><xsl:value-of select="descendant::text" /></Warenbezeichnung>
                <EAN><xsl:value-of select="descendant::ean" /></EAN>
            </Position>
            </xsl:for-each>
        </Auftragspositionen>
    </Auftrag>
</Auftragsliste>
</xsl:template>
</xsl:stylesheet>
