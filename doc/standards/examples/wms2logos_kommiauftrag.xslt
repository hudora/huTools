<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:output method="html"/>
<xsl:output method="xml" indent="yes" version="1.0" encoding="utf-8" />


<xsl:template match="/kommiauftrag">
<Auftragsliste>
    <Auftrag>
        <Auftragskopf>
            <EinlagererNr>10056</EinlagererNr>
            <FremdlieferscheinNr><xsl:value-of select="descendant::kommiauftragsnr" /></FremdlieferscheinNr>
            <KundenauftragsNr><xsl:value-of select="descendant::auftragsnr" /></KundenauftragsNr>
        </Auftragskopf>
        <Auftragsinformationen>
            <Liefertermin>
                <xsl:value-of select="translate(descendant::anliefertermin, '-:', '')" />
            </Liefertermin>
            <!-- Terminart -->
            <Terminart>
                <xsl:choose>
                    <xsl:when test="/kommiauftrag/fixtermin = 'True'">FIX</xsl:when>
                    <xsl:otherwise>BIS</xsl:otherwise>
                </xsl:choose>
            </Terminart>
            <Textcode1>8</Textcode1>
            <Auftragstext>
                <xsl:for-each select="descendant::versandeinweisung">
                    <xsl:if test="contains('packliste
                                            separater_lieferschein
                                            avisieren_unter
                                            abholer
                                            hebebuehne',
                                            bezeichner)">
                        <xsl:value-of select="bezeichner" />
                        <xsl:text>: </xsl:text>
                        <xsl:value-of select="anweisung" />
                        <xsl:if test="following-sibling::*">$</xsl:if>
                    </xsl:if>
                </xsl:for-each>
            </Auftragstext>
            <Textcode2>2</Textcode2>
            <Kommissioniertext>
                <xsl:for-each select="descendant::versandeinweisung">
                    <xsl:if test="contains('packhoehe
                                            sortenrein
                                            etiketten
                                            etiketten_speicherort',
                                            bezeichner)">
                        <xsl:value-of select="bezeichner" />
                        <xsl:text>: </xsl:text>
                        <xsl:value-of select="anweisung" />
                        <xsl:if test="following-sibling::*">$</xsl:if>
                    </xsl:if>
                </xsl:for-each>
            </Kommissioniertext>
            <EmpfaengerILN><xsl:value-of select="descendant::iln" /></EmpfaengerILN>
            <Auftragsprioritaet><xsl:value-of select="prioritaet" /></Auftragsprioritaet>
            <Versandart>
                <xsl:apply-templates select="packanweisungen/palettenversand" />
            </Versandart>
            <Frankatur>
                <xsl:call-template name="TMPL_UNFREI" />
            </Frankatur>
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
                <MengeEH1><xsl:value-of select="number(descendant::menge)" /></MengeEH1>
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

<xsl:template match="packanweisungen/palettenversand">
        <xsl:choose>
            <xsl:when test="/kommiauftrag/packanweisungen/palettenversand/text()='True' and /kommiauftrag/versandvorschriften/versandvorschrift/bezeichner/text()='unfrei'">DHL</xsl:when>
            <xsl:when test="/kommiauftrag/packanweisungen/palettenversand/text()='True' and /kommiauftrag/land='DE'">MAEIND</xsl:when>
            <xsl:when test="/kommiauftrag/packanweisungen/palettenversand/text()='True' and /kommiauftrag/land!='DE'">MAEEXP</xsl:when>
            <xsl:when test="/kommiauftrag/packanweisungen/palettenversand/text()='False' and /kommiauftrag/versandvorschriften/versandvorschrift/bezeichner/text()='unfrei'">DPDUNF</xsl:when>
            <xsl:when test="/kommiauftrag/versandvorschriften/item/bezeichner/text()='selbstabholer'">Selbstabholer</xsl:when>
            <xsl:otherwise>DPDSTA</xsl:otherwise>
        </xsl:choose>
</xsl:template>

<xsl:template name="TMPL_UNFREI">
        <xsl:choose>
            <xsl:when test="/kommiauftrag/versandvorschriften/versandvorschrift/bezeichner/text()='unfrei'">UNFR</xsl:when>
            <xsl:otherwise>FRHS</xsl:otherwise>
        </xsl:choose>
</xsl:template>

</xsl:stylesheet>