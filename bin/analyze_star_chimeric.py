#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It takes as input a PSL formated file generated which has been converted from
SAM file (that is Chimeric.out.sam by sam2psl.py) generated by STAR aligner.
Here the assumption is that the consecutive lines which has the same read id
can me merge safely into one mapping.



Author: Daniel Nicorici, Daniel.Nicorici@gmail.com

Copyright (c) 2009-2021 Daniel Nicorici

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


# info PSL
"""
========================================================
More about PSL format is here: http://genome.ucsc.edu/FAQ/FAQformat#format2


PSL format

PSL lines represent alignments, and are typically taken from files generated
by BLAT or psLayout. See the BLAT documentation for more details. All of the
following fields are required on each data line within a PSL file:

   1. matches - Number of bases that match that aren't repeats
   2. misMatches - Number of bases that don't match
   3. repMatches - Number of bases that match but are part of repeats
   4. nCount - Number of 'N' bases
   5. qNumInsert - Number of inserts in query
   6. qBaseInsert - Number of bases inserted in query
   7. tNumInsert - Number of inserts in target
   8. tBaseInsert - Number of bases inserted in target
   9. strand - '+' or '-' for query strand. For translated alignments, second '+'or '-' is for genomic strand
  10. qName - Query sequence name
  11. qSize - Query sequence size
  12. qStart - Alignment start position in query
  13. qEnd - Alignment end position in query
  14. tName - Target sequence name
  15. tSize - Target sequence size
  16. tStart - Alignment start position in target
  17. tEnd - Alignment end position in target
  18. blockCount - Number of blocks in the alignment (a block contains no gaps)
  19. blockSizes - Comma-separated list of sizes of each block
  20. qStarts - Comma-separated list of starting positions of each block in query
  21. tStarts - Comma-separated list of starting positions of each block in target

Example:
Here is an example of an annotation track in PSL format. Note that line breaks have been inserted into the PSL lines in this example for documentation display purposes. Click here for a copy of this example that can be pasted into the browser without editing.

track name=fishBlats description="Fish BLAT" useScore=1
59 9 0 0 1 823 1 96 +- FS_CONTIG_48080_1 1955 171 1062 chr22
    47748585 13073589 13073753 2 48,20,  171,1042,  34674832,34674976,
59 7 0 0 1 55 1 55 +- FS_CONTIG_26780_1 2825 2456 2577 chr22
    47748585 13073626 13073747 2 21,45,  2456,2532,  34674838,34674914,
59 7 0 0 1 55 1 55 -+ FS_CONTIG_26780_1 2825 2455 2676 chr22
    47748585 13073727 13073848 2 45,21,  249,349,  13073727,13073827,

Be aware that the coordinates for a negative strand in a PSL line are handled in a special way. In the qStart and qEnd fields, the coordinates indicate the position where the query matches from the point of view of the forward strand, even when the match is on the reverse strand. However, in the qStarts list, the coordinates are reversed.

Example:
Here is a 30-mer containing 2 blocks that align on the minus strand and 2 blocks that align on the plus strand (this sometimes can happen in response to assembly errors):

0         1         2         3 tens position in query
0123456789012345678901234567890 ones position in query
            ++++          +++++ plus strand alignment on query
    --------    ----------      minus strand alignment on query

Plus strand:
     qStart=12
     qEnd=31
     blockSizes=4,5
     qStarts=12,26

Minus strand:
     qStart=4
     qEnd=26
     blockSizes=10,8
     qStarts=5,19

Essentially, the minus strand blockSizes and qStarts are what you would get if you reverse-complemented the query. However, the qStart and qEnd are not reversed. To convert one to the other:

     qStart = qSize - revQEnd
     qEnd = qSize - revQStart
"""


"""
Example of "Chimeric.out.sam"


000B1-2	0	ENSG00000115053|ENSG00000084234|30111	22878	3	35M55S	*	0	0	AAGAGGATGATGAGGACGAGGATGACGACGACGACGAAGACAGTGATGAAGAGGAGGATGATGACAGTGAGGAGGATGAGGAGGATGACG	^_acceeeggggfiiiiiihiiihiiihiihihhiiigeeeee]abccbbbbac`_c_`bbbbcc]bY_bbc`ac^R]]`bbca[]YYS[	NH:i:2	HI:i:1	AS:i:46	nM:i:8
000B1-2	256	ENSG00000115053|ENSG00000084234|30111	21916	3	35S55M	*	0	0	AAGAGGATGATGAGGACGAGGATGACGACGACGACGAAGACAGTGATGAAGAGGAGGATGATGACAGTGAGGAGGATGAGGAGGATGACG	^_acceeeggggfiiiiiihiiihiiihiihihhiiigeeeee]abccbbbbac`_c_`bbbbcc]bY_bbc`ac^R]]`bbca[]YYS[	NH:i:2	HI:i:2	AS:i:54	nM:i:0

00IUU-2	16	ENSG00000066468|ENSG00000080824|120125	176254	3	52S32M6S	*	0	0	TCACAGGTGAGACCAAGGACCAGGTAGCTAACTCAGCCTTTGTGGAACGTCTCCAGAAACATATCTATTATATCACAGGTGAGACCAAGG	`_`baeeeegfggggiiiifiiiiiihihhfhfdcfffffihihhgchiihhhiihihhhhfghhhdifidaeeahhggggeeeeeeb__	NH:i:2	HI:i:1	AS:i:29	nM:i:1
00IUU-2	272	ENSG00000066468|ENSG00000080824|120125	176520	3	3S49M38S	*	0	0	TCACAGGTGAGACCAAGGACCAGGTAGCTAACTCAGCCTTTGTGGAACGTCTCCAGAAACATATCTATTATATCACAGGTGAGACCAAGG	`_`baeeeegfggggiiiifiiiiiihihhfhfdcfffffihihhgchiihhhiihihhhhfghhhdifidaeeahhggggeeeeeeb__	NH:i:2	HI:i:2	AS:i:54	nM:i:2

00Q6O-1	0	ENSG00000168036|ENSG00000167978|65260	4810	3	25M65S	*	0	0	GGCGGGAGGAGCCTGTTCCCCTGAGCAGCTGGAGTCCAGAAATGATTTTTTCGATGAATTTAGGATTTTGCCGCAGTATACATCTGCAGT	bbbeeeeeggeggffhfhiihiihiiiiihii`d_ehfgfiiiiigggggebc`dcccddccccbcccccbbaca]abccccdccccccc	NH:i:2	HI:i:1	AS:i:25	nM:i:2
00Q6O-1	256	ENSG00000168036|ENSG00000167978|65260	792	3	25S65M	*	0	0	GGCGGGAGGAGCCTGTTCCCCTGAGCAGCTGGAGTCCAGAAATGATTTTTTCGATGAATTTAGGATTTTGCCGCAGTATACATCTGCAGT	bbbeeeeeggeggffhfhiihiihiiiiihii`d_ehfgfiiiiigggggebc`dcccddccccbcccccbbaca]abccccdccccccc	NH:i:2	HI:i:2	AS:i:65	nM:i:0

00R5E-2	0	ENSG00000075624|ENSG00000182472|36634	36522	3	24M66S	*	0	0	CCCAACTTGAGATGTATGAAGGCTGGTGATAGCATTGCTTTCGTGTAAATTATGTAATGCAAAATTTTTTTAATCTTCGCCTTAATACTT	bbbeeeeegegggigfhhdeghiiiifghiiihhhhihhiihhfgggiiifhhihfggiiiihhiiiidhgeeeeeeecccccbccbccc	NH:i:2	HI:i:1	AS:i:23	nM:i:0
00R5E-2	256	ENSG00000075624|ENSG00000182472|36634	36395	3	24S66M	*	0	0	CCCAACTTGAGATGTATGAAGGCTGGTGATAGCATTGCTTTCGTGTAAATTATGTAATGCAAAATTTTTTTAATCTTCGCCTTAATACTT	bbbeeeeegegggigfhhdeghiiiifghiiihhhhihhiihhfgggiiifhhihfggiiiihhiiiidhgeeeeeeecccccbccbccc	NH:i:2	HI:i:2	AS:i:64	nM:i:0



The same converted to PSL (by sam2psl.py):

27	63	0	0	0	0	0	0	+	000B1-2	90	0	35	ENSG00000115053|ENSG00000084234|30111	105086	22877	22912	1	35,	0,	22877,
55	35	0	0	0	0	0	0	+	000B1-2	90	35	90	ENSG00000115053|ENSG00000084234|30111	105086	21915	21970	1	55,	35,	21915,

31	59	0	0	0	0	0	0	-	00IUU-2	90	52	84	ENSG00000066468|ENSG00000080824|120125	179087	176253	176285	1	32,	52,	176253,
47	43	0	0	0	0	0	0	-	00IUU-2	90	3	52	ENSG00000066468|ENSG00000080824|120125	179087	176519	176568	1	49,	3,	176519,

23	67	0	0	0	0	0	0	+	00Q6O-1	90	0	25	ENSG00000168036|ENSG00000167978|65260	85470	4809	4834	1	25,	0,	4809,
65	25	0	0	0	0	0	0	+	00Q6O-1	90	25	90	ENSG00000168036|ENSG00000167978|65260	85470	791	856	1	65,	25,	791,

24	66	0	0	0	0	0	0	+	00R5E-2	90	0	24	ENSG00000075624|ENSG00000182472|36634	76352	36521	36545	1	24,	0,	36521,
66	24	0	0	0	0	0	0	+	00R5E-2	90	24	90	ENSG00000075624|ENSG00000182472|36634	76352	36394	36460	1	66,	24,	36394,



The same thing from the Chimaric.out.junction:


ENSG00000115053|ENSG00000084234|30111	22913	+	ENSG00000115053|ENSG00000084234|30111	21915	+	0	0	5	000B1-2	22878	35M55S	21916	35S55M
ENSG00000066468|ENSG00000080824|120125	176253	-	ENSG00000066468|ENSG00000080824|120125	176569	-	0	0	0	00IUU-2	176254	52S32M6S	176520	3S49M38S

ENSG00000168036|ENSG00000167978|65260	4835	+	ENSG00000168036|ENSG00000167978|65260	791	+	1	2	0	00Q6O-1	4810	25M65S	792	25S65M
ENSG00000075624|ENSG00000182472|36634	36546	+	ENSG00000075624|ENSG00000182472|36634	36394	+	0	0	0	00R5E-2	36522	24M66S	36395	24S66M

ENSG00000168036|ENSG00000167978|65260	4744	+	ENSG00000168036|ENSG00000167978|65260	4677	+	0	0	6	00WK1-2	4720	24M66S	4678	24S66M
ENSG00000168036|ENSG00000167978|65260	45485	+	ENSG00000168036|ENSG00000167978|65260	45355	+	0	0	0	00X03-1	45449	36M54S	45356	36S54M

ENSG00000187514|ENSG00000131771|6647	16224	-	ENSG00000187514|ENSG00000131771|6647	16275	-	0	0	2	011RU-1	16225	66S24M	16209	66M24S
ENSG00000075624|ENSG00000182472|36634	36538	+	ENSG00000075624|ENSG00000182472|36634	36330	+	0	0	1	01GCZ-2	36513	25M65S	36331	25S65M


The expected output of this program would be this PSL file for the above example:

27	63	0	0	0	0	0	0	+	000B1-2	90	0	35	ENSG00000115053|ENSG00000084234|30111	105086	22877	22912	1	35,	0,	22877,
55	35	0	0	0	0	0	0	+	000B1-2	90	35	90	ENSG00000115053|ENSG00000084234|30111	105086	21915	21970	1	55,	35,	21915,
becomes
27+55	63-55	0	0	0	0	0	0	+	000B1-2	90	0	90	ENSG00000115053|ENSG00000084234|30111	105086	22877	22912	2	35,55,	0,35,	22877,21915,

31	59	0	0	0	0	0	0	-	00IUU-2	90	52	84	ENSG00000066468|ENSG00000080824|120125	179087	176253	176285	1	32,	52,	176253,
47	43	0	0	0	0	0	0	-	00IUU-2	90	3	52	ENSG00000066468|ENSG00000080824|120125	179087	176519	176568	1	49,	3,	176519,
becomes
47+31	43-31	0	0	0	0	0	0	-	00IUU-2	90	3	84	ENSG00000066468|ENSG00000080824|120125	179087	176519	176568	2	49,32	3,52	176519,176253,

23	67	0	0	0	0	0	0	+	00Q6O-1	90	0	25	ENSG00000168036|ENSG00000167978|65260	85470	4809	4834	1	25,	0,	4809,
65	25	0	0	0	0	0	0	+	00Q6O-1	90	25	90	ENSG00000168036|ENSG00000167978|65260	85470	791	856	1	65,	25,	791,

24	66	0	0	0	0	0	0	+	00R5E-2	90	0	24	ENSG00000075624|ENSG00000182472|36634	76352	36521	36545	1	24,	0,	36521,
66	24	0	0	0	0	0	0	+	00R5E-2	90	24	90	ENSG00000075624|ENSG00000182472|36634	76352	36394	36460	1	66,	24,	36394,



"""

