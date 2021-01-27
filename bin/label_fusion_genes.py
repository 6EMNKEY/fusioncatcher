#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It labels the candidate list of fusion genes generated by 'find_fusion_genes.py'.



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
import sys
import os
import optparse

if __name__ == '__main__':

    #command line parsing

    usage="%prog [options]"
    description="""It labels the candidate list of fusion genes generated by 'find_fusion_genes.py'."""
    version="%prog 0.10 beta"

    parser=optparse.OptionParser(usage=usage,description=description,version=version)

    parser.add_option("--input",
                      action="store",
                      type="string",
                      dest="input_fusion_genes_filename",
                      help="""The input file in text tab delimited format containing the fusion genes candidates produced by 'find_fusion_genes.py'. """)


    parser.add_option("--filter_gene_pairs",
                      action="store",
                      type="string",
                      dest="input_filter_gene_pairs_filename",
                      help="""The input text file tab separated format containing gene pairs which are used as filter for labeling (two columns and no header; the order of genes in the gene pairs is ignored).""")

    parser.add_option("--filter_gene_pairs_threshold",
                      action="store",
                      type="int",
                      dest="input_filter_gene_pairs_threshold",
                      default = 0,
                      help="""The threshold which will be used to filter the gene fusions from '--filter_gene_pairs' only if there is a third column. The threshold will applied to the third column. Default is '%default'.""")


    parser.add_option("--filter_genes",
                      action="store",
                      type="string",
                      dest="input_filter_genes_filename",
                      help="""The input text file format containing genes which are used as filter for labeling.""")

    parser.add_option("--label",
                      action="store",
                      type="string",
                      dest="label",
                      help="""Label used to mark the candidate fusion genes which are founf in the filter.""")

    parser.add_option("--output_fusion_genes",
                      action="store",
                      type="string",
                      dest="output_fusion_genes_filename",
                      help="""The output text tab-separated file containing the candidate fusion genes which are found in the filter. The format is as the input file and sorted by counts column.""")


    parser.add_option("--similar_gene_symbols",
                      action = "store_true",
                      dest = "similar_gene_symbols",
                      default = False,
                      help = """It labels the pairs of genes which have similar gene HUGO symbols (i.e. the symbol name is the same except the last character). Default is %default.""")

    parser.add_option("--min_dist_gene_gene",
                      action = "store",
                      type = "int",
                      dest = "input_min_dist_gene_gene",
                      help = """It labels the pairs of genes where the distance between the genes is below a given threshold (for example 100000 bp).""")

    parser.add_option("--min_dist_gene_gene_database",
                      action = "store",
                      type = "string",
                      dest = "input_min_dist_gene_gene_database_filename",
                      help = """Database with exons position on chromosomes which is used to extract the gene positions, e.g. 'more_exons_ensembl.txt'. This is needed only when '--min_distance_gene_gene' is used.""")



    (options,args) = parser.parse_args()

    # validate options
    if not (options.input_fusion_genes_filename and
            options.output_fusion_genes_filename and
            options.label
            ):
        parser.print_help()
        parser.error("One of the options has not been specified.")
        sys.exit(1)

    if not (options.input_filter_gene_pairs_filename or options.input_filter_genes_filename or options.input_min_dist_gene_gene):
        parser.error("At least one of the options '--filter_gene_pairs' or '--filter_genes' or '--min_dist_gene_gene should be specified.")
        sys.exit(1)

    if options.input_filter_gene_pairs_filename and options.input_filter_genes_filename:
        parser.error("Only one if the options '--filter_gene_pairs' or '--filter_genes' should be specified.")
        sys.exit(1)

    if (((not options.input_min_dist_gene_gene_database_filename) and options.input_min_dist_gene_gene) or
       (options.input_min_dist_gene_gene_database_filename and (not options.input_min_dist_gene_gene))):
        parser.error("Both command line parameters are needed to be specified '--min_dist_gene_gene' and '--min_dist_gene_gene_database'.")
        sys.exit(1)


    homologs = set()
    if options.input_filter_gene_pairs_filename:
        print "Reading...",options.input_filter_gene_pairs_filename
        if os.path.isfile(options.input_filter_gene_pairs_filename) or os.path.islink(options.input_filter_gene_pairs_filename):
            if options.input_filter_gene_pairs_threshold and options.input_filter_gene_pairs_threshold > 0:
                homologs = [line.rstrip('\r\n').split('\t')[:3] for line in file(options.input_filter_gene_pairs_filename,'r') if line.rstrip('\r\n')]
                homologs = [line[:2] for line in homologs if len(line)>2 and line[2].isdigit() and int(line[2])>=options.input_filter_gene_pairs_threshold]
                homologs=set(['\t'.join(sorted(line)) for line in homologs])
            else:
                homologs=set(['\t'.join(sorted(line.rstrip('\r\n').split('\t')[:2])) for line in file(options.input_filter_gene_pairs_filename,'r') if line.rstrip('\r\n')])

    no_proteins = set()
    if options.input_filter_genes_filename:
        print "Reading...",options.input_filter_genes_filename
        no_proteins=set([line.rstrip('\r\n') for line in file(options.input_filter_genes_filename,'r') if line.rstrip('\r\n')])

    genes = {}
    if options.input_min_dist_gene_gene_database_filename:
        print "Processing the exons database...",options.input_min_dist_gene_gene_database_filename
        # ensembl_peptide_id             0
        # ensembl_gene_id                1
        # ensembl_transcript_id          2
        # ensembl_exon_id                3
        # exon_chrom_start               4
        # exon_chrom_end                 5
        # rank                           6
        # start_position                 7
        # end_position                   8
        # transcript_start               9
        # transcript_end                 10
        # strand                         11
        # chromosome_name                12
        # cds_start                      13
        # cds_end                        14
        # 5_utr_start                    15
        # 5_utr_end                      16
        # 3_utr_start                    17
        # 3_utr_end                      18
        exons = [line.rstrip('\r\n').split('\t') for line in file(options.input_min_dist_gene_gene_database_filename,'r').readlines() if line.rstrip('\r\n')]
        exons = [(line[1], # gene_id              0
                  line[7], # gene_start           1
                  line[8], # gene_end             2
                  line[11],# strand               3
                  line[12] # chromosome           4
                  ) for line in exons]
        for line in exons:
            gn = line[0]
            gs = int(line[1])
            ge = int(line[2])
            st = int(line[3])
            ch = line[4]
            if gs > ge:
                (gs,ge) = (ge,gs)
            if gn not in genes:
                genes[gn] = {'start':gs,
                             'end':ge,
                             'strand':st,
                             'chrom':ch}


    print "Reading...",options.input_fusion_genes_filename
    # Assume format:
    #Fusion_gene_1	Fusion_gene_2	Count_paired-end_reads	Fusion_gene_symbol_1	Fusion_gene_symbol_2
    #ENSG00000175110	ENSG00000233830	1	MRPS22
    #ENSG00000205246	ENSG00000233924	1	RPSAP18,RPSAP8,RPSAP58
    #ENSG00000103222	ENSG00000116857	1	ABCC1	TMEM9
    #...
    data=[line.rstrip('\r\n').split('\t') for line in file(options.input_fusion_genes_filename,'r').readlines() if line.rstrip('\r\n')]
    header=data.pop(0)
    # add the labels on column no. 6
    label_col = False
    if len(header) == 5:
        label_col = True
        header.append('Fusion_description')
    temp = []
    label = options.label


    if options.input_min_dist_gene_gene:
        # deal with the distance between genes and label accordingly
        for line in data:
            a = line[0]
            b = line[1]


            if (genes.has_key(a) and
                genes.has_key(b) and
                genes[a]["chrom"] == genes[b]["chrom"] and
                genes[a]["strand"] == genes[b]["strand"] and
                min([abs(genes[a]["start"]-genes[b]["start"]),
                     abs(genes[a]["start"]-genes[b]["end"]),
                     abs(genes[a]["end"]-genes[b]["start"]),
                     abs(genes[a]["end"]-genes[b]["end"])]) <= options.input_min_dist_gene_gene
               ):
                if label_col:
                    temp.append(line+[label])
                else:
                    if line[-1]:
                        temp.append(line[:-1]+[','.join([line[-1],label])])
                    else:
                        temp.append(line[:-1]+[label])
            else:
                if label_col:
                    temp.append(line+[''])
                else:
                    temp.append(line)


    else:
        similar = 'similar_symbols'
        myset = set(['.','-','_'])

        def handle_hyphen(cba,card):
            cba = cba.lower().strip()
            for ix in xrange(100,-1,-1):
                kx = "%s%d" % (card.lower(),ix)
                if cba.endswith(kx):
                    cba = cba.replace(kx,'')
                    break
            return cba

        for line in data:
            a=line[0]
            b=line[1]
            c = line[3].lower()
            d = line[4].lower()
            flag = False

            if (options.similar_gene_symbols and
                c and
                d and
                (
                (
                len(c) > 3 and
                len(d) > 3 and
                (
                 (c[:-1] == d[:-1] and c[-1] in myset) or
                 (c[:-2] == d[:-2] and c[-2] in myset) or
                 (c[:-1] == d[:-2] and c[-1] in myset) or
                 (c[:-2] == d[:-1] and c[-2] in myset)
                )
                ) or
                (c == d) or
                (handle_hyphen(c,'-as') == handle_hyphen(d,'-as')) or
                (handle_hyphen(c,'-it') == handle_hyphen(d,'-it'))
                )

                ):
                label = options.label + ',' + similar
                flag = True
            else:
                label = options.label

            g='\t'.join(sorted([a,b]))
            if (g in homologs) or (a in no_proteins) or (b in no_proteins):
                if label_col:
                    temp.append(line+[label])
                else:
                    if line[-1]:
                        temp.append(line[:-1]+[','.join([line[-1],label])])
                    else:
                        temp.append(line[:-1]+[label])
            else:
                if label_col:
                    if flag:
                        temp.append(line+[similar])
                    else:
                        temp.append(line+[''])
                else:
                    if flag:
                        temp.append(line[:-1]+[','.join([line[-1],similar])])
                    else:
                        temp.append(line)

#            print c,d,temp

    data=sorted(temp,key=lambda x: ( (-int(x[2]),x[0],x[1]) ) )
    data.insert(0,header)
    file(options.output_fusion_genes_filename,'w').writelines(['\t'.join(line)+'\n' for line in data])

    print "The end."
