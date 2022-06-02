#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It generates the list of pre-candidate fusion genes. This list is hard coded
in here and it is manually curated from healthy human brains (BA9 prefrontal cortex)
from <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE68719>.



Author: Daniel Nicorici, Daniel.Nicorici@gmail.com

Copyright (c) 2009-2022 Daniel Nicorici

This file is part of FusionCatcher.

FusionCatcher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FusionCatcher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FusionCatcher (see file 'COPYING.txt').  If not, see
<http://www.gnu.org/licenses/>.

By default, FusionCatcher is running BLAT aligner
<http://users.soe.ucsc.edu/~kent/src/> but it offers also the option to disable
all its scripts which make use of BLAT aligner if you choose explicitly to do so.
BLAT's license does not allow to be used for commercial activities. If BLAT
license does not allow to be used in your case then you may still use
FusionCatcher by forcing not use the BLAT aligner by specifying the option
'--skip-blat'. Fore more information regarding BLAT please see its license.

Please, note that FusionCatcher does not require BLAT in order to find
candidate fusion genes!

This file is not running/executing/using BLAT.

"""
import sys
import os
import optparse
import symbols

if __name__ == '__main__':

    #command line parsing

    usage = "%prog [options]"
    description = """It generates the list of pre-candidate fusion genes from healthy human brains."""
    version = "%prog 0.12 beta"

    parser = optparse.OptionParser(usage=usage,description=description,version=version)

    parser.add_option("--organism",
                      action = "store",
                      type = "string",
                      dest = "organism",
                      default = "homo_sapiens",
                      help="""The name of the organism for which the list of allowed candidate fusion genes is generated, e.g. homo_sapiens, mus_musculus, etc. Default is '%default'.""")

    parser.add_option("--output",
                      action="store",
                      type="string",
                      dest="output_directory",
                      default = '.',
                      help="""The output directory where the list of allowed candidate fusion genes is generated. Default is '%default'.""")

    parser.add_option("--skip-filter-overlap",
                      action="store_true",
                      dest="skip_filter_overlap",
                      default = False,
                      help="""If set then it filters out the known fusion genes where the (i) genes are fully overlapping, or (ii) the genes are partially overlapping and are on the same strand. Default is '%default'.""")

    (options,args) = parser.parse_args()

    # validate options
    if not (options.output_directory
            ):
        parser.print_help()
        sys.exit(1)


    #
    #
    #

    print "Generating the list of allowed/known fusion genes..."
    fusions = dict()

    # manual curation from papers

    fusions['rattus_norvegicus'] = []

    fusions['mus_musculus'] = []

    fusions['canis_lupus_familiaris'] = []

    fusions['homo_sapiens'] = [
        ['A1BG-AS1','AC012313.2'],
        ['AACS','UBC'],
        ['AARS2','CA5A'],
        ['AARS2','PSME4'],
        ['ABCC5','TMEM178A'],
        ['ABHD11','AC118553.2'],
        ['ABHD17A','CCDC144NL-AS1'],
        ['ABHD18','LMNTD1'],
        ['AC000095.1','AC007326.1'],
        ['AC000095.2','DGCR5'],
        ['AC004551.1','NDUFC2'],
        ['AC004951.1','DTX2P1-UPK3BP1-PMS2P11'],
        ['AC005154.3','GOLGA8R'],
        ['AC005225.2','HEATR4'],
        ['AC005412.3','MYO18A'],
        ['AC005532.1','C1GALT1'],
        ['AC005550.1','MEOX2'],
        ['AC005670.2','LRRC37A2'],
        ['AC005736.2','LIMA1'],
        ['AC005829.1','C17ORF58'],
        ['AC006210.2','RDX'],
        ['AC006504.5','FAM107A'],
        ['AC007388.1','AP000442.1'],
        ['AC007391.1','NDUFAF7'],
        ['AC007966.1','FSIP2-AS1'],
        ['AC008105.1','AC008105.3'],
        ['AC008507.1','TAF9'],
        ['AC008736.1','COQ7'],
        ['AC008759.2','NABP2'],
        ['AC008969.1','RBM8A'],
        ['AC009053.1','PDPR'],
        ['AC009533.1','DDX11'],
        ['AC009812.3','AC104452.1'],
        ['AC010168.2','SS18'],
        ['AC010655.4','METTL2A'],
        ['AC010931.2','VSNL1'],
        ['AC011337.1','SLC36A1'],
        ['AC011477.2','AC022558.1'],
        ['AC011498.2','CHAF1A'],
        ['AC011603.2','CAMK2N1'],
        ['AC011603.2','FAM107A'],
        ['AC011603.2','PNMA2'],
        ['AC011767.1','AC091951.1'],
        ['AC012358.1','LINC00957'],
        ['AC015908.2','TMEM220-AS1'],
        ['AC016168.2','MGAT5B'],
        ['AC016588.2','TMX1'],
        ['AC016597.1','GNAO1'],
        ['AC017104.1','ARMC9'],
        ['AC018638.2','AL606534.5'],
        ['AC018648.1','DPY19L1'],
        ['AC019080.4','NMT2'],
        ['AC019205.2','IL3RA'],
        ['AC020663.2','TAF15'],
        ['AC020763.4','SLC22A17'],
        ['AC020922.3','IL11'],
        ['AC021054.1','ATRNL1'],
        ['AC021683.1','PAAF1'],
        ['AC022211.4','ICOSLG'],
        ['AC022400.5','AGAP4'],
        ['AC022596.2','AC104024.2'],
        ['AC022784.7','ERI1'],
        ['AC023283.1','SHTN1'],
        ['AC024575.1','EPOR'],
        ['AC024937.2','PPP4R2'],
        ['AC025465.1','LINC01170'],
        ['AC025588.1','PTCD3'],
        ['AC026461.1','SNCA'],
        ['AC026523.1','LINC00923'],
        ['AC026790.1','TAF15'],
        ['AC027281.2','VAC14-AS1'],
        ['AC048341.2','MON2'],
        ['AC068279.1','AC245060.6'],
        ['AC068492.1','DARS-AS1'],
        ['AC068587.6','AC107918.4'],
        ['AC068831.2','CERK'],
        ['AC069061.2','AC233702.10'],
        ['AC069133.1','LINC01289'],
        ['AC073133.2','LINC01006'],
        ['AC073263.1','TET3'],
        ['AC073342.1','KEL'],
        ['AC073575.1','VPS53'],
        ['AC073610.3','WNT10B'],
        ['AC079328.2','FAM13C'],
        ['AC079907.2','WASHC3'],
        ['AC087280.2','OR2AG2'],
        ['AC087386.1','IGK@'],
        ['AC087392.3','STX1B'],
        ['AC091271.1','EBF1'],
        ['AC092143.1','TCF25'],
        ['AC092437.1','STX18-AS1'],
        ['AC092490.2','RIMKLB'],
        ['AC093014.1','RWDD1'],
        ['AC096536.3','TMEM61'],
        ['AC098679.2','AIDA'],
        ['AC098850.5','USP32'],
        ['AC099062.1','LMO4'],
        ['AC100830.1','ZNF609'],
        ['AC100868.1','KMT2C'],
        ['AC103564.1','C9ORF172'],
        ['AC103923.1','ATG4C'],
        ['AC104066.2','DANCR'],
        ['AC104411.1','KRT8'],
        ['AC104452.1','CEP104'],
        ['AC104452.1','RPL7L1'],
        ['AC105094.2','RNF152'],
        ['AC108471.2','UBE2K'],
        ['AC109460.3','NFATC2IP'],
        ['AC112907.2','MCF2L2'],
        ['AC114296.1','SLC25A48'],
        ['AC116562.4','LINC00937'],
        ['AC116565.2','PDE6B'],
        ['AC119044.1','PCED1B-AS1'],
        ['AC124276.1','PXMP4'],
        ['AC127526.5','ERVK-28'],
        ['AC129492.3','TMEM107'],
        ['AC135012.1','SLC2A11'],
        ['AC136944.1','IGK@'],
        ['AC138409.2','AC138866.2'],
        ['AC211485.1','USP14'],
        ['AC234783.1','H2BFM'],
        ['AC239798.4','HIST2H2BA'],
        ['AC239809.3','HYDIN2'],
        ['AC242426.3','CHD1L'],
        ['AC243829.1','CCL4L2'],
        ['AC245123.1','AC246817.2'],
        ['AC245297.3','LINC01138'],
        ['AC245884.4','MRI1'],
        ['AC245884.4','TIAL1'],
        ['ACAN','MAPKBP1'],
        ['ACSL6','FAM189B'],
        ['ACSL6','LINC00887'],
        ['ACTB','ICA1L'],
        ['ACTB','MBP'],
        ['ACTN1','DNAJA2'],
        ['ACTR10','GUCY1B3'],
        ['ACVR2B','GABRA2'],
        ['ACVR2B','TNR'],
        ['ACYP1','NEK9'],
        ['ACYP2','DDX5'],
        ['ADAM23','EPB41L4B'],
        ['ADAM23','FOCAD'],
        ['ADARB1','PPP1R9B'],
        ['ADCY1','FRRS1L'],
        ['ADD3-AS1','XPNPEP1'],
        ['ADGRB3','LMBRD1'],
        ['ADGRF1','FBXO44'],
        ['ADIRF','SNCG'],
        ['ADORA1','LINC01353'],
        ['AF038458.1','LYRM2'],
        ['AF254983.1','TPTE2'],
        ['AK5','KCNIP4'],
        ['AKAP11','NECTIN3'],
        ['AKAP7','DNM1'],
        ['AKT3','HMGB1'],
        ['AL021408.1','AL133346.1'],
        ['AL022315.1','CDC42EP1'],
        ['AL031587.4','AL031587.6'],
        ['AL031587.6','GATC'],
        ['AL031714.1','GNAQ'],
        ['AL035409.1','ST6GALNAC5'],
        ['AL035681.1','CHADL'],
        ['AL049698.1','KIF25-AS1'],
        ['AL049838.1','C14ORF37'],
        ['AL078639.1','LINC00632'],
        ['AL109811.2','ANKRD26'],
        ['AL121894.1','CST3'],
        ['AL133325.3','NKX2-2'],
        ['AL133410.1','NPR2'],
        ['AL135925.1','LINC00863'],
        ['AL136307.1','FARS2'],
        ['AL136317.2','AL591441.1'],
        ['AL136985.3','LINC01358'],
        ['AL137013.1','TERF1'],
        ['AL137186.2','SPAG9'],
        ['AL137230.1','EFCAB11'],
        ['AL139287.1','FOXP1'],
        ['AL139353.1','BBS5'],
        ['AL158151.1','PTPA'],
        ['AL158151.3','PTPA'],
        ['AL160272.1','TLR4'],
        ['AL160290.2','BUB3'],
        ['AL161457.2','KIR3DX1'],
        ['AL353803.1','UBA52'],
        ['AL354813.1','SIAE'],
        ['AL355922.1','RNASE2'],
        ['AL355994.2','FAM131C'],
        ['AL356599.1','COX6C'],
        ['AL358334.2','AL589765.4'],
        ['AL359233.1','AL392023.2'],
        ['AL359643.2','LYRM4'],
        ['AL359915.2','IGH@'],
        ['AL365277.1','ZNF655'],
        ['AL390726.5','CYP4F26P'],
        ['AL390728.4','ZNF720'],
        ['AL451070.1','FABP3'],
        ['AL590132.1','IPO7'],
        ['AL590426.1','SCD5'],
        ['AL590666.1','CRABP2'],
        ['AL591885.1','ZBTB18'],
        ['AL592310.1','FAM133B'],
        ['AL596220.1','C1ORF27'],
        ['AL627230.7','FAM27E3'],
        ['AL645937.4','OR2B4P'],
        ['AL662844.4','OR52A1'],
        ['AL662899.2','ANKRD54'],
        ['AL662899.2','HERC4'],
        ['AL662899.2','IGH@'],
        ['AL807752.2','AL807752.4'],
        ['AL807752.7','MBP'],
        ['ALDOC','GFAP'],
        ['ALG1','TSSC2'],
        ['ALG9','AP001781.2'],
        ['ALK','MAPKBP1'],
        ['ALK','ZNF587'],
        ['AMER2','MBP'],
        ['ANAPC10','HHIP-AS1'],
        ['ANAPC16','IL3RA'],
        ['ANKRD10-IT1','NSD2'],
        ['ANKRD18B','ANKRD19P'],
        ['AOAH','ELMO1'],
        ['AP000317.1','LINC00310'],
        ['AP000346.2','IGLL3P'],
        ['AP000688.2','CBR3'],
        ['AP001029.1','AP001029.2'],
        ['AP001626.1','MUM1'],
        ['AP002026.1','KCNK2'],
        ['AP002812.2','RSF1'],
        ['AP002852.2','ODF1'],
        ['AP003393.1','USP2-AS1'],
        ['AP005117.1','KIAA0895L'],
        ['AP005901.3','LINC01632'],
        ['AP006222.1','RPL23AP53'],
        ['AP1M2','CDKN2D'],
        ['APBA2','BASP1'],
        ['APBA2','GOLGA8A'],
        ['APBB1','HPX'],
        ['APBB1','OGDHL'],
        ['APEH','RNF123'],
        ['APPBP2','PTPRZ1'],
        ['APPL2','NABP2'],
        ['ARF4-AS1','DENND6A-AS1'],
        ['ARHGAP26','S1PR3'],
        ['ARHGAP26','ZNF124'],
        ['ARHGEF26-AS1','LINC02006'],
        ['ARL10','CRLF2'],
        ['ARL17B','SAR1B'],
        ['ARL6','REPS2'],
        ['ARMC8','MRAS'],
        ['ARPC2','PRPF6'],
        ['ARSF','GYG2'],
        ['ASH1L','C4ORF47'],
        ['ASMTL-AS1','MMP17'],
        ['ASPA','IGF2R'],
        ['ASTN2','ETFA'],
        ['ATM','NCAPH2'],
        ['ATP1B1','DNAJC7'],
        ['ATP1B1','HIF1A'],
        ['ATP5B','HNRNPDL'],
        ['ATP6V1C1','AZIN1-AS1'],
        ['ATRNL1','CLK3'],
        ['ATRNL1','TTC32'],
        ['ATXN3','THAP11'],
        ['AVL9','RFC5'],
        ['B3GNT9','TRADD'],
        ['BACH2','TAPBP'],
        ['BAG1','MRPS21'],
        ['BAG5','CKB'],
        ['BANK1','QSOX2'],
        ['BASP1','CDH18'],
        ['BASP1','KLC1'],
        ['BATF3','NSL1'],
        ['BCKDK','KAT8'],
        ['BCL11A','C17ORF75'],
        ['BCL11A','VPS53'],
        ['BCL2','SNX27'],
        ['BCO2','ZFP62'],
        ['BICDL2','HCFC1R1'],
        ['BIN1','C11ORF70'],
        ['BIN3','EGR3'],
        ['BMP3','C4ORF22'],
        ['BMP7','MYH3'],
        ['BRCA1','VAT1'],
        ['BRD4','DNAJC24'],
        ['BRD9','TPPP'],
        ['BX119927.1','BX276092.7'],
        ['BX571846.1','F8'],
        ['BX890604.1','FAM239A'],
        ['BZW1','TCEANC2'],
        ['C10ORF90','DAD1'],
        ['C11ORF45','KCNJ1'],
        ['C12ORF60','PDE6H'],
        ['C14ORF93','PSMB5'],
        ['C15ORF61','MAP2K5'],
        ['C19MC','SERINC3'],
        ['C19ORF25','FXR2'],
        ['C1ORF21','SFPQ'],
        ['C20ORF96','NRSN2-AS1'],
        ['C2CD5','ITPR1'],
        ['C2ORF74','FER'],
        ['C3ORF58','STAMBPL1'],
        ['C4ORF50','CRMP1'],
        ['C7ORF50','ZFAND2A'],
        ['C8ORF44','ZFR'],
        ['CABP1','CDC42BPB'],
        ['CABP1','DOPEY2'],
        ['CABP1','SEC13'],
        ['CABP1','SPIRE2'],
        ['CACNA1A','TAF13'],
        ['CACNB2','G3BP2'],
        ['CACNB2','NSUN6'],
        ['CACNG8','PREPL'],
        ['CACNG8','UQCRB'],
        ['CALCOCO1','GPR61'],
        ['CALM1','TTC7B'],
        ['CALM2','FKBP8'],
        ['CALM2','GNAI3'],
        ['CALM3','MBP'],
        ['CALM3','RAP2A'],
        ['CALY','OS9'],
        ['CAMK1','CPNE9'],
        ['CAMK2A','MBP'],
        ['CAMK2N1','CRHR1-IT1_'],
        ['CAMK2N1','MIR100HG'],
        ['CAMKK1','CENPV'],
        ['CAPN1','SHD'],
        ['CASD1','EIF3E'],
        ['CASKIN1','CST3'],
        ['CCDC125','EIF3G'],
        ['CCDC130','ZNF14'],
        ['CCDC77','DAP3'],
        ['CCDC84','MAP4'],
        ['CCDC88B','PRDX5'],
        ['CCM2L','XKR7'],
        ['CCNB1','SLC30A5'],
        ['CCT6P1','INTS4'],
        ['CD247','CREG1'],
        ['CD96','NECTIN3'],
        ['CD99','ESYT2'],
        ['CDC6','WIPF2'],
        ['CDH3','ZFP90'],
        ['CDIP1','PLP2'],
        ['CDK5R1','PSMD11'],
        ['CELF2','CMC2'],
        ['CELF6','PARP6'],
        ['CEP97','TRPM7'],
        ['CERCAM','TCF4'],
        ['CES4A','POMGNT1'],
        ['CHCHD1','ZSWIM8'],
        ['CHCHD10','TRG@'],
        ['CHD3','CYB5D1'],
        ['CHD4','INO80E'],
        ['CHD5','NTRK2'],
        ['CHI3L1','IFI35'],
        ['CHST5','TMEM231'],
        ['CHST6','TMEM170A'],
        ['CKB','FAM131B'],
        ['CKB','MBP'],
        ['CLASP2','FAM104A'],
        ['CLASP2','HACE1'],
        ['CLIC2','TMLHE-AS1'],
        ['CLN8','KBTBD11'],
        ['CLPX','NUDT15'],
        ['CLU','GNAS'],
        ['CMC2','RALYL'],
        ['CMSS1','EEF1D'],
        ['CNTN1','PPHLN1'],
        ['COA4','MRPL48'],
        ['COPRS','UTP6'],
        ['COPS2','NPIPB5'],
        ['COPS5','SCAF1'],
        ['COX6A2','ZNF843'],
        ['CPB1','TRAF3IP2-AS1'],
        ['CPSF6','SRSF11'],
        ['CPSF6','ZNF3'],
        ['CRLF2','ELMOD1'],
        ['CRLF2','PMS2CL'],
        ['CRLF2','SIK2'],
        ['CRLF2','TADA2A'],
        ['CRLF3','TEFM'],
        ['CROCC','RNF123'],
        ['CRTC1','PFDN5'],
        ['CRYBB2','IGK@'],
        ['CRYZL1','GOSR1'],
        ['CSF2RA','GNPTG'],
        ['CSF2RA','PNMA2'],
        ['CSNK1E','Z98749.2'],
        ['CTBP2','NEAT1'],
        ['CTDSPL','GEMIN4'],
        ['CTIF','MBP'],
        ['CTSA','KLHDC4'],
        ['CTU2','SNAI3-AS1'],
        ['CWC27','NDUFS4'],
        ['CYB561D2','CYB561D2'],
        ['CYB5R3','HSD17B12'],
        ['CYP4F26P','FAM95C'],
        ['DAZAP1','SUN1'],
        ['DBNDD2','TP53TG5'],
        ['DCAF16','USF3'],
        ['DENND4A','RBX1'],
        ['DENND5B','LINC02387'],
        ['DERL1','MAP2K1'],
        ['DHRS4L1','DHRS4L2'],
        ['DIAPH1','HDAC3'],
        ['DIP2C','NCAM1'],
        ['DLGAP1','PPM1A'],
        ['DOPEY2','GTF2IRD2'],
        ['DPAGT1','H2AFX'],
        ['DPP9','MYDGF'],
        ['DRD5','IGK@'],
        ['DSEL','EFCAB11'],
        ['DST','MBP'],
        ['DSTN','VAPB'],
        ['DSTN','XKR4'],
        ['DSTYK','IGK@'],
        ['DUSP6','POC1B'],
        ['DUX4','LINC02193'],
        ['DYNLL2','SRSF7'],
        ['EFCAB14','NMNAT1'],
        ['EIF4A2','KAZN'],
        ['EIF4E','NOL6'],
        ['ELF2','SF3B1'],
        ['EML4','REX1BD'],
        ['EML4','SFXN1'],
        ['ENO2','PKD1'],
        ['EPM2A','ZDHHC22'],
        ['ERAS','HDAC6'],
        ['ERCC6','TMEM232'],
        ['ERI3','MYO6'],
        ['EXOSC10','TRIM37'],
        ['EXOSC9','PP12613'],
        ['F3','FLYWCH1'],
        ['FADS6','TBL1XR1'],
        ['FAM107A','MBP'],
        ['FAM120B','JKAMP'],
        ['FAM129A','SLC25A16'],
        ['FAM159A','GPX7'],
        ['FAM177A1','ZNF500'],
        ['FAM49A','VSNL1'],
        ['FAM53C','NRF1'],
        ['FAM66A','FAM66D'],
        ['FAM66C','LINC02449'],
        ['FAM83D','PPP1R16B'],
        ['FAM86B3P','FAM86DP'],
        ['FAM86B3P','FAM90A1'],
        ['FAM86C1','FAM86C2P'],
        ['FAM86JP','FAM86LP'],
        ['FARP2','HDLBP'],
        ['FAT1','MTNR1A'],
        ['FBXO25','LINC01881'],
        ['FBXW7','GATB'],
        ['FBXW7','MYCBP2'],
        ['FCGRT','PTGDS'],
        ['FECH','GHITM'],
        ['FEM1A','FP475955.4'],
        ['FGF12','MB21D2'],
        ['FGFR2','GTPBP6'],
        ['FO681548.1','TERF2IP'],
        ['FOXRED2','KIAA0513'],
        ['FRG1','FRG1DP'],
        ['FRG1DP','FRG1HP'],
        ['FRRS1L','IL3RA'],
        ['FRRS1L','ZNF891'],
        ['FTCD','SPATC1L'],
        ['GABBR2','GPCPD1'],
        ['GABRG3','OCA2'],
        ['GALK2','NPIPB5'],
        ['GALNT9','NOC4L'],
        ['GAR1','RRH'],
        ['GAS5','SMYD4'],
        ['GATD1','LINC00887'],
        ['GATD1','PTCD1'],
        ['GATD1','ST8SIA5'],
        ['GATD1','WWOX'],
        ['GATS','MRPL52'],
        ['GATS','PILRB'],
        ['GBP4','ZHX3'],
        ['GFAP','GNAS'],
        ['GFAP','SNAP25'],
        ['GFAP','VGLL4'],
        ['GHDC','HCRT'],
        ['GIMAP2','MX1'],
        ['GLG1','LINC00320'],
        ['GLRA2','VSNL1'],
        ['GLS','PEX14'],
        ['GNL2','PPFIBP1'],
        ['GOLGA4','MRAS'],
        ['GPI','SSTR5-AS1'],
        ['GPR155','MIR100HG'],
        ['GPSM2','LINC02551'],
        ['GRIN1','TMEM161B-AS1'],
        ['GRK4','SARAF'],
        ['GRM3','TRB@'],
        ['GTF2H3','TCTN2'],
        ['GUSBP11','SPECC1L'],
        ['GVINP1','PRDX6'],
        ['H3F3A','HIST1H3PS1'],
        ['HACD2','SCD5'],
        ['HAPLN2','NAXE'],
        ['HBS1L','KIF13A'],
        ['HCG17','TRIM26'],
        ['HDAC10','PFKL'],
        ['HDHD5-AS1','STK39'],
        ['HERC4','LIN52'],
        ['HIP1R','PTGDS'],
        ['HKR1','LINC01535'],
        ['HKR1','PAK1'],
        ['HMGB1','NCAM1'],
        ['HNRNPH1','Z98749.2'],
        ['HNRNPUL1','SPTBN4'],
        ['HOOK2','TAX1BP1'],
        ['HPRT1','LINC00629'],
        ['HPX','TRIM3'],
        ['HSD17B1','NAGLU'],
        ['HSD17B12','TRA@'],
        ['HSD17B14','LCN12'],
        ['HSDL2','KIAA1958'],
        ['HTT','UCHL1'],
        ['ICOSLG','SLC25A3'],
        ['ICOSLG','SP4'],
        ['IFI6','LINC02574'],
        ['IGF2BP1','STAC2'],
        ['IGK@','MORN3'],
        ['IGK@','SRGAP2B'],
        ['IGSF22','PTPN5'],
        ['IK','SLC4A10'],
        ['IL32','MMP25'],
        ['IL3RA','WSB1'],
        ['ILF3-AS1','MOG'],
        ['ING5','ME2'],
        ['INTS6','OIP5-AS1'],
        ['IPO5','SPIDR'],
        ['IPP','TMEM69'],
        ['IRAK1','MECP2'],
        ['IRGQ','XRCC1'],
        ['ISCU','SF1'],
        ['ITM2B','SH3D19'],
        ['ITPR1-AS1','SUMF1'],
        ['JADE1','ST8SIA5'],
        ['JAKMIP3','NOC4L'],
        ['JDP2','OIP5-AS1'],
        ['JMJD7-PLA2G4B','MAN2C1'],
        ['KALRN','UMPS'],
        ['KATNA1','LATS1'],
        ['KCNK15-AS1','LINC01260'],
        ['KCTD21-AS1','USP35'],
        ['KDELC1','TEX30'],
        ['KIF3A','MORN4'],
        ['KIF5A','PRKCB'],
        ['KIF5A','R3HDM2'],
        ['KIFC2','RPS16'],
        ['KLF7','MBP'],
        ['KLHDC2','RWDD3'],
        ['KYNU','PIK3R1'],
        ['LAMA4','REPS2'],
        ['LAMTOR5-AS1','QDPR'],
        ['LANCL1','SYCP2'],
        ['LANCL3','XK'],
        ['LGI1','TERF2'],
        ['LHFPL5','SLITRK2'],
        ['LIMD1','SSH2'],
        ['LINC00320','SRP19'],
        ['LINC00499','LINC00500'],
        ['LINC00649','VSNL1'],
        ['LINC00893','LINC00894'],
        ['LINC00963','MAPKBP1'],
        ['LINC01036','LINC01037'],
        ['LINC01176','ZNRF2'],
        ['LINC01184','PCYOX1L'],
        ['LINC01250','TAF1D'],
        ['LINC01632','RFC5'],
        ['LINC01719','PDE4DIP'],
        ['LINC02044','NEPRO'],
        ['LINC02389','TBC1D30'],
        ['LINC02473','SOD3'],
        ['LINC02526','QRSL1'],
        ['LRRC40','NCBP1'],
        ['LRRC47','MALT1'],
        ['LRRFIP2','RALYL'],
        ['LRRFIP2','SNRPG'],
        ['LYPLAL1','PTPRZ1'],
        ['LYZ','YWHAZ'],
        ['MAGI2','PSMB1'],
        ['MAL2','SAMD12'],
        ['MAP2K4','MOBP'],
        ['MAP4K2','METTL6'],
        ['MAPK12','TTC19'],
        ['MAPKBP1','S100PBP'],
        ['MATR3','MDH1'],
        ['MBP','MTURN'],
        ['MBP','PHLDB1'],
        ['MBP','PLP1'],
        ['MBP','PPP4R1'],
        ['MBP','PTPN2'],
        ['MBP','RAB40B'],
        ['MBP','RBFOX3'],
        ['MBP','SS18'],
        ['MDM4','RAB11FIP4'],
        ['MED12','SATB1'],
        ['MEG3','SCOC'],
        ['MEGF8','NFIX'],
        ['METTL6','SH3BP5'],
        ['MFSD14A','WDR7'],
        ['MFSD14C','ZNF782'],
        ['MIR100HG','SLC4A8'],
        ['MIR100HG','SNX27'],
        ['MORF4L2-AS1','TMEM31'],
        ['MOV10L1','PANX2'],
        ['MOV10L1','RPAP2'],
        ['MPPED1','VPS13D'],
        ['MRPL30','RNF10'],
        ['MRPL58','RAB37'],
        ['MSL2','TTLL7'],
        ['MSX1','STX18-AS1'],
        ['MT1E','MT1M'],
        ['MTFR1','YTHDF3'],
        ['MTURN','N4BP1'],
        ['MXD1','SLC11A2'],
        ['MYO5A','SETDB2'],
        ['NAA60','ZNF174'],
        ['NALCN','PCCA'],
        ['NAPSA','NAPSB'],
        ['NCALD','UBR5'],
        ['NCSTN','NHLH1'],
        ['NDRG3','NR6A1'],
        ['NDUFB2','SRSF12'],
        ['NDUFS1','TRA@'],
        ['NDUFV3','SLC7A10'],
        ['NEDD4L','TCF4'],
        ['NEFM','THY1'],
        ['NEK4','TAF1D'],
        ['NEU3','ZNF667-AS1'],
        ['NOC4L','TTYH3'],
        ['NOL10','NUPL2'],
        ['NQO2','TAF1'],
        ['NR2C1','ZNF470'],
        ['NUTM2A','NUTM2B'],
        ['OIP5-AS1','PAFAH1B2'],
        ['OSBPL3','PPFIA2'],
        ['PACS2','SOGA1'],
        ['PAIP2','Z82186.1'],
        ['PARP6','PKM'],
        ['PBX1','YWHAZ'],
        ['PDLIM1','SORBS1'],
        ['PDZK1','RNF115'],
        ['PEAK1','TSPAN3'],
        ['PHACTR3','RHOJ'],
        ['PHACTR4','RFC5'],
        ['PHYHIPL','ZMIZ1-AS1'],
        ['PICK1','POLR2F'],
        ['PIGT','WFDC2'],
        ['PINX1','XKR6'],
        ['PLP1','TF'],
        ['PLXNB3','TMEM144'],
        ['PNKD','SLC11A1'],
        ['POR','RHBDD2'],
        ['PPCDC','SCAMP5'],
        ['PPFIBP2','ZNF544'],
        ['PPM1K','XPNPEP3'],
        ['PPP1R14C','TENM2'],
        ['PPP2R5A','VPS72'],
        ['PREX2','SEC62'],
        ['PRKACB','SLC22A3'],
        ['PRKCSH','SFXN5'],
        ['PROCA1','SDF2'],
        ['PSD3','ZBTB1'],
        ['PSEN1','RBM25'],
        ['PTCD2','TANGO2'],
        ['PTGR2','RNF157'],
        ['PTP4A2','SYT2'],
        ['PTPN14','TNFRSF25'],
        ['PTPRF','USP11'],
        ['PTPRG','SKI'],
        ['PTPRN2','USP11'],
        ['PTPRN2','VAT1L'],
        ['R3HCC1L','TBPL2'],
        ['RAD9A','SWAP70'],
        ['RAP1GAP','USP48'],
        ['RAP1GDS1','SPATA18'],
        ['RBBP5','TSNAX'],
        ['RC3H2','RTN1'],
        ['RIN3','SLC24A4'],
        ['RNF141','WSB1'],
        ['RNF165','SEPT3'],
        ['RNF19A','SCPEP1'],
        ['RTN1','SYT16'],
        ['RUSC2','SRGAP3'],
        ['SATB2','SFPQ'],
        ['SBNO2','SHC2'],
        ['SCHLAP1','UBE2E3'],
        ['SDHA','TMCC1-AS1'],
        ['SENP6','TAF13'],
        ['SENP7','USP32'],
        ['SERINC3','TMEM130'],
        ['SF3B1','WWOX'],
        ['SFPQ','TRIM59'],
        ['SFPQ','USP15'],
        ['SH2B1','ZNF320'],
        ['SLC12A6','ZNF347'],
        ['SLC20A2','TOLLIP'],
        ['SLC25A18','TTPA'],
        ['SLC25A23','SPIRE2'],
        ['SLC25A43','SLC25A5'],
        ['SLC9B1','UBE2D3'],
        ['SMAD2','TRIM2'],
        ['SMIM17','ZNF71'],
        ['SNX9','ZDHHC14'],
        ['SOGA3','TRAPPC9'],
        ['SORBS1','SRI'],
        ['SPRN','SYCE1'],
        ['SPTBN4','TRPM2'],
        ['SRPRB','TF'],
        ['SSH2','TANGO2'],
        ['STIM2','ZNF251'],
        ['SYNE1','ZNF605'],
        ['SYT1','TCTE1'],
        ['TADA2A','WWOX'],
        ['TANGO2','ZNF251'],
        ['TANGO2','ZNF641'],
        ['TEX21P','ZBTB25'],
        ['THOC7','TRIM33'],
        ['TMEM130','ZNF843'],
        ['TMEM191A','TMEM191C'],
        ['TMOD1','TXNL4A'],
        ['TPPP','ZDHHC11B'],
        ['TRA@','UBE2V2'],
        ['TRA@','ZNF273'],
        ['TRA@','ZNF506'],
        ['TRIM62','WDTC1'],
        ['TRMT10B','WSB1'],
        ['TTC3','TUBE1'],
        ['VAT1L','WWOX'],
        ['ZC3H11A','ZMYND11'],
        ['ZFYVE9','ZNF714'],
        ['ZNF382','ZNF529-AS1'],
        ['ZNF439','ZNF700'],
        ['ZNF493','ZNF788']
]



    data = fusions.get(options.organism.lower(),[])
    if data:

        #file_symbols = os.path.join(options.output_directory,'genes_symbols.txt')
        file_symbols = os.path.join(options.output_directory,'synonyms.txt')
        loci = symbols.generate_loci(file_symbols)

        genes = symbols.read_genes_symbols(file_symbols)

        d = []
        for (g1,g2) in data:
            if g1.upper() != g2.upper():
                ens1 = symbols.ensembl(g1.upper(),genes,loci)
                ens2 = symbols.ensembl(g2.upper(),genes,loci)
                if ens1 and ens2:
                    for e1 in ens1:
                        for e2 in ens2:
                            if e1 != e2:
                                d.append([e1,e2])

        data = ['\t'.join(sorted(line)) + '\n' for line in d]
        data = list(set(data))

        print "%d known fusion genes found in manually currated database" % (len(data),)

        if not options.skip_filter_overlap:
            d1 = []
            overlappings = ['ensembl_fully_overlapping_genes.txt',
                            'ensembl_same_strand_overlapping_genes.txt',
                            'refseq_fully_overlapping_genes.txt',
                            'refseq_same_strand_overlapping_genes.txt',
#                            'ucsc_fully_overlapping_genes.txt',
#                            'ucsc_same_strand_overlapping_genes.txt',
                            'pairs_pseudogenes.txt',
                            'paralogs.txt']
            for ov in overlappings:
                p = os.path.join(options.output_directory,ov)
                print "Parsing file:",p
                if os.path.isfile(p):
                    d2 = sorted(set([tuple(sorted(line.rstrip('\r\n').split('\t'))) for line in file(p,'r').readlines() if line.rstrip('\r\n')]))
                d1.extend(d2)
            d = set()
            for line in d1:
                (a,b) = (line[0],line[1])
                if a > b:
                    (a,b) = (b,a)
                d.add("%s\t%s\n" % (a,b))
            skipped = [line for line in data if line in d]
            data = [line for line in data if not line in d]
            file(os.path.join(options.output_directory,'cortex_known_but_overlapping.txt'),'w').writelines(sorted(skipped))

            print "%d known fusion genes left after removing the overlappings" % (len(data),)

    file(os.path.join(options.output_directory,'cortex.txt'),'w').writelines(sorted(data))
    #