import os
import sys
import optparse
import gc


# PSL columns
psl_matches = 0
psl_misMatches = 1
psl_repMatches = 2
psl_nCount = 3
psl_qNumInsert = 4
psl_qBaseInsert = 5
psl_tNumInsert = 6
psl_tBaseInsert = 7
psl_strand = 8
psl_qName = 9
psl_qSize = 10
psl_qStart = 11
psl_qEnd = 12
psl_tName = 13
psl_tSize = 14
psl_tStart = 15
psl_tEnd = 16
psl_blockCount = 17
psl_blockSizes = 18
psl_qStarts = 19
psl_tStarts = 20


#########################
def lines(filename):
    # it gives chunks
    fin = None
    if filename == '-':
        fin = sys.stdin
    else:
        fin = open(filename,'r')
    while True:
        lines = fin.readlines(10**8)
        if not lines:
            break
        gc.disable()
        lines = [line.rstrip('\r\n').split('\t') for line in lines if line.rstrip('\r\n')]
        gc.enable()
        for line in lines:
            yield line
    fin.close()

#########################
def chunks(psl_file):
    # gives in a chunk the PSL files which have the same read is a QNAME
    last_qname = None
    last_tname = None
    last_strand = None
    chunk = []
    for line in lines(psl_file):
        if not chunk:
            last_qname = line[psl_qName]
            last_tname = line[psl_tName]
        if last_qname != line[psl_qName] or last_tname != line[psl_tName] or last_strand != line[psl_strand]:
            # the bin is full and now analyze it
            yield chunk
            last_qname = line[psl_qName]
            last_tname = line[psl_tName]
            last_strand = line[psl_strand]
            chunk = []
        chunk.append(line)
    if chunk:
        yield chunk

