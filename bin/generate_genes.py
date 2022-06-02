#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It takes as input a fasta file containing a genome and genes positions on the 
genome and it gives the exon sequences as a fasta file.



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

#
"""

The format of the file contaning exonic positions is as follows, e.g. genes_positions_ensembl.txt

ensembl_gene_id
end_position
start_position
strand
chromosome_name

The output is in file: "genes_ensembl.fa" as follows:
>ENSG00000000457
GCACCTCTACTGTTTGCTACAAGTGGCCAGCAGCCATTTTGGATTTGGGCGGAAATGAAA
TTAAAACTGTGCTGTTAAAAGCCTAAAAATTCAAGTCAAGACAAACTTAAGCATTCGACC
AACACATCTAGAAAGGGGGCATCTTCGTGGACTAACTAGACCACTGGGGCAGTGAGTGAA
ACTCGGTATCGTCGCGGCGCCCACACTTAAGATGGCACCGGCCTGAGACTCAGCTGTGCG
GCCTCTCTACCTCGGTTCCTGGTTAGTTGGCCTCATTGGTGGCGTCGGAGGGAGGAAGGT
GGGCCTTCTGTCCCGTTTCCGGACCCGTCTCTATGGTGTAGGAGAAACCCGGCCCCCAGA
AGATTGTGGGTGTAGTGGCCACAGCCTTACAGGCAGGCAGGGGTGGTTGGTGTCAACAGG
GGGGCCAACAGGGTACCAGAGCCAAGACCCTCGGCCTCCTCCCCCGCCGCCTTCCTGCAG
GTAACAGGGAGCCCTGCGCTGCGCCCCCAGTCCTTGCAGGACTGCGCCGTGGGGGAAGGG
GCCGGGCGGGGAGGAGGCGGCGGGCGCGCGCCCCGCTCGCGGGTCTGCGCTCTGGGGCCC
GCGCGGGAGCGAGCTCGGCGCGGCGCCGGCGGCCGGTTGAGCTGTGCTCTCAGCTTCGGA
GCAGCCTCCCCTTGCTGATTGTGGGGCGCCCTGTAATCTGCGCTTCGCGGGCGGCCCCCG
ACGGGTGAGGCGCCCGCGGCCAGAGCTCTCCAAGGCGGCCGCGGAGTCGGTCCTCGCAGG
GAGGTGTGGAAGGTGAGGGGCCAGCGAAGCGAGAGCGGCGCCTCGGCCCTTCAGTGACCC

"""
import os
import sys
import Bio
import Bio.SeqIO
import Bio.SeqRecord
import Bio.Alphabet
import optparse

def give_seq(seq,start,end,strand,chrom_len):
    if start > end:
        (start,end) = (end,start)
    s = ""
    if strand == '1' or strand == '+1' or strand == '+':
        s = seq[start-1:end]
    else:
        s = seq[start-1:end].reverse_complement()
    if end > chrom_len:
        s = s + "N"*(chrom_len-end)
    return s

def get_cols(t):
    return (t[4],t[0],int(t[2]),int(t[1]),t[3]) # chromosome, gene_id, gene_start, gene_end, gene_strand


if __name__ == '__main__':

    #command line parsing

    usage = "%prog [options]"
    description = """It takes as input a fasta file containing a genome and genes positions on the genome and it gives the exon sequences as a fasta file."""
    version = "%prog 0.10 beta"

    parser = optparse.OptionParser(usage=usage,description=description,version=version)

    parser.add_option("--input_genes",
                      action="store",
                      type="string",
                      dest="input_genes_positions",
                      help="""Input file with genes positions.""")

    parser.add_option("--input_genome",
                      action="store",
                      type="string",
                      dest="input_genome_fasta",
                      help="""Input FASTA genome containing the genome sequences.""")


    parser.add_option("--output",
                      action="store",
                      type="string",
                      dest="output_directory",
                      default = '.',
                      help="""The output directory where the genes sequences are written. Default is '%default'.""")


    (options,args) = parser.parse_args()

    # validate options
    if not (options.input_genes_positions and 
            options.input_genome_fasta and 
            options.output_directory
            ):
        parser.print_help()
        parser.error("Missing argument(s)!")
        sys.exit(1)


    #
    #
    #

    data = set([get_cols(line.rstrip('\r\n').split('\t')) for line in file(options.input_genes_positions,'r').readlines() if line.rstrip('\r\n')])
    dc = dict()
    for line in data:
        if line[0] not in dc:
            dc[line[0]] = []
        dc[line[0]].append(line[1:])




    genes = []
    output_handle = open(os.path.join(options.output_directory,'genes.fa'), "w")
    chrome = []
    for record in Bio.SeqIO.parse(open(options.input_genome_fasta, "rU"), "fasta") :
        reid = record.id
        lerese = len(record.seq)
        print '  * chromosome %s has length %d' % (reid, lerese)
        chrome.append("%s\t%s\n" % (reid,str(lerese)))
        if record.id in dc:
            s = record.seq
            d = dc[record.id]
            for line in d:
                seq = give_seq(s,line[1],line[2],line[3],chrom_len=lerese)
                if seq:
                    gene = line[0]
                    genes.append(Bio.SeqRecord.SeqRecord(seq,id=gene,name="",description=""))
            Bio.SeqIO.write(genes, output_handle, "fasta")
            genes = []
    output_handle.close()

    #file(os.path.join(options.output_directory,'chromosomes_information.txt'),'w').writelines(chrome)
    #