#########################
def merge_star_chimeric(psl_in, psl_ou):
    #
    psl = []
    fou = None
    if psl_ou == '-':
        fou = sys.stdout
    else:
        fou = open(psl_ou,'w')
    limit_psl = 10**5

    for box in chunks(psl_in):
        if len(box) == 2:
            if box[0][psl_strand] != box[1][psl_strand]:
                continue
            merged = None

            temp = box[0][:]

            r1_start = int(box[0][psl_qStart])
            r2_start = int(box[1][psl_qStart])
            if r1_start > r2_start:
                box = (box[1],box[0])

            r1_start = int(box[0][psl_qStart])
            r1_end = int(box[0][psl_qEnd])
            r2_start = int(box[1][psl_qStart])
            r2_end = int(box[1][psl_qEnd])

            t1_start = int(box[0][psl_tStart])
            t1_end = int(box[0][psl_tEnd])
            t2_start = int(box[1][psl_tStart])
            t2_end = int(box[1][psl_tEnd])

            if t1_start > t2_start:
                continue

            wiggle = 9
            if r1_end + wiggle > r2_start and r1_end < r2_start:
                dif = r2_start - r1_end

                # extend the first
                #box[0][psl_matches] = str(int(box[0][psl_matches]))
                #box[0][psl_misMatches] = str(int(box[0][psl_misMatches]) + dif)

                box[0][psl_qEnd] = str(int(box[0][psl_qEnd]) + dif)
                box[0][psl_tEnd] = str(int(box[0][psl_tEnd]) + dif)

                t = box[0][psl_blockSizes].split(',')
                t[-2] = str(int(t[-2]) + dif)
                box[0][psl_blockSizes] = ','.join(t)

                # recompute
                r1_start = int(box[0][psl_qStart])
                r1_end = int(box[0][psl_qEnd])

                t1_start = int(box[0][psl_tStart])
                t1_end = int(box[0][psl_tEnd])

            elif r1_end > r2_start and r1_end < r2_start + wiggle:
                dif = r2_start - r1_end

                # cut the second
                box[1][psl_matches] = str(int(box[1][psl_matches]) - dif)
                box[1][psl_misMatches] = str(int(box[1][psl_misMatches]) + dif)

                box[1][psl_qStart] = str(int(box[1][psl_qStart]) + dif)
                box[1][psl_tStart] = str(int(box[1][psl_tStart]) + dif)

                t = box[1][psl_blockSizes].split(',')
                t[0] = str(int(t[0]) - dif)
                box[1][psl_blockSizes] = ','.join(t)

                t = box[1][psl_qStarts].split(',')
                t[0] = str(int(t[0]) + dif)
                box[1][psl_qStarts] = ','.join(t)

                t = box[1][psl_tStarts].split(',')
                t[0] = str(int(t[0]) + dif)
                box[1][psl_tStarts] = ','.join(t)

                # recompute
                r2_start = int(box[1][psl_qStart])
                r2_end = int(box[1][psl_qEnd])

                t2_start = int(box[1][psl_tStart])
                t2_end = int(box[1][psl_tEnd])

            if r1_end <= r2_start and t1_end <= t2_start: #and box[0][psl_strand] == "+" :
                temp[psl_matches] = int(box[0][psl_matches]) + int(box[1][psl_matches])
                temp[psl_misMatches] = int(box[0][psl_misMatches]) - int(box[1][psl_matches])

                temp[psl_qNumInsert] = int(box[0][psl_qNumInsert]) + int(box[1][psl_qNumInsert])
                temp[psl_qBaseInsert] = int(box[0][psl_qBaseInsert]) + int(box[1][psl_qBaseInsert])
                temp[psl_tNumInsert] = int(box[0][psl_tNumInsert]) + int(box[1][psl_tNumInsert])
                temp[psl_tBaseInsert] = int(box[0][psl_tBaseInsert]) + int(box[1][psl_tBaseInsert])

                temp[psl_qStart] = r1_start
                temp[psl_qEnd] = r2_end

                temp[psl_tStart] = t1_start
                temp[psl_tEnd] = t2_end

                temp[psl_blockCount] = int(box[0][psl_blockCount]) + int(box[1][psl_blockCount])
                temp[psl_blockSizes] = box[0][psl_blockSizes] + box[1][psl_blockSizes]

                temp[psl_qStarts] = box[0][psl_qStarts] + box[1][psl_qStarts]

                temp[psl_tStarts] = box[0][psl_tStarts] + box[1][psl_tStarts]
                temp[psl_tNumInsert] = '1'

                merged = temp



            if merged:
                gc.disable()
                psl.append(map(str,merged))
                gc.enable()
                if len(psl) >= limit_psl:
                    fou.writelines(['\t'.join(line)+'\n' for line in psl])
                    psl = []
    # output PSL
    if psl:
        fou.writelines(['\t'.join(line)+'\n' for line in psl])
    #



#########################
if __name__ == '__main__':

    #command line parsing

    usage = "%prog [options]"
    description = """It takes as input a PSL formated file generated which has been converted from
SAM file (that is Chimeric.out.sam by sam2psl.py) generated by STAR aligner.
Here the assumption is that the consecutive lines which has the same read id
can me merge safely into one mapping."""
    version = "%prog 0.10 beta"

    parser = optparse.OptionParser(
        usage = usage,
        description = description,
        version = version)

    parser.add_option("--input","-i",
                      action="store",
                      type="string",
                      dest="input_filename",
                      help="""The input file in PSL format.""")

    parser.add_option("--output","-o",
                      action="store",
                      type="string",
                      dest="output_filename",
                      help="""The output PSL file containing the contigs with the best alignment which must be unique.""")

    (options,args) = parser.parse_args()

    # validate options
    if not (options.input_filename and
            options.output_filename
            ):
        parser.print_help()
        sys.exit(1)

    # running
    merge_star_chimeric(options.input_filename, options.output_filename)
#
