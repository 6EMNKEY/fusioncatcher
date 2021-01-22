# Table of Contents
1. [Introduction](#1---introduction)
2. [Hardware requirements and dependencies](#2---hardware-requirements-and-dependencies)
3. [FusionCatcher in scientific articles](#3---fusioncatcher-in-scientific-articles)
4. [Installation and usage examples](#4---installation-and-usage-examples)
5. [Quick installation](#5---quick-installation)
6. [Usage](#6---usage)
7. [Aligners](#7---aligners)
8. [Command line options](#8---command-line-options)
9. [Methods](#9---methods)
10. [Comparisons to other tools](#10---comparisons-to-other-tools)
11. [License](#11---license)
12. [Citing](#12---citing)
13. [Reporting bugs](#13---reporting-bugs)

---


# 1 - INTRODUCTION

*FusionCatcher* searchers for **somatic** novel/known **fusion genes**, **translocations** and/or **chimeras** in RNA-seq data (stranded/unstranded  **paired-end/single-end** reads FASTQ files produced by Illumina next-generation sequencing platforms like Illumina Solexa/`HiSeq`/`NextSeq`/`MiSeq`/`MiniSeq`) from _diseased_ samples.

The aims of *FusionCatcher* are:
  * very good detection rate for finding candidate **somatic fusion genes** (see [somatic mutations](http://en.wikipedia.org/wiki/Mutation#Somatic_mutations); using a matched **normal** sample is optional; several databases of known fusion genes found in healthy samples are used as a list of known false positives; biological knowledge is used, like for example gene fusion between a gene and its pseudogene is filtered out),
  * very good RT-PCR validation rate of found candidate somatic fusion genes (this is very important for us),
  * very easy to use (i.e. no _a priori_ knowledge of bioinformatic databases and bioinformatics is needed in order to run *FusionCatcher* BUT Linux/Unix knowledge is needed; it allows a very high level of control for expert users),
 * very good detection of challenging fusion genes, like for example IGH fusions, CIC fusions, DUX4 fusions, CRLF2 fusions, TCF3 fusions, etc.,
  * to be as automatic as possible (i.e. the *FusionCatcher* will choose automatically the best parameters in order to find candidate somatic fusion genes, e.g. finding automatically the adapters, quality trimming of reads, building the exon-exon junctions automatically based on the length of the reads given as input, etc. while giving also full control to expert users) while providing the best possible detection rate for finding somatic fusion genes (with a very low rate of false positives but a very good sensitivity).

*FusionCatcher* supports:
  * as input FASTQ and/or SRA file types (paired-end reads from stranded or strand-specific experiments, single-end reads when they are longer than 130bp),
  * five different methods (using Bowtie aligner and optionally BLAT, STAR, BOWTIE2 aligners) for finding new fusion genes **BUT** by default only Bowtie, Blat, and STAR aligners will be used,
  * several eukaryotic organisms (which are in [Ensembl database](http://www.ensembl.org/index.html)), like for example, human, rat, mouse, dog, etc.

---


# 2 - HARDWARE REQUIREMENTS AND DEPENDENCIES

For running *FusionCatcher* it is needed a computer with:
  * 64-bit `*NIX` environment
  * minimum 24 GB of RAM (in many cases it might work even with 16GB of RAM for very small input FASTQ files in order of megabytes)
  * 1 CPU (minimum)
  * ~700 GB temporary disk space (needed just for temporary files)


## 2.1 - Required dependencies
  * **Linux/Unix** 64-bit (e.g. Ubuntu version 12.04/14.04/16.04 or newer)
  * **Python** version 2.7.x (>=2.6.0 and < 3.0 is fine)
  * **BioPython** version 1.73 (>=1.50 is fine)
  * **Bowtie** 64-bit version 1.2.3 http://bowtie-bio.sourceforge.net/index.shtml (will be installed by `boostrap.py`)
  * forked **SeqTK** version 1.2-r101c-dirty  http://github.com/ndaniel/seqtk (will be installed by `boostrap.py`)
  * **fastqtk** version 0.27  http://github.com/ndaniel/fastqtk (will be installed by `boostrap.py`)
  * organism specific  data from [Ensembl](http://www.ensembl.org) database release 102 (all downloading and the necessary building process is handled automatically by the included/provided tool `fusioncatcher-build` and therefore no knowledge of Ensembl database or other databases is needed) (will be installed by `boostrap.py`)
  * **STAR** version 2.7.2b https://github.com/alexdobin/STAR . Executables are available at http://github.com/alexdobin/STAR/releases (will be installed by `boostrap.py`)
  * **BOWTIE2** version 2.3.5.1 http://bowtie-bio.sourceforge.net/bowtie2/index.shtml (will be installed by `boostrap.py`)
  * **BBMAP** version 38.44 https://sourceforge.net/projects/bbmap/ (will be installed by `boostrap.py`)

## 2.2 - Optional dependencies

### 2.2.1 - Strongly recommended
These are expected by default to be installed but their use can be disabled by using the command line option '--skip-blat'.
  * **BLAT** version 0.35 http://users.soe.ucsc.edu/~kent/src/ . Executables are available at http://hgdownload.cse.ucsc.edu/admin/exe/ . Please, check the license to see if it allows you to run/use it! This is needed by *FusionCatcher* (hint: if you are a non-profit organization you should be fine) (will be installed by `boostrap.py`)
  * **faToTwoBit** http://users.soe.ucsc.edu/~kent/src/ . Executables are available at http://hgdownload.cse.ucsc.edu/admin/exe/ . Please, check the license to see if it allows you to run/use it! This is needed by *FusionCatcher* and `fusioncatcher-build` if one plans to use BLAT as a second (optional) alternative method for finding fusion genes! (required also by option `--blat-visualization`) (will be installed by `boostrap.py`)

Note: If one does not want to install BLAT (whilst installing *FusionCatcher* automatically thru `bootstrap.py`) and also not to use BLAT with *FusionCatcher* then using command line `-k` option of `bootstrap.py` will do that.

### 2.2.2 - Nice to have (but optional)
  * **Velvet** (de novo assembler) version 1.2.10 http://www.ebi.ac.uk/~zerbino/velvet/ . This is needed if one plans to do _de novo_ assembly of the reads which support the candidate fusion genes. (required by option `--assembly` of *FusionCatcher*) (will be installed by `boostrap.py`)
  * **fastq-dump** version 2.9.6 from NCBI SRA Toolkit http://www.ncbi.nlm.nih.gov/Traces/sra/?view=software . This is needed by *FusionCatcher* if one plans to use as input SRA files (will be installed by `boostrap.py`)
  * Python library **openpyxl** version 1.5.6 http://pypi.python.org/pypi/openpyxl (other versions might work but have not been tested). It is needed by `fusioncatcher-build` for parsing the [ConjoinG](http://metasystems.riken.jp/conjoing/) database.
  * Python library **xlrd** version 0.6.1 http://pypi.python.org/pypi/xlrd (other versions might work but have not been tested). It is needed by `fusioncatcher-build` for parsing the [ChimerDB](http://ercsb.ewha.ac.kr/FusionGene/) database.
  * **pigz** version 2.3.1 http://zlib.net/pigz/ for using GZIP on several CPUs in parallel (other older versions might support this) (will be installed by `boostrap.py`)
  * **Picard tools** version 2.21.2 http://github.com/broadinstitute/picard (will be installed by `boostrap.py`)

## 2.3 - Genomic Databases
These are used (downloaded and parsed) automatically by `boostrap.py` of *FusionCatcher*:
  * **ENSEMBL** database http://www.ensembl.org/ (required)
  * **UCSC** database http://hgdownload.cse.ucsc.edu/downloads.html#human (required)
  * **RefSeq** database (thru **UCSC** database) (required)
  * **Viruses/bacteria/phages** genomes database (from the NCBI database) [ftp://ftp.ncbi.nlm.nih.gov/genomes/Viruses/](ftp://ftp.ncbi.nlm.nih.gov/genomes/Viruses/) (required)
  * **COSMIC** database http://cancer.sanger.ac.uk/cancergenome/projects/cosmic/ (optional)
  * **TICdb** database http://www.unav.es/genetica/TICdb/ (optional)
  * **ChimerDB 2.0** database (literature-based annotation) http://ercsb.ewha.ac.kr/FusionGene/ (optional)
  * **Cancer Genome Project** **(CGP)** translocations database http://www.sanger.ac.uk/genetics/CGP/Census/ (optional)
  * **ConjoinG** database http://metasystems.riken.jp/conjoing/ (optional)
  * **CACG** conjoined genes database http://cgc.kribb.re.kr/map/ (optional)
  * **DGD** database http://dgd.genouest.org/ (optional)
  * **Illumina BodyMap2 RNA-seq** database http://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-513/

**NOTES**:
  * **ENSEMBL** database is used for finding novel/known fusions genes
  * **COSMIC**, **TICdb**, **ChimerDB**, **Cancer Genome Project**, **ConjoinG**, and manual curated fusion gene database are indexed and used further for annotating/labeling the found fusion genes for an easier visualization of **novel** genes (i.e. not published yet) found by *FusionCatcher*. For more information how this is used see [Tables 1,2,3](#output-data).
  * *FusionCatcher* can work just fine and is able to find fusion genes without any of the optional dependencies/tools/programs!
  * if **BLAT** is not installed (or one does not want to use it) please use option '--skip-blat' in order to let know *FusionCatcher* that it should not use it! Also, specifying that BLAT should be be used can be done by editing manually the line `aligners = blat,star` from file `fusioncatcher/etc/configuration.cfg` (that is remove the `blat` string).


---

# 3 - FusionCatcher in scientific articles

*FusionCatcher* has been used for finding novel and known fusion genes in the following articles:
  * S. Kangaspeska, S. Hultsch, H. Edgren, D. Nicorici, A. Murumägi, O.P. Kallioniemi, **Reanalysis of RNA-sequencing data reveals several additional fusion genes with multiple isoforms**, PLOS One, Oct. 2012. http://dx.doi.org/10.1371/journal.pone.0048745
  * H. Edgren, A. Murumagi, S. Kangaspeska, D. Nicorici, V. Hongisto, K. Kleivi, I.H. Rye, S. Nyberg, M. Wolf, A.L. Borresen-Dale, O.P. Kallioniemi, **Identification of fusion genes in breast cancer by paired-end RNA-sequencing**, Genome Biology, Vol. 12, Jan. 2011. http://dx.doi.org/10.1186/gb-2011-12-1-r6
  * JN. Honeyman, EP. Simon, N. Robine, R. Chiaroni-Clarke, DG. Darcy, I. Isabel, P. Lim, CE. Gleason, JM. Murphy, BR. Rosenberg, L. Teegan, CN. Takacs, S. Botero, R. Belote, S. Germer, A-K. Emde, V. Vacic, U. Bhanot, MP. LaQuaglia, and S.M. Simon, **Detection of a Recurrent DNAJB1-PRKACA Chimeric Transcript in Fibrolamellar Hepatocellular Carcinoma**, Science 343 (6174), Feb. 2014, pp. 1010-1014, http://dx.doi.org/10.1126/science.1249484
  * T. Pietsch, I. Wohlers, T. Goschzik, V. Dreschmann, D. Denkhaus, E. Dorner, S. Rahmann, L. Klein-Hitpass, **Supratentorial ependymomas of childhood carry C11orf95–RELA fusions leading to pathological activation of the NF-kB signaling pathway**, Acta Neuropathologica 127(4), Apr. 2014, pp. 609-611. http://dx.doi.org/10.1007/s00401-014-1264-4
  * M. Jimbo, K.E. Knudsen, J.R. Brody, **Fusing Transcriptomics to Progressive Prostate Cancer**, The American Journal of Pathology, 2014, http://dx.doi.org/10.1016/j.ajpath.2014.08.001
  * Y.P. Yu, Y. Ding, Z. Chen, S. Liu, A. Michalopoulos, R. Chen, Z. Gulzar, B. Yang, K.M. Cieply, A. Luvison, B.G. Ren, J.D. Brooks, D. Jarrard, J.B. Nelson. G.K. Michalopoulos, G.C. Tseng, J.H. Luo, **Novel fusion transcripts associate with progressive prostate cancer**,  The American Journal of Pathology, 2014, http://dx.doi.org/10.1016/j.ajpath.2014.06.025
  * C.M Lindqvist, J. Nordlund, D. Ekman, A. Johansson, B.T. Moghadam, A. Raine, E. Overnas, J. Dahlberg, P. Wahlberg, N. Henriksson, J. Abrahamsson, B.M. Frost, D. Grander, M. Heyman, Rolf Larsson, J. Palle, S. Soderhall, E. Forestier, G. Lonnerholm, A.C. Syvanen, E.C. Berglund, **The Mutational Landscape in Pediatric Acute Lymphoblastic Leukemia Deciphered by Whole Genome Sequencing**, Human Mutation, 2014, http://dx.doi.org/10.1002/humu.22719
  * I. Panagopoulos, L. Gorunova, B. Davidson, Sverre Heim, **Novel TNS3-MAP3K3 and ZFPM2-ELF5 fusion genes identified by RNA sequencing in multicystic mesothelioma with t(7;17)(p12;q23) and t(8;11)(q23;p13)**, Cancer Letters, Dec. 2014, http://dx.doi.org/10.1016/j.canlet.2014.12.002
  * J.C Lee, Y.M. Jeng, S.Y. Su, C.T Wu, K.S. Tsai, C.H. Lee, C.Y. Lin, J.M. Carter, J. W. Huang, S.H. Chen, S.R. Shih, A. Marino-Enriquez, C.C. Chen, A.L. Folpe, Y.L. Chang, C.W. Liang, **Identification of a novel FN1–FGFR1 genetic fusion as a frequent event in phosphaturic mesenchymal tumour**, The journal of Pathology, Jan. 2015, http://dx.doi.org/10.1002/path.4465
  * J. Nordlund, C.L. Backlin, V. Zachariadis, L. Cavelier, J. Dahlberg, I. Ofverholm, G. Barbany, A. Nordgren, E. Overnas, J. Abrahamsson, T. Flaegstad, M.M. Heyman, O.G. Jonsson, J. Kanerva, R. Larsson, J. Palle, K. Schmiegelow, M.G. Gustafsson, G. Lonnerholm, E. Forestier, A.C. Syvanen, **DNA methylation-based subtype prediction for pediatric acute lymphoblastic leukemia**, Clinical Epigenetics, 7:11, Feb. 2015,  http://dx.doi.org/10.1186/s13148-014-0039-z
  * J.H. Luo, S. Liu, Z.H. Zuo, R. Chen, G.C. Tseng, Y.P. Yu, **Discovery and Classification of Fusion Transcripts in Prostate Cancer and Normal Prostate Tissue**, The American Journal of Pathology, May 2015, http://dx.doi.org/10.1016/j.ajpath.2015.03.008
  * T. Meissner, K.M. Fisch, L. Gioia, **OncoRep: an n-of-1 reporting tool to support genome-guided treatment for breast cancer patients using RNA-sequencing**, BMC Medical Genomics, May 2015, http://dx.doi.org/10.1186/s12920-015-0095-z
  * S. Torkildsen, L. Gorunova, K. Beiske, G.E. Tjonnfjord, S. Heim, I. Panagopoulos, **Novel ZEB2-BCL11B Fusion Gene Identified by RNA-Sequencing in Acute Myeloid Leukemia with t(2;14)(q22;q32)**, PLOS One, July 2015, http://dx.doi.org/10.1371/journal.pone.0132736
  * M. Cieslik, R. Chugh, Y.M. Wu, M. Wu, C. Brennan, R. Lonigro, F. Su, R. Wang, J. Siddiqui, R. Mehra, X. Cao, D. Lucas, A.M. Chinnaiyan, D. Robinson, **The use of exome capture RNA-seq for highly degraded RNA with application to clinical cancer sequencing**, Genome Research, August 2015, http://dx.doi.org/10.1101/gr.189621.115
  * E.P. Simon, C.A. Freije, B.A. Farber, G. Lalazar, D.G. Darcy, J.N. Honeyman, R. Chiaroni-Clark, B.D. Dill, H. Molina, U.K. Bhanot, M.P. La Quaglia, B.R. Rosenberg, S.M. Simon, **Transcriptomic characterization of fibrolamellar hepatocellular carcinoma**, PNAS, October 2015, http://dx.doi.org/10.1073/pnas.1424894112 
  * Y. Marincevic-Zuniga, V. Zachariadis, L. Cavelier, A. Castor, G. Barbany, E. Forestier, L. Fogelstrand, M. Heyman, J. Abrahamsson, G. Lonnerholm, A. Nordgren, A.C. Syvanen, J. Nordlund, **PAX5-ESRRB is a recurrent fusion gene in B-cell precursor pediatric acute lymphoblastic leukemia**, Haematologica, October 2015, http://dx.doi.org/10.3324/haematol.2015.132332
  * M. Brenca, S. Rossi, M. Polano, D. Gasparotto, L. Zanatta, D. Racanelli, L. Valori, S. Lamon, A.P. Dei Tos, R. Maestro, **Transcriptome sequencing identifies ETV6-NTRK3 as a gene fusion involved in GIST**, The Journal of Pathology, November 2015, http://dx.doi.org/10.1002/path.4677
  * Roberts K.G., et al. **High Frequency and Poor Outcome of Ph-like Acute Lymphoblastic Leukemia in Adults**, Blood Journal, Vol. 126, December 2015, http://www.bloodjournal.org/content/126/23/2618
  * Kekeeva T., et al. **Novel fusion transcripts in bladder cancer identified by RNA-seq**, Cancer Letters, Feb. 2016, http://dx.doi.org/10.1016/j.canlet.2016.02.010
  * Panagopoulos I. et al. **Rare MLL-ELL fusion transcripts in childhood acute myeloid leukemia-association with young age and myeloid sarcomas?**, Experimental Hematology & Oncology, Vol. 5, March 2016, http://dx.doi.org/10.1186/s40164-016-0037-2 
  * Chang W. et al, **Multi-Dimensional ClinOmics for Precision Therapy of Children and Adolescent Young Adults with Relapsed and Refractory Cancer: A report from the Center for Cancer Research**, Clinical Cancer Research, March 2016, http://dx.doi.org/10.1158/1078-0432.CCR-15-2717
  * Spans L. et al., **Recurrent MALAT1-GLI1 oncogenic fusion and GLI1 upregulation define a subset of plexiform fibromyxoma**, The Journal of Pathology, April 2016, http://dx.doi.org/10.1002/path.4730
  * Micci F. et al., **Cytogenetic and Molecular Profile of Endometrial Stromal Sarcoma**, Genes Chromosomes & Cancer, May 2016, http://dx.doi.org/10.1002/gcc.22380
  * Olsen K.T. et al., **Novel Fusion Genes and Chimeric Transcripts in Ependymal Tumors**, Genes Chromosomes & Cancer, July 2016, http://dx.doi.org/10.1002/gcc.22392
  * Panagopoulos I. et al., **Recurrent fusion of the genes FN1 and ALK in gastrointestinal leiomyomas**, Modern Pathology, July 2016, http://dx.doi.org/10.1038/modpathol.2016.129
  * Barnes D.J. et al., **A germline mutation of CDKN2A and a novel RPLP1-C19MC fusion detected in a rare melanotic neuroectodermal tumor of infancy: a case report**, BMC Cancer, August 2016, http://dx.doi.org/10.1186/s12885-016-2669-3
  * Panagopoulos I. et al., **Gene fusions AHRR-NCOA2, NCOA2-ETV4, ETV4-AHRR, P4HA2-TBCK, and TBCK-P4HA2 resulting from the translocations t(5;8;17)(p15;q13;q21) and t(4;5)(q24;q31) in a soft tissue angiofibroma**, Oncology Reports, Sept. 2016, http://dx.doi.org/10.3892/or.2016.5096
  * Lang P.Y. et al., **ATR maintains chromosomal integrity during postnatal cerebellar neurogenesis and is required for medulloblastoma formation**, Development, Nov. 2016, http://dx.doi.org/10.1242/dev.139022
  * Gu Z. et al., **Genomic analyses identify recurrent MEF2D fusions in acute lymphoblastic leukaemia**, Nature Communications, Nov. 2016, http://dx.doi.org/10.1038/ncomms13331
  * Alaei-Mahabadi B. et al., **Global analysis of somatic structural genomic alterations and their impact on gene expression in diverse human cancers**, PNAS, Nov. 2016, http://dx.doi.org/10.1073/pnas.1606220113
  * Yap K.L. et al., **Diagnostic evaluation of RNA sequencing for the detection of genetic abnormalities associated with Ph-like acute lymphoblastic leukemia (ALL)**, Leukemia & Lymphoma, Nov. 2016, http://dx.doi.org/10.1080/10428194.2016.1219902
  * Brunetti M. et al., **Recurrent fusion transcripts in squamous cell carcinomas of the vulva**, Oncotarget, Feb. 2017, http://dx.doi.org/10.18632/oncotarget.15167
  * Sahm F. et al., **DNA methylation-based classification and grading system for meningioma: a multicentre, retrospective analysis**, The Lancet Oncology, March 2017, http://dx.doi.org/10.1016/S1470-2045(17)30155-9
  * Reshmi S.C. et al., **Targetable kinase gene fusions in high risk B-ALL: a study from the Children's Oncology Group**, Blood, April 2017, https://doi.org/10.1182/blood-2016-12-758979
  * Tomic T.T. et al., **A new GTF2I-BRAF fusion mediating MAPK pathway activation in pilocytic astrocytoma**, PLOS One, April 2017, https://doi.org/10.1371/journal.pone.0175638
  * Schwartzman O. et al., **Suppressors and activators of JAK-STAT signaling at diagnosis and relapse of acute lymphoblastic leukemia in Down syndrome**, PNAS, May 2017, https://doi.org/10.1073/pnas.1702489114
  * Panagopoulos I. et al., **Identification of SETD2-NF1 fusion gene in a pediatric spindle cell tumor with the chromosomal translocation t(3;17)(p21;q12)**, Oncology Reports, May 2017, https://doi.org/10.3892/or.2017.5628
  * Sorenson E.C. et al., **Genome and transcriptome profiling of fibrolamellar hepatocellular carcinoma demonstrates p53 and IGF2BP1 dysregulation**, PLOS One, May 2017, https://doi.org/10.1371/journal.pone.0176562
  * Hettmer S. et al., **Epithelioid hemangioendotheliomas of the liver and lung in children and adolescents**, Pediatric Blood & Cancer, June 2017, https://doi.org/10.1002/pbc.26675
  * Pisapia D.J. et al., **Next-Generation Rapid Autopsies Enable Tumor Evolution Tracking and Generation of Preclinical Models**, JCO Precision Oncology, June 2017, https://doi.org/10.1200/PO.16.00038 
  * Bekers E.M. et al., **Soft tissue angiofibroma – clinicopathologic, immunohistochemical and molecular analysis of 14 cases**, Genes, Chromosomes and Cancers, June 1027, https://doi.org/10.1002/gcc.22478
  * Mandahl N. et al., **Scattered genomic amplification in dedifferentiated liposarcoma**, Molecular Cytogenetics, Vol. 10, June 2017, https://doi.org/10.1038/10.1186/s13039-017-0325-5
  * Biaconi D. et al., **Biochemical and genetic predictors of overall survival in patients with metastatic pancreatic cancer treated with capecitabine and nab-paclitaxel**, Scientific Reports, Vol. 7, July 2017, https://doi.org/10.1038/s41598-017-04743-0
  * Sahraeian S.M.E. et.al., **Gaining comprehensive biological insight into the transcriptome by performing a broad-spectrum RNA-seq analysis**, Nature Communication, Vol. 8, July 2017, https://doi.org/10.1038/s41467-017-00050-4
  * Micci F. et al., **Fusion of the Genes BRD8 and PHF1 in Endometrial Stromal Sarcoma**, Genes, Chromosomes and Cancers, July 2017,  https://doi.org/10.1002/gcc.22485
  * Kivioja J.L. et al., **Chimeric NUP98–NSD1 transcripts from the cryptic t(5;11)(q35.2;p15.4) in adult de novo acute myeloid leukemia**, Leukemia and Lymphoma, Aug. 2017, http://dx.doi.org/10.1080/10428194.2017.1357174
  * Marincevic-Zuniga Y. et al., **Transcriptome sequencing in pediatric acute lymphoblastic leukemia identifies fusion genes associated with distinct DNA methylation profiles**, Journal of Hematology and Oncology, Aug. 2017, http://doi.org/10.1186/s13045-017-0515-y
  * Kumar A. et al., **The impact of RNA sequence library construction protocols on transcriptomic profiling of leukemia**, BMC Genomics, Aug. 2017, http://doi.org/10.1186/s12864-017-4039-1
  * Singh R. et al., **Analysis of the whole transcriptome from gingivo-buccal squamous cell carcinoma reveals deregulated immune landscape and suggests targets for immunotherapy**, PLOS One, Sept. 2017, http://doi.org/10.1371/journal.pone.0183606
  * Arbajian E. et al., **Inflammatory leiomyosarcoma is a distinct tumor characterized by near-haploidization, few somatic mutations, and a primitive myogenic gene expression signature**, Modern Pathology, Sept. 2017,   http://doi.org/10.1038/modpathol.2017.113
  * Varghese, A.M. et al., **Clinical and molecular characterization of patients with cancers of unknown primary in the modern era**, Annals of Oncology, Sep. 2017, http://doi.org/10.1093/annonc/mdx545
  * Persson H. et al., **Frequent miRNA-convergent fusion gene events in breast cancer**, Nature Communications, Oct. 2017, http://doi.org/doi:10.1038/s41467-017-01176-1
  * Gu J. et al., **RNA-seq Based Transcription Characterization of Fusion Breakpoints as a Potential Estimator for Its Oncogenic Potential**, BioMed Research International, Oct. 2017, http://doi.org/10.1155/2017/9829175
  * Dalin M.G. et al., **Multi-dimensional genomic analysis of myoepithelial carcinoma identifies prevalent oncogenic gene fusions**, Nature Communications, Oct. 2017, http://doi.org/10.1038/s41467-017-01178-z
  * Panagopoulos I. et al., **DEK-NUP214-Fusion Identified by RNA-Sequencing of an Acute Myeloid Leukemia with t(9;12)(q34;q15)**, Cancer Genomics and Proteomics, Nov. 2017, http://doi.org/10.21873/cgp.20053 
  * Kita K. et al., **In vivo imaging xenograft models for the evaluation of anti-brain tumor efficacy of targeted drugs**, Cancer Medicine, Nov. 2017, http://doi.org/10.1002/cam4.1255
  * Xia Q. Y. et al., **Novel gene fusion of PRCC-MITF defines a new member of MiT family translocation renal cell carcinoma: clinicopathologic analysis and detection of the gene fusion by RNA-sequencing and FISH**, Histopathology, Nov. 2017, http://doi.org/10.1111/his.13439
  * Chang M.T. et al., **Small cell carcinomas of the bladder and lung are characterized by a convergent but
distinct pathogenesis**, Clinical Cancer Research, Nov. 2017, http://doi.org/10.1158/1078-0432.CCR-17-2655
  * Arbajian E. et al., **In-depth Genetic Analysis of Sclerosing Epithelioid Fibrosarcoma Reveals Recurrent Genomic Alterations and Potential Treatment Targets**, Clinical Cancer Research, Dec. 2017, http://doi.org/10.1158/1078-0432.CCR-17-1856
 * Brunetti M. et al., **RNA-Sequencing identifies novel GREB1-NCOA2 fusion gene in a uterine sarcoma with the chromosomal translocation t(2;8)(p25;q13)**, Genes Chromosomes Cancer, Dec. 2017, http://doi.org/10.1002/gcc.22518
 * Gillard M. et al., **Integrative Genomic Analysis of Coincident Cancer Foci Implicates CTNNB1 and PTEN Alterations in Ductal Prostate Cancer**, European Urology Focus, Dec. 2017, https://doi.org/10.1016/j.euf.2017.12.003
 * Alamri A.M. et al., **Expanding primary cells from mucoepidermoid and other salivary gland neoplasms for genetic and chemosensitivity testing**, Disease Models and Mechanisms, Jan. 2018, https://doi.org/10.1242/dmm.031716
 * Togashi Y. et al., **MYB and MYBL1 in adenoid cystic carcinoma: diversity in the mode of genomic rearrangement and transcripts**, Modern Pathology, Feb. 2018, https://doi.org/10.1038/s41379-018-0008-8
 * Roussy M. et al., **NUP98-BPTF gene fusion identified in primary refractory acute megakaryoblastic leukemia of infancy**, Genes, Chromosomes and Cancer, Feb. 2018, https://doi.org/10.1002/gcc.22532
 * Nishiyama A. et al., **Foretinib overcomes entrectinib resistance associated with the NTRK1 G667C mutation in NTRK1 fusion-positive tumor cells in a brain metastasis model**, Clinical Cancer Research, Feb. 2018, https://doi.org/10.1158/1078-0432.CCR-17-1623 
 * Liu H. et al., **Identifying and Targeting Sporadic Oncogenic Genetic Aberrations in Mouse Models of Triple-Negative Breast Cancer**, Cancer Discovery, March 2018, https://doi.org/10.1158/2159-8290.CD-17-0679
 * Panagopoulos I. et al., **PAN3–PSMA2 fusion resulting from a novel t(7;13)(p14;q12) chromosome translocation in a myelodysplastic syndrome that evolved into acute myeloid leukemia**, Experimental Hematology and Oncology, March 2018, https://doi.org/10.1186/s40164-018-0099-4
 * Alholle A. et al., **Genetic analyses of undifferentiated small round cell sarcoma identifies a novel sarcoma subtype with a recurrent CRTC1‐SS18 gene fusion, The Journal of Pathology, March 2018, https://doi.org/10.1002/path.5071
 * Agostini A. et al., **Identification of novel cyclin gene fusion transcripts in endometrioid ovarian carcinomas**, Internation Journal of Cancer, April 2018,  https://doi.org/10.1002/ijc.31418
 * Brunetti M. et al., **Identification of an EPC2-PHF1 fusion transcript in low-grade endometrial stromal sarcoma**, Oncotarget, April 2018, https://doi.org/10.18632/oncotarget.24969
 * Panagopoulos I. et al., **RUNX1-PDCD6 fusion resulting from a novel t(5;21)(p15;q22) chromosome translocation in myelodysplastic syndrome secondary to chronic lymphocytic leukemia**, PLOS One, April 2018, https://doi.org/10.1371/journal.pone.0196181
 * Bie D.J. et al., **Single-cell sequencing reveals the origin and the order of mutation acquisition in T-cell acute lymphoblastic leukemia**, Leukemia, April 2018, https://doi.org/10.1038/s41375-018-0127-8
 * Chiaretti S. et al., **Rapid identification of BCR/ABL1‐like acute lymphoblastic leukaemia patients using a predictive statistical model based on quantitative real time‐polymerase chain reaction: clinical, prognostic and therapeutic implications**, British Journal of Haematology, April 2018, https://doi.org/10.1111/bjh.15251
* Wang X.T. et al., **RNA sequencing of Xp11 translocation-associated cancers reveals novel gene fusions and distinctive clinicopathologic correlations**, Modern Pathology, April 2018, https://doi.org/10.1038/s41379-018-0051-5
* Churchman M.L. et al., **Germline Genetic IKZF1 Variation and Predisposition to Childhood Acute Lymphoblastic Leukemia**, Cancer Cell, May 2018, https://doi.org/10.1016/j.ccell.2018.03.021
* Knuuttila M. et al., **Intratumoral androgen levels are linked to TMPRSS2-ERG fusion in prostate cancer**, Endocrinology-related-Related Cancer, May 2018, doi: https://doi.org/10.1530/ERC-18-0148
* He H., et al., **Identification of a Recurrent LMO7–BRAF Fusion in Papillary Thyroid Carcinoma**, Thyroid, May 2018, https://doi.org/10.1089/thy.2017.0258
* Wang C. et al., **Whole-genome sequencing reveals genomic signatures associated with the inflammatory microenvironments in Chinese NSCLC patients**, Nature Communications, May 2018, https://doi.org/10.1038/s41467-018-04492-2 
* Parris T.Z. et al., **Genome-wide multi-omics profiling of the 8p11-p12 amplicon in breast carcinoma**, Oncotarget, May 2018, https://dx.doi.org/10.18632%2Foncotarget.25329
* Gioiosa S. et al., **Massive NGS Data Analysis Reveals Hundreds Of Potential Novel Gene Fusions in Human Cell Lines**, GigaScience, June 2018, https://doi.org/10.1093/gigascience/giy062
* Roberts, K.G. et al., **Genomic and outcome analyses of Ph-like ALL in NCI standard-risk patients: a report from the Children’s Oncology Group**, Blood, June 2018, https://doi.org/10.1182/blood-2018-04-841676
* Rosenberg S. et al., **A recurrent point mutation in PRKCA is a hallmark of chordoid gliomas**, Nature Communications, June 2018, https://doi.org/10.1038/s41467-018-04622-w
* Ganly I. et al., **Integrated Genomic Analysis of Hürthle Cell Cancer Reveals Oncogenic Drivers, Recurrent Mitochondrial Mutations, and Unique Chromosomal Landscapes**, Cancer Cell, August 2018, https://doi.org/10.1016/j.ccell.2018.07.002
* Wrzeszczynski K.O. et al., **Analytical Validation of Clinical Whole-Genome and Transcriptome Sequencing of Patient Derived Tumors Clinical Application of Whole-Genome Sequencing for Reporting Targetable Variants in Cancer**, The Journal of Molecular Diagnostics, Aug. 2018,  https://doi.org/10.1016/j.jmoldx.2018.06.007
* Hultsch S. et  al., **Association of tamoxifen resistance and lipid reprogramming in breast cancer**, BMC Cancer, Aug. 2018, https://doi.org/10.1186/s12885-018-4757-z
* Alexander T.B. et al., **The genetic basis and cell of origin of mixed phenotype acute leukaemia**, Nature, Sept. 2018, https://doi.org/10.1038/s41586-018-0436-0
* Al-Ibraheemi A. et al., **Aberrant receptor tyrosine kinase signaling in lipofibromatosis: a clinicopathological and molecular genetic study of 20 cases**, Modern Pathology, Oct. 2018, https://doi.org/10.1038/s41379-018-0150-3
* Engqvist H. et al., **Transcriptomic and genomic profiling of early-stage ovarian carcinomas associated with histotype and overall survival**, Oncotarget, Oct. 2018, https://doi.org/10.18632/oncotarget.26225
* Haider Z. et al., **An integrated transcriptome analysis in T‐cell acute lymphoblastic leukemia links DNA methylation subgroups to dysregulated TAL1 and ANTP homeobox gene expression**, Cancer Medicine, Dec. 2018, https://doi.org/10.1002/cam4.1917
* Sekimizu M. et al., **Frequent mutations of genes encoding vacuolar H+‐ATPase components in granular cell tumors**, Genes Chromosomes & Cancer, Dec. 2018, https://doi.org/10.1002/gcc.22727
* Troll C.J. et al., **Structural Variation Detection by Proximity Ligation from Formalin-Fixed, Paraffin-Embedded Tumor Tissue**, The journal of molecular diagnostic, Dec. 2018, https://doi.org/10.1016/j.jmoldx.2018.11.003
* Xiao W. et al., **PHF6 and DNMT3A mutations are enriched in distinct subgroups of mixed phenotype acute leukemia with T-lineage differentiation**, Blood Advances, Dec. 2018, https://doi.org/10.1182/bloodadvances.2018023531
* Diolaiti D. et al., **A recurrent novel MGA–NUTM1 fusion identifies a new subtype of high-grade spindle cell sarcoma**, Cold Spring Harbor Molecular Case Studies, Dec. 2018, https://doi.org/10.1101/mcs.a003194
* Dupain C. et al., **Discovery of New Fusion Transcripts in a Cohort of Pediatric Solid Cancers at Relapse and Relevance for Personalized Medicine**, Molecular Therapy, Jan. 2019, https://doi.org/10.1016/j.ymthe.2018.10.022
* Gu Z. et al., **PAX5-driven subtypes of B-progenitor acute lymphoblastic leukemia**, Nature Genetics, Jan. 2019, https://dx.doi.org/10.1038/s41588-018-0315-5
* Loarer F.L. et al., **Clinicopathologic Features of CIC-NUTM1 Sarcomas, a New Molecular Variant of the Family of CIC-Fused Sarcomas**, The American Journal of Surgical Pathology, Feb. 2019, https://dx.doi.org/10.1097/PAS.0000000000001187
* Piarulli  G. et al., **Gene fusion involving the insulin‐like growth factor 1 receptor in an ALK‐negative inflammatory myofibroblastic tumour**, Histopathology, Feb. 2019, https://doi.org/10.1111/his.13839
* Chen S. et al., **Widespread and Functional RNA Circularization in Localized Prostate Cancer**, Cell, Feb. 2019, https://doi.org/10.1016/j.cell.2019.01.025
* McNeer N.A. et al., **Genetic mechanisms of primary chemotherapy resistance in pediatric acute myeloid leukemia**, Leukemia, Feb. 2019, https://doi.org/10.1038/s41375-019-0402-3
* Fouchardiere A. et al., **B-Catenin nuclear expression discriminates deep penetrating nevi from other cutaneous melanocytic tumors**, Virchows Archiv, Feb. 2019, https://doi.org/10.1007/s00428-019-02533-9
* Huang D.W. et al., **RNA Sequencing in B-Cell Lymphomas**, Lymphoma, Feb. 2019, https://doi.org/10.1007/978-1-4939-9151-8_13
* Heyer E.E. et al., **Diagnosis of fusion genes using targeted RNA sequencing**, Nature Communications, March 2019, https://doi.org/10.1038/s41467-019-09374-9
* Ravi N. et al., **Identification of Targetable Lesions in Anaplastic Thyroid Cancer by Genome Profiling**, March 2019, https://doi.org/10.3390/cancers11030402
* Zhu C. et al., **The fusion landscape of hepatocellular carcinoma**, Molecular Oncology, April 2019, https://doi.org/10.1002/1878-0261.12479
* Schroeder M.P. et al., **Integrated analysis of relapsed B-cell precursor Acute Lymphoblastic Leukemia identifies subtype-specific cytokine and metabolic signatures**, Scientific Reports, March 2019, https://doi.org/10.1038/s41598-019-40786-1
* Bastian L. et al., **PAX5 biallelic genomic alterations define a novel subgroup of B-cell precursor acute lymphoblastic leukemia**, Leukemia, March 2019, https://doi.org/10.1038/s41375-019-0430-z
* Korshunov A. et al., **Desmoplastic/nodular medulloblastomas (DNMB) and medulloblastomas with extensive nodularity (MBEN) disclose similar epigenetic signatures but different transcriptional profiles**, Acta Neuropathologica, March 2019, https://doi.org/10.1007/s00401-019-01981-6
* Rampersaud E. et al., **Germline deletion of ETV6 in familial acute lymphoblastic leukemia**, Blood Advances, April 2019, https://doi.org/10.1182/bloodadvances.2018030635
* Zhang X.C. et al., **Comprehensive genomic and immunological characterization of Chinese non-small cell lung cancer patients**, Nature Communications, April 2019, http://dx.doi.org/10.1038/s41467-019-09762-1
* Yang W. et al., **Immunogenic neoantigens derived from gene fusions stimulate T cell responses**, Nature Medicine, Vol. 25, April 201, https://doi.org/10.1038/s41591-019-0434-2
* Frank M.O. et al., **Sequencing and curation strategies for identifying candidate glioblastoma treatments**, BMC Medical Genomics, April 2019, https://doi.org/10.1186/s12920-019-0500-0
* Yamazaki F. et al., **Novel NTRK3 Fusions in Fibrosarcomas of Adults**, The American Journal of Surgical Pathology, April 2019, https://doi.org/10.1097/PAS.0000000000001194
* Zhu D. et al., **The landscape of chimeric RNAs in bladder urothelial carcinoma**, The International Journal of Biochemistry and Cell Biology, May 2019, https://doi.org/10.1016/j.biocel.2019.02.007
* Troll C.J. et al., **Structural Variation Detection by Proximity Ligation from Formalin-Fixed, Paraffin-Embedded Tumor Tissue**, The Journal of Molecular Diagnostics, May 2019, https://doi.org/10.1016/j.jmoldx.2018.11.003
* Saba K.H. et al., **Genetic profiling of a chondroblastoma‐like osteosarcoma/malignant phosphaturic mesenchymal tumor of bone reveals a homozygous deletion of CDKN2A, intragenic deletion of DMD and a targetable FN1‐FGFR1 gene fusion**, Genes Chromosomes and Cancer, May 2019,  https://doi.org/10.1002/gcc.22764
* Panagopoulos I. et al., **Novel GTF2I–PDGFRB and IKZF1–TYW1 fusions in pediatric leukemia with normal karyotype**, Experimental Hematology & Oncology, May 2019, https://doi.org/10.1186/s40164-019-0136-y
* Trahair T. et al., **Crizotinib and Surgery for Long-Term Disease Control in Children and Adolescents With ALK-Positive Inflammatory Myofibroblastic Tumors**, JCO Precision Oncology, May 2019, https://doi.org/10.1200/PO.18.00297
* Blackburn J. et al., **TMPRSS2‐ERG fusions linked to prostate cancer racial health disparities: A focus on Africa**, Prostate, May 2019, https://doi.org/10.1002/pros.23823
* Yang B. et al., **Xp11 translocation renal cell carcinoma and clear cell renal cell carcinoma with TFE3 strong positive immunostaining: morphology, immunohistochemistry, and FISH analysis**, Modern Pathology, June 2019, https://doi.org/10.1038/s41379-019-0283-z
* Hynst J. et al., **Bioinformatic pipelines for whole transcriptome sequencing data exploitation in leukemia patients with complex structural variants**, PeerJ 7:e7071, June 2019, https://doi.org/10.7717/peerj.7071
* Makise N. et al., **Low-grade endometrial stromal sarcoma with a novel MEAF6-SUZ12 fusion**, Virchows Arch., June 2019, https://doi.org/10.1007/s00428-019-02588-8


---

# 4 - INSTALLATION AND USAGE EXAMPLES

## 4.1 - Automatic installation {#automatic-installation}

### 4.1.1 - Installation using boostrap.py

This is an example of automatic installation of *FusionCatcher* (and it is installed here "~/fusioncatcher" if these are run in your home directory) and the required databases and indexes (which are downloaded instead of being built locally):
```
wget http://sf.net/projects/fusioncatcher/files/bootstrap.py -O bootstrap.py && python bootstrap.py -t --download
```
where:
  * `wget http://sf.net/projects/fusioncatcher/files/bootstrap.py` downloads from internet the `bootstrap.py` which is the installation script (it is recommended to use the `boostrap.py` from `ttp://sf.net/projects/fusioncatcher/files/bootstrap.py` because it is more up to date)
  * `python bootstrap.py` runs using `python` the installation script `bootstrap.py` (here one may replace `python` with its own custom installation of python, like for example `/some/other/custom/python`)
  * `-t` installs the software tools (and their exact version) needed by *FusionCatcher*
  * `--download` forces the installation script `bootstrap.py` to download and install automatically also the databases needed by *FusionCatcher* (if this is not used the databases needed by *FusionCatcher* will not be installed and the user will have to build/install them manually later)

In case that there are several Python versions installed already then it is possible to point which one to use for installation and running *FusionCatcher*, as following (no required databases and indexes are installed automatically in this example):
```
wget http://sf.net/projects/fusioncatcher/files/bootstrap.py -O bootstrap.py

/some/other/python bootstrap.py
```

In case that one wants to install *FusionCatcher* here `/some/directory/fusioncatcher/`, then this shall be run (no required databases and indexes are installed automatically in this example):
```
wget http://sf.net/projects/fusioncatcher/files/bootstrap.py -O bootstrap.py

/your/favourite/python bootstrap.py --prefix=/some/directory/
```

In case that one wants to install *FusionCatcher* and download the databases directly and build locally the indexes, then this shall be run:
```
wget http://sf.net/projects/fusioncatcher/files/bootstrap.py -O bootstrap.py && python bootstrap.py --build
```

This is an example of automatic installation of *FusionCatcher* and the required databases and indexes (which are downloaded instead of being built locally) while all the questions asked by the installation script are answered automatically with YES (WARNING: this might overwrite files/directories):
```
wget http://sf.net/projects/fusioncatcher/files/bootstrap.py -O bootstrap.py && python bootstrap.py --download -y
```

In case that one has the admin/root rights then it is possible to install *FusionCatcher* as following (no required databases and indexes are installed automatically in this example):
```
wget http://sf.net/projects/fusioncatcher/files/bootstrap.py -O bootstrap.py
sudo python bootstrap.py
```

In case that one plans not to use at all BLAT with *FusionCatcher* then add the command line `-k` to the `boostrap.py`, as following:

```
python bootstrap.py -k
```

In case that you do not know which one to use from these examples, please use the first one!
Also, for more info about what options offered by `bootstrap.py`, please run
```
bootstrap.py --help
```

Please, do not forget to build/download the organism data after this is done running (please notice the last lines displayed by `bootstrap.py` after it finished running and execute the commands suggested there, e.g. use `download.sh`)!

### 4.1.2 - Installation using conda

FusionCatcher can be installed also using `conda`, as follows:
```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda create -n fusioncatcher fusioncatcher
```
After the environment is created, the next steps are:
```
source activate fusioncatcher
download-human-db.sh
```
and `conda` config will permanently add the three channels in the user `conda` config file.
Additionally, creating new and clean environment with `conda create` is recommended over using `conda install`.


### 4.1.3 - Installation from GitHub

```
git clone https://github.com/ndaniel/fusioncatcher
cd fusioncatcher/tools/
./install_tools.sh
cd ../data
./download-human-db.sh
```
**NOTE**: Here it is assumed that Python 2.7.x and BioPython are already installed.


## 4.2 - Manual installation {#manual-installation}

This is an example (or one of the many ways) for installing *FusionCatcher* on a **Ubuntu Linux 12.04/14.04 64-bit system** and the *FusionCatcher* and its dependencies are installed in `/apps`.

  * check that Python 2.6.X or 2.7.X is installed and working properly! If not then install it together with its development environment and other (probably) needed dependencies (required):
  ```
sudo apt-get install build-essential
sudo apt-get install libncurses5-dev
sudo apt-get install gawk
sudo apt-get install gcc
sudo apt-get install g++
sudo apt-get install make
sudo apt-get install automake
sudo apt-get install gzip
sudo apt-get install bzip2
sudo apt-get install cmake
sudo apt-get install zlib1g-dev
sudo apt-get install zlib1g
sudo apt-get install wget
sudo apt-get install curl
sudo apt-get install pigz
sudo apt-get install zip
sudo apt-get install tar
sudo apt-get install unzip
sudo apt-get install libc6-dev
sudo apt-get install default-jdk
sudo apt-get install libtbb-dev
sudo apt-get install libtbb2
sudo apt-get install parallel
sudo apt-get install python
sudo apt-get install python-dev
sudo apt-get install python-numpy
sudo apt-get install python-biopython
sudo apt-get install python-xlrd
sudo apt-get install python-openpyxl
  ```
  
  and for [RedHat](http://www.redhat.com)/[CentOS](http://www.centos.org) this would be required
  ```
sudo yum groupinstall "Development Tools"
sudo yum install ncurses-devel
sudo yum install awk
sudo yum install gcc
sudo yum install make
sudo yum install cmake
sudo yum install glibc-devel
sudo yum install zlib-devel
sudo yum install gzip
sudo yum install pigz
sudo yum install wget
sudo yum install curl
sudo yum install tbb-devel
sudo yum install python-devel
sudo yum install python-biopython
sudo yum install python-numpy
sudo yum install python-xlrd
sudo yum install python-openpyxl
sudo yum install java-1.8.0-openjdk* (or other Java?)
  ```
  
  and for [OpenSUSE](http://www.opensuse.org) this would be required
  ```
  sudo zypper in --type pattern Basis-Devel
  sudo zypper in gcc
  sudo zypper in ncurses-devel
  sudo zypper in python-devel
  sudo zypper in zlib-devel
  ```
  
  * installing **BioPython** (required):
  ```
  sudo apt-get install python-numpy
  sudo apt-get install python-biopython
  ```
  
  * installing Python module **xlrd** (optional):
  ```
  sudo apt-get install python-xlrd
  ```
  
  * installing Python module **openpyxl** (optional):
  ```
  sudo apt-get install python-openpyxl
  ```
  
  * create the needed directories:
  ```
  mkdir -p /apps/fusioncatcher/tools
  mkdir -p /apps/fusioncatcher/data
  ```
  
  * installing **Bowtie** 64-bit version 1.2.3 (required)
  ```
  cd /apps/fusioncatcher/tools
  wget https://github.com/BenLangmead/bowtie/releases/download/v1.2.3/bowtie-1.2.3-linux-x86_64.zip
  unzip bowtie-1.2.3-linux-x86_64.zip
  ln -s bowtie-1.2.3-linux-x86_64 bowtie
  ```
  
  * installing **Bowtie2** 64-bit version 2.3.5.1 (required)
  ```
  cd /apps/fusioncatcher/tools
  wget https://github.com/BenLangmead/bowtie2/releases/download/v2.3.5.1/bowtie2-2.3.5.1-linux-x86_64.zip
  unzip bowtie2-2.3.5.1-linux-x86_64.zip
  ln -s bowtie2-2.3.5.1-linux-x86_64 bowtie2
  ```
  
  * installing **BLAT** version 0.35 (optional; if **BLAT** is not installed please use option '--skip-blat' or remove the `blat` string from the `aligners =...` line of file `fusioncatcher/etc/configuration.cfg` in order to let know *FusionCatcher* that it should not use it)
  ```
  cd /apps/fusioncatcher/tools
  mkdir blat_v0.35
  cd blat_v0.35
  wget http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/blat/blat
  chmod +x blat
  wget http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/faToTwoBit
  chmod +x faToTwoBit
  wget http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/liftOver
  chmod +x liftOver
  cd ..
  ln -s blat_v0.35 blat
  ```
  
  * installing **fastq-dump** version 2.6.2 from **NCBI SRA Toolkit** version 2.6.2 (optional but it is required in case that one wants to test the installation using the example given below)
  ```
  cd /apps/fusioncatcher/tools
  wget http://ftp-private.ncbi.nlm.nih.gov/sra/sdk/2.9.6/sratoolkit.2.9.6-centos_linux64.tar.gz
  tar zxvf sratoolkit.2.9.6-centos_linux64.tar.gz
  ln -s sratoolkit.2.9.6-centos_linux64 sratoolkit
  ```
  
  * installing **SeqTK** version 1.0-r82b (please note that this is a different development branch than the official development) (required)
  ```
  cd /apps/fusioncatcher/tools
  wget http://github.com/ndaniel/seqtk/archive/1.0-r82b.tar.gz -O 1.0-r82b.tar.gz
  tar zxvf 1.0-r82b.tar.gz
  cd seqtk-1.0-r82b
  make
  cd ..
  ln -s seqtk-1.0-r82b seqtk
  ```
  
  * installing **fastqtk** version 0.27 (required)
  ```
  wget https://github.com/ndaniel/fastqtk/archive/v0.27.tar.gz -O v0.27.tar.gz --no-check-certificate
  tar --overwrite -xvzf v0.27.tar.gz -C .
  make -C fastqtk-0.27
  chmod +x fastqtk-0.27/fastqtk
  ln -s fastqtk-0.27 fastqtk
  ```
  
  * installing **STAR** version 2.7.2b (required)
  ```
  cd /apps/fusioncatcher/tools
  wget http://github.com/alexdobin/STAR/archive/2.7.2b.tar.gz -O 2.7.2b.tar.gz
  tar zxvf 2.7.2b.tar.gz
  cd 2.7.2b
  cd source
  rm -f STAR
  cp ../bin/Linux_x86_64_static/STAR .
  ```
  
  Try to run this command (if it fails please ignore the error messages and continue further; continue further either way)
  ```
  make
  ```
  
  and continue with
  ```
  cd ..
  ln -s 2.7.2b star
  ```
  
  * installing **Velvet** version 1.2.10 (optional)
  ```
  cd /apps/fusioncatcher/tools
  wget http://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.10.tgz
  tar zxvf velvet_1.2.10.tgz
  cd velvet_1.2.10
  make
  cd ..
  ln -s velvet_1.2.10 velvet
  ```
  > *Note*: Velvet depends on zlib-dev which may be installed like this
  ```
  sudo apt-get install zlib-dev
  ```
  
  * installing **coreutils** version 8.25 for a newer version of **sort** command which allows use of several CPUs in parallel, that is the use of `--parallel` command line option (optional)
  ```
  cd /apps/fusioncatcher/tools
  wget http://ftp.gnu.org/gnu/coreutils/coreutils-8.25.tar.xz
  tar --xz -xvf coreutils-8.25.tar.xz
  cd coreutils-8.25
  ./configure
  make
  cd ..
  ln -s coreutils-8.25 coreutils
  ```
  
  * installing **pigz** version 2.4 (optional)
  ```
  cd /apps/fusioncatcher/tools
  wget http://zlib.net/pigz/pigz-2.4.tar.gz
  tar zxvf pigz-2.3.1.tar.gz
  cd pigz-2.4
  make
  cd ..
  ln -s pigz-2.4 pigz
  ```
  
 
  * installing **Picard tools** version 2.2.2 (optional)
  ```
  cd /apps/fusioncatcher/tools
  mkdir picard
  cd picard
  wget http://github.com/broadinstitute/picard/releases/download/2.21.2/picard.jar
  cd ..
  ```
  
  * installing *FusionCatcher* version 1.20 (required)
  ```
  cd /apps/fusioncatcher
  wget http://sourceforge.net/projects/fusioncatcher/files/fusioncatcher_v1.20.zip
  unzip fusioncatcher_v1.20.zip
  cd fusioncatcher_v1.20
  
  rm -rf ../bin
  rm -rf ../etc
  rm -rf ../doc
  rm -rf ../VERSION
  rm -rf ../NEWS
  rm -rf ../LICENSE
  rm -rf ../README.md
  rm -rf ../DEPENDENCIES
  
  ln -s $(pwd)/bin ../bin
  ln -s $(pwd)/etc ../etc
  ln -s $(pwd)/doc ../doc
  ln -s $(pwd)/test ../test
  ln -s $(pwd)/VERSION ../VERSION
  ln -s $(pwd)/NEWS ../NEWS
  ln -s $(pwd)/LICENSE ../LICENSE
  ln -s $(pwd)/README.md ../README.md
  ln -s $(pwd)/DEPENDENCIES ../DEPENDENCIES
  ```
  
  * specify the paths to the above tools such that *FusionCatcher* can find them. There are two choices.
   * *Choice A*: Edit the *FusionCatcher* configuration file `configuration.cfg` (type: `nano /apps/fusioncatcher/etc/configuration.cfg` at command line), which has priority over `PATH`,  and make sure that the *FusionCatcher*'s configuration file **'configuration.cfg'** looks like this:
   ```
   [paths]
   python = /usr/bin/
   data = /apps/fusioncatcher/data/current/
   scripts = /apps/fusioncatcher/bin/
   bowtie = /apps/fusioncatcher/tools/bowtie/
   blat = /apps/fusioncatcher/tools/blat/
   bowtie2 = /apps/fusioncatcher/tools/bowtie2/
   star = /apps/fusioncatcher/tools/star/source/
   seqtk = /apps/fusioncatcher/tools/seqtk/
   fasttk = /apps/fusioncatcher/tools/fastqtk/
   velvet = /apps/fusioncatcher/tools/velvet/
   fatotwobit = /apps/fusioncatcher/tools/blat/
   liftover = /apps/fusioncatcher/tools/blat/
   sra = /apps/fusioncatcher/tools/sratoolkit/bin/
   numpy = /apps/fusioncatcher/tools/numpy/
   biopython = /apps/fusioncatcher/tools/biopython/
   xlrd = /apps/fusioncatcher/tools/xlrd/
   openpyxl = /apps/fusioncatcher/tools/openpyxl/
   fastqtk = /apps/fusioncatcher/tools/fastqtk/
   lzop = /apps/fusioncatcher/tools/lzop/src/
   coreutils = /apps/fusioncatcher/tools/coreutils/src/
   pigz = /apps/fusioncatcher/tools/pigz/
   samtools = /apps/fusioncatcher/tools/samtools/
   picard = /apps/fusioncatcher/tools/picard/
   parallel = /appsfusioncatcher/tools/paralell/src/
   bbmap = /apps/fusioncatcher/tools/bbmap/
   pxz = /apps/fusioncatcher/tools/pxz/
   java = /usr/bin/
   [parameters]
   threads = 0
   aligners = blat,star
   [versions]
   fusioncatcher = 1.33
   ```
   
   * *Choice B*: Add the paths for the needed tools to the `PATH` variable by editing, for example, the `.bashrc` file (type: `nano ~/.bashrc` at command line) and add the following lines at the end:
   ```
   export PATH=/apps/fusioncatcher/bin:$PATH
   export PATH=/apps/fusioncatcher/tools/bowtie:$PATH
   export PATH=/apps/fusioncatcher/tools/bowtie2:$PATH
   export PATH=/apps/fusioncatcher/tools/blat:$PATH
   export PATH=/apps/fusioncatcher/tools/star/source/:$PATH
   export PATH=/apps/fusioncatcher/tools/liftover:$PATH
   export PATH=/apps/fusioncatcher/tools/seqtk:$PATH
   export PATH=/apps/fusioncatcher/tools/fastqtk:$PATH
   export PATH=/apps/fusioncatcher/tools/sratoolkit/bin:$PATH
   export PATH=/apps/fusioncatcher/tools/velvet/:$PATH
   export PATH=/apps/fusioncatcher/tools/fatotwobit/:$PATH
   export PATH=/apps/fusioncatcher/tools/lzop/src/:$PATH
   export PATH=/apps/fusioncatcher/tools/coreutils/src/:$PATH
   export PATH=/apps/fusioncatcher/tools/pigz/:$PATH
   export PATH=/apps/fusioncatcher/tools/samtools/:$PATH
   export PATH=/apps/fusioncatcher/tools/bbmap/:$PATH
   export PATH=/apps/fusioncatcher/tools/picard/:$PATH
   ```
   
   > *Note 1*: If a different version of Python is used/needed by *FusionCatcher* than the standard `/usr/bin/env python` then also please make sure that that specific version of Python is added to the `PATH` variable by editing, for example, the `.bashrc` file (type: `nano ~/.bashrc` at command line) or add the following lines at the end:
   ```
   export PATH=/some/other/version/of/python:$PATH
   ```
   
   > *Note 2*: `fusioncatcher/etc/configuration.cfg` **has priority** over `$PATH`. 
   
   > *Note 3*: In some cases it might not be enough to change the Python's path in `.bashrc` file, like for example the case when *FusionCatcher* is run on a server which defaults to another Python than one used to install *FusionCatcher*. In this case it is required that one changes all the [shebangs](http://en.wikipedia.org/wiki/Shebang_(Unix)) of the all Python scripts which belong to *FusionCatcher*. In case that one uses the Python which has the following Python executable path `/some/other/python` than this can be done like this (it changes in place `/usr/bin/env python` into `/some/other/python` in all `/apps/fusioncatcher/bin/*.py`):
   ```
   sed -i 's/\/usr\/bin\/env\ python/\/some\/other\/python/g' /apps/fusioncatcher/bin/*.py
   ```
  
  * download/build the human build data from Ensembl database and other databases and build the necessary indexes and files (the latest release of Ensembl data is release 95 as March 2019 when this section was updated last time). There are two alternative ways to get the human **build data**. The recommended way is to use `fusioncatcher-build`.
   * Using direct download
   ```
   mkdir -p /apps/fusioncatcher/data
   cd /apps/fusioncatcher/data
   wget http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.aa
   wget http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ab
   wget http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ac
   wget http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ad
   cat human_v102.tar.gz.* | tar xz
   ln -s human_v102 current
   ```
   
   * Using `fusioncatcher-build` -- It will takes several hours (e.g. 5-10 hours) and it depends highly on the bandwidth of your internet connection. One may find out what Ensembl database version is available at [www.ensembl.org] and what version has been downloaded by looking to the last three lines printed on the screen by `fusioncatcher-build`.
   ```
   mkdir -p /apps/fusioncatcher/data/human_v102
   cd /apps/fusioncatcher/data/human_v102
   /apps/fusioncatcher/bin/fusioncatcher-build -g homo_sapiens -o .
   cd ..
   ln -s human_v102 current
   ```



## 4.3 - Semi-automatic installation

This is an example of semi-automatic installation of *FusionCatcher* (and it is installed here: `/some/server/apps/fusioncatcher`). This may be used when *FusionCatcher* should be installed on a computer without internet connection. Shortly, in this case all the software dependencies and indexes of databases need to be downloaded separately on another computer which has internet connection and from there they should be copied/moved to the computer without internet connection. Here are the steps for achieving these:

  * on computer A (which has internet connection):
   * create locally a folder named, for example, `fuscat`:
    ```
    mkdir fuscat
    cd fuscat
    ```
   * download `bootstrap.py`
    ```
    wget http://sf.net/projects/fusioncatcher/files/bootstrap.py
    ```
   * find out the dependencies needed to be downloaded and download them manually into folder `fuscat` (their URLs will be shown and the user needs to download them manually using wget or its favourite browser)
    ```
    python bootstrap.py --list-dependencies
    ...
    ```
   * copy/move (manually) the folder `fuscat` and all its content to computer B (which does not have internet connection) where one intends to install *FusionCatcher*
  * on the computer B (which does not have internet connection), where one intends to install *FusionCatcher*:
   * go to the folder `fuscat` and make sure that the downloaded files do **not** have their permissions set as executables (this might confuse `bootstrap.py`)
    ```
    cd fuscat
    chmod -x *
    ```
   * start the installing process of *FusionCatcher* using `bootstrap.py` (if one wishes to use another version of Python, like for example having the path `/some/other/python` then below please replace `python` with `/some/other/python`)
    ```
    python bootstrap.py --local .
    ```
   * for installing the pre-built index files for human, please run (or take a look for instructions to) `download.sh` (it should be in `bin` directory where *FusionCatcher* has been installed)
   * for installing the pre-built index files for other organisms than human please, use `fusioncatcher-build` according tot the manual

For more information regarding the installation settings and possibilities, run:
```
python bootstrap.py --help
```

## 4.4 - Testing installation

This test works only when human organism.

### 4.4.1 - Automatic

Here are the steps for testing the installation of *FusionCatcher* using human genome.
```
cd ~
/apps/fusioncatcher/test/test.sh
```
Afterwards a message will be shown at console if the installation test went fine or not.

### 4.4.1 - Manual

Here are the steps for testing the installation of *FusionCatcher* using human genome.

```
mkdir ~/test
cd ~/test

wget http://sourceforge.net/projects/fusioncatcher/files/test/reads_1.fq.gz
wget http://sourceforge.net/projects/fusioncatcher/files/test/reads_2.fq.gz

cd ..

/apps/fusioncatcher/bin/fusioncatcher \
-d /apps/fusioncatcher/data/current/ \
--input ~/test/ \
--output ~/test-results/
```

This should take around 5 minutes to run and the result file `~/test-results/final-list_candidates-fusion-genes.txt` should look like [this](http://sourceforge.net/projects/fusioncatcher/files/test/final-list_candidate-fusion-genes.txt).

This dataset contains a very small set of short reads covering 12 already known fusion genes from human tumor cell lines which have been RNA sequenced (for more see [here](http://sourceforge.net/projects/fusioncatcher/files/test/readme.txt)).

## 4.5 - Breast cancer cell line

This is an example of finding fusion genes in the BT474 cell line using the public available RNA-seq data (from SRA archive):
  * download the publicly available RNA-seq data for BT-474 tumor breast cell line published in article **H. Edgren, A. Murumagi, S. Kangaspeska, D. Nicorici, V. Hongisto, K. Kleivi, I.H. Rye, S. Nyberg, M. Wolf, A.L. Borresen-Dale, O.P. Kallioniemi, Identification of fusion genes in breast cancer by paired-end RNA-sequencing, Genome Biology, Vol. 12, Jan. 2011** http://genomebiology.com/2011/12/1/R6/ :
   ```
   mkdir -p ~/bt474
   cd ~/bt474
   wget http://ftp-private.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR064/SRR064438/SRR064438.sra
   wget http://ftp-private.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR064/SRR064439/SRR064439.sra
   ```
   
  * run *FusionCatcher* (it takes around ~2.5 hours):
   ```
   /apps/fusioncatcher/bin/fusioncatcher \
   -d /apps/fusioncatcher/data/current/ \
   -i ~/bt474/ \
   -o ~/bt474_fusions/
   ```
   
  * if the run was successful then there should be the (non-empty) files (for more information see [here](#output-data)):
   ```
   ~/bt474_fusions/final-list_candidate_fusion_genes.txt
   ~/bt474_fusions/summary_candidate_fusions.txt
   ~/bt474_fusions/viruses_bacteria_phages.txt
   ~/bt474_fusions/supporting-reads_gene-fusions_BOWTIE.zip
   ~/bt474_fusions/supporting-reads_gene-fusions_BLAT.zip
   ~/bt474_fusions/supporting-reads_gene-fusions_STAR.zip
   ~/bt474_fusions/info.txt
   ~/bt474_fusions/fusioncatcher.log
  ```
  
  and the file
  ```
  ~/bt474_fusions/final-list_candidate_fusion_genes.txt
  ```
  
  should contain almost all fusion genes which have been published here:
   * S. Kangaspeska, S. Hultsch, H. Edgren, D. Nicorici, A. Murumägi, O.P. Kallioniemi, Reanalysis of RNA-sequencing data reveals several additional fusion genes with multiple isoforms, PLOS One, Oct. 2012. http://dx.plos.org/10.1371/journal.pone.0048745
   * H. Edgren, A. Murumagi, S. Kangaspeska, D. Nicorici, V. Hongisto, K. Kleivi, I.H. Rye, S. Nyberg, M. Wolf, A.L. Borresen-Dale, O.P. Kallioniemi, Identification of fusion genes in breast cancer by paired-end RNA-sequencing, Genome Biology, Vol. 12, Jan. 2011. http://genomebiology.com/2011/12/1/R6

## 4.6 - Batch mode

This is an example of finding fusion genes in the [Illumina Body Map 2.0](http://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-513/) RNA-seq data which consists of 16 RNA samples from 16 different organs from healthy persons. For doing this the batch mode is used (where the input is [this file](http://sourceforge.net/projects/fusioncatcher/files/examples/illumina-bodymap2.txt)), as shown here:
```
mkdir -p ~/bodymap
cd ~/bodymap
wget http://sourceforge.net/projects/fusioncatcher/files/examples/illumina-bodymap2.txt
fusioncatcher-batch.py -i illumina-bodymap2.txt -o results
```
The input file for `fusioncatcher-batch.py` is a text tab-separated file with two columns and 16 lines (one line for each organ from Illumina Body Map 2.0). The first column contains the URLs for the input FASTQ files and the second column (which is optional) contains the name of the organ (which will be used to create a output directory later where the results will be). Therefore, *FusionCatcher* will be run automatically 16 times by the `fusioncatcher-batch.py`.

The fusion genes found in *Illumina Body Map 2.0* could be used later, for example, as a list of known false positives when looking for fusion genes in diseased/tumor samples.

## 4.7 - Matched normal sample

In case that there is available RNA-seq data from a tumor sample and its match normal sample then the somatic mode of *FusionCatcher* may be used.  By default *FusionCatcher* is using a background list of fusion genes which have been found previously in normal healthy samples (e.g. Illumina BodyMap2 , etc.).

For example, lets assume that (i) the BT-474 is the rumor sample from here, and (ii) the matched normal samples if the healthy breast sample from here.  In this case, in order to find the somatic fusion genes in the BT-474 (that are the fusion genes which are found in BT-474 and are not found in the healthy sample) *FusionCatcher* should be run as follows:

```
mkdir -p ~/bt474
cd ~/bt474
wget http://ftp-private.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR064/SRR064438/SRR064438.sra
wget http://ftp-private.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR064/SRR064439/SRR064439.sra


mkdir -p ~/healthy
cd ~/healthy
wget http://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR064/SRR064437/SRR064437.sra

cd ~

fusioncatcher.py
--input ~/bt474/
--normal ~/healthy
--output ~/results/
```

The somatic fusion genes for BT-474 will be found in `~/results/bt474/final-list_candidate_fusion_genes.txt` file. The fusion genes which marked as **matched-normal** (see column 3) in BT-474 (that is `~/results/bt474/final-list_candidate_fusion_genes.txt` file) have been found also in the healthy sample also and most likely they are not somatic.

In case that there are several tumor samples and their matched healthy samples then batch mode of *FusionCatcher* may be used, as follows:
```
fusioncatcher-batch.py
--input /some/path/tumor-file.txt
--normal /some/path/healthy-file.txt
--output /some/path/results/
```
where:
  * `/some/path/tumor-file.txt` is a text file containing on each line a path to FASTQ files belonging to the tumor cells (an example is [here](http://sourceforge.net/projects/fusioncatcher/files/examples/edgren.txt)),
  * `/some/path/healthy-file.txt` is a text file containing on each line a path to FASTQ files belonging to the healthy cells (an example is [here](http://sourceforge.net/projects/fusioncatcher/files/examples/illumina-bodymap2.txt)),
  * `/some/path/results` is the output directory where the results are placed.

## 4.8 - Edgren RNA-seq dataset

This is an example of finding fusion genes in the Edgren RNA-seq data (from SRA archive):
  * H. Edgren, A. Murumagi, S. Kangaspeska, D. Nicorici, V. Hongisto, K. Kleivi, I.H. Rye, S. Nyberg, M. Wolf, A.L. Borresen-Dale, O.P. Kallioniemi, **Identification of fusion genes in breast cancer by paired-end RNA-sequencing**, Genome Biology, Vol. 12, Jan. 2011. http://genomebiology.com/2011/12/1/R6
  * S. Kangaspeska, S. Hultsch, H. Edgren, D. Nicorici, A. Murumägi, O.P. Kallioniemi, **Reanalysis of RNA-sequencing data reveals several additional fusion genes with multiple isoforms**, PLOS One, Oct. 2012. http://dx.plos.org/10.1371/journal.pone.0048745
```
fusioncatcher-batch.py -i http://sourceforge.net/projects/fusioncatcher/files/examples/edgren.txt -o results/
```
NOTE: **DO NOT POOL** the samples from all these cell lines. **DO NOT** give at once all these SRA/FASTQ files as input to FusionCatcher! Run *FusionCatcher* separately for each cell line! It is ok the pool together the samples from the same cell line together (but still do not concatenate yourself the FASTQ files and let FusionCatcher do it for you)!


---


# 5 - QUICK INSTALLATION

## 5.1 - Getting executables

For a fully automatic installation (including the required indexes of databases) run:
```
wget http://sf.net/projects/fusioncatcher/files/bootstrap.py && python bootstrap.py --download
```

In case of a manual installation, first please check that (i) the required dependencies are installed, and (ii) download the source files of *FusionCatcher*, like for example:
```
wget http://sourceforge.net/projects/fusioncatcher/files/fusioncatcher_v1.20.zip 
unzip fusioncatcher_v1.20.zip
```

For an example of:
  * fully automatic installation see [here](#automatic-installation),
  * manual installation see [here](#manual-installation), and
  * semi-automatic installation see  [here](#manual-installation).

## 5.2 - Organism's build data

First, it is needed to download data or build the necessary files/indexes for running the *FusionCatcher*. This process should be done once for every single organism or every time when the [Ensembl](http://www.ensembl.org) database is updated.


### 5.2.1 - Direct download of human build data

Here, in this example, the necessary data is downloaded and necessary files/indexes for the **human genome** are downloaded in the directory `/some/human/data/human_v102/` which will be used later.

```
mkdir -p /some/human/data/
cd /some/human/data/
wget http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.aa
wget http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ab
wget http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ac
wget http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ad
cat human_v102.tar.gz.* | tar xz
ln -s human_v102 current
```

If this works then it is not necessary to start building yourself the build data as shown below (which is **only** needed in case that the direct download for some reason does not work or one wishes to use the build data of another organism which is not available for download).

### 5.2.2 - Building yourself the organism's build data

Here, in this example, the necessary data is downloaded and necessary files/indexes are built for the **human genome** in the directory `/some/human/data/directory/` which will be used later.
```
fusioncatcher-build -g homo_sapiens -o /some/human/data/directory/
```
This takes around 5-10 hours (downloading, building indexes/databases, etc.).

In case that one wants to use a Ensembl server which is situated geographically closer, then one has:
  * Ensembl server in Europe (used by default):
```
fusioncatcher-build -g homo_sapiens -o /some/human/data/directory/
```
  * Ensembl server in East US:
```
fusioncatcher-build -g homo_sapiens -o /some/human/data/directory/ --web=useast.ensembl.org
```
  * Ensembl server in West US:
```
fusioncatcher-build -g homo_sapiens -o /some/human/data/directory/ --web=uswest.ensembl.org
```
  * Ensembl server in Asia:
```
fusioncatcher-build -g homo_sapiens -o /some/human/data/directory/ --web=asia.ensembl.org
```


In case, that it is not possible to use `fusioncatcher-build` for vary reasons (e.g. access to Ensembl website is very slow) then one may directly download the latest **human build data** (generated by `fusioncatcher-build` using Ensembl database release 95) necessary for running *FusionCatcher* from [here](http://sourceforge.net/projects/fusioncatcher/files/data/) (all files are needed and the total size is ~25 GB).

For rat genome, one has
```
fusioncatcher-build -g rattus_norvegicus -o /some/rat/data/directory/
```

For mouse genome, one has
```
fusioncatcher-build -g mus_musculus -o /some/mouse/data/directory/
```

**NOTE**: *FusionCatcher* version 1.33 needs a newer **build data** than the previous version (that is 1.10) of 'fusioncatcher-build'.

---


# 6 - USAGE

Searching for fusion genes in a human organism, one has:
```
fusioncatcher \
-d /some/human/data/directory/ \
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/
```
where:
  * `/some/human/data/directory/` - contains the data and files generated by `fusioncatcher-build` (see [Get data](#output-data) section)
  * `/some/input/directory/containing/fastq/files/` - contains the input FASTQ (or SRA if NCBI SRA toolkit is installed) files (and not any other type of files which are not do not contain sequecing data, e.g. readme.txt)
  * `/some/output/directory/` - contains output files (for more information see [here](#output-data)):
    * `final-list_candidate_fusion_genes.txt`
    * `summary_candidate_fusions.txt`
    * `supporting-reads_gene-fusions_BOWTIE.zip`
    * `supporting-reads_gene-fusions_BLAT.zip`
    * `supporting-reads_gene-fusions_STAR.zip`
    * `viruses_bacteria_phages.txt`
    * `info.txt`
    * `fusioncatcher.log`

Searching for fusion genes in a rat organism, one has:
```
fusioncatcher \
-d /some/rat/data/directory/ \
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/
```

Searching for fusion genes in a mouse organism, one has:
```
fusioncatcher \
-d /some/mouse/data/directory/ \
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/
```



## 6.1 - Input data

The input data shall be:
  * a directory containing the input FASTQ/SRA files (this is highly recommended), or
  * several files separated by comma, e.g. `file01.fq,file02.fq` (there should be no blank before and after the comma!).

All types of raw FASTQ files produced by the Illumina Solexa and Illumina HiSeq platforms containing **paired-end** reads may be given as input. The FASTQ files shall:
  * come from an **RNA** sequencing experiment (i.e. the transcriptome/RNA is sequenced), and
  * contain **paired-end** reads, and
  * paired FASTQ files should be synchronized (i.e. reads which for a pair should be on the same line number if both FASTQ files).
  * paired-end reads which follow the suggested Illumina's sample preparation protocol, that is the two read-mates are: (i) from opposite strands, and (ii) opposite directions to one another (in other words, in order to 'bring' a read and its mate-read on the same strand then one needs to perform reverse-complement operation on only one of them)
  * paired-end reads shall come from a **stranded** (i.e. strand-specific) or **unstranded** sample preparation protocol (both are supported by *FusionCatcher*)!


It is **highly recommended** that:
  * the input FASTQ files contain the **raw** reads generated by the Illumina sequencers **without any additional trimming** (i.e. all reads from all files shall have the same length), and
  * every single input FASTQ file contains reads from only and only **one** sample/replicate (i.e. **do not concatenate** in one big FASTQ file several other FASTQ files; just give the input all FASTQ files and *FusionCatcher* will do the concatenation).

*FusionCatcher* will automatically pre-process the input reads, as follows:
  * trimming 3' end of the reads based on quality scores (default Q5),
  * removing automatically the adapter from the reads (it predicts the adapter sequence based on the reads which form a pair and also overlap and the non-overlapping parts are the predicted adapters),
  * trimming the poly A/C/G/T tails,
  * removing the reads which contain short tandem repeats (see: M. Gymrek, et al. lobSTR: A short tandem repeat profiler for personal genomes, Genome Res. 2012 Jun;22(6):1154-62, here http://genome.cshlp.org/content/22/6/1154.abstract ,
  * removing the reads which are marked as bad by Illumina sequencer,
  * removing the reads which are too short after the trimming,
  * removing the reads which map on ribosomal RNA,
  * removing the reads which map on genomes of bacteria/phages/viruses (from: [ftp://ftp.ncbi.nlm.nih.gov/genomes/Viruses/](ftp://ftp.ncbi.nlm.nih.gov/genomes/Viruses/) ).

Note: If the reads contains barcode sequences then they should be removed before given as inputs to *FusionCatcher*.

The SRA files are accepted as input as long as the NCBI SRA toolkit (see dependencies section) is installed and available.

The following files are accepted/used as input:
  * `*.fq.zip`
  * `*.fq.gz`
  * `*.fq.bz2`
  * `*.fastq.zip`
  * `*.fastq.gz`
  * `*.fastq.bz2`
  * `*.txt.zip`
  * `*.txt.gz`
  * `*.txt.bz2`
  * `*.fq`
  * `*.fastq`
  * `*.sra`
and the `zip` and `gz` archives should contain only one file.

*FusionCatcher* also accepts as input also URLs (it shall start with ftp:// or http://), like for example
```
fusioncatcher -i ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR030/ERR030872/ERR030872_1.fastq.gz,ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR030/ERR030872/ERR030872_2.fastq.gz -o thyroid
```

The FASTQ input files should be the ones generated by the Illumina platform without any kind of additional processing/filtering/trimming. *FusionCatcher* is doing its own filtering (automatically identifies and trims the adapters, trimming if needed, quality filtering of reads, removal of rRNA reads, etc.).

*FusionCatcher* is using the file names of the input files in order to figure out which files are paired (which contains ´[R1](https://code.google.com/p/FusionCatcher/source/detail?r=1)´ reads and which contains the corresponding ´[R2](https://code.google.com/p/FusionCatcher/source/detail?r=2)´ reads). For this *FusionCatcher* is ordering alphabetically the file names (found in a input directory) and it considers that the first two form a pair, the next two are forming a pair and so on. Shortly, here the first two files, the next two files and so on should be synchronized. For example, considering the following input files:
```
L002_R1.fastq.gz
L002_R2.fastq.gz
L003_R1.fastq.gz
L003_R2.fastq.gz
```
*FusionCatcher* would automatically figure out correctly that the first two files form a pair and the next two would form another pair.

There are cases when ordering alphabetically the input file names would make *FusionCatcher* to pair wrongly the input files (i.e. the input FASTQ files are not synchronized). In this kind of cases, renaming the input files such that they fit this rule helps. For example, considering the following input files (where the file containing ´[R1](https://code.google.com/p/FusionCatcher/source/detail?r=1)´ reads is split into two files and the file containing ´[R2](https://code.google.com/p/FusionCatcher/source/detail?r=2)´ reads is split into another two files):
```
L002_R1_01.fastq.gz
L002_R1_02.fastq.gz
L002_R2_01.fastq.gz
L002_R2_02.fastq.gz
```
*FusionCatcher* would automatically figure out **wrongly** that the first two files form a pair and the next two would form another pair. In this case, renaming the files like this
```
mv L002_R1_01.fastq.gz 01_L002_R1_01.fastq.gz 
mv L002_R1_02.fastq.gz 03_L002_R1_02.fastq.gz 
mv L002_R2_01.fastq.gz 02_L002_R2_01.fastq.gz 
mv L002_R2_02.fastq.gz 04_L002_R2_02.fastq.gz 
```
would give this alphabetically order list:
```
01_L002_R1_01.fastq.gz
02_L002_R2_01.fastq.gz
03_L002_R1_02.fastq.gz
04_L002_R2_02.fastq.gz
```
and with this input files *FusionCatcher* would work correctly. Another way, around this would be to give the input files separated by comma (in the correct order and no blanks before and after the comma), like this
```
fusioncatcher -i L002_R1_01.fastq.gz,L002_R2_01.fastq.gz,L002_R1_02.fastq.gz,L002_R2_02.fastq.gz 
```

For example, this is a valid input:
```
01_L002_R1_01.fastq.gz
02_L002_R2_01.fastq.gz
03_L002_R1_02.fastq.gz
04_L002_R2_02.fastq.gz
05_L002_R1_03.fastq.gz
06_L002_R2_03.fastq.gz
07_L002_R1_04.fastq.gz
08_L002_R2_04.fastq.gz
09_L002_R1_05.fastq.gz
10_L002_R2_05.fastq.gz
11_L002_R1_06.fastq.gz
12_L002_R2_06.fastq.gz
```

For example, this is **NOT** a valid input:
```
10_L002_R2_05.fastq.gz
11_L002_R1_06.fastq.gz
12_L002_R2_06.fastq.gz
1_L002_R1_01.fastq.gz
2_L002_R2_01.fastq.gz
3_L002_R1_02.fastq.gz
4_L002_R2_02.fastq.gz
5_L002_R1_03.fastq.gz
6_L002_R2_03.fastq.gz
7_L002_R1_04.fastq.gz
8_L002_R2_04.fastq.gz
9_L002_R1_05.fastq.gz
```


**NOTE:**
  * In case that a directory is given as input, one shall make sure that the input directory does not contain files which do not contain reads sequences (e.g. readme.txt, info.txt, etc.)!
  * Please, let *FusionCatcher* _do_ the the concatenation of several FASTQ files (i.e. just put all the FASTQ files into one folder and give that folder as input to *FusionCatcher*) and do NOT do concatenate the FASTQ files yourself (e.g. using `cat`). This is because most likely different FASTQ files might have:
   * different adapter sequences (*FusionCatcher* is expecting that there are only one type of adapter, exactly like it comes directly from the Illumina sequencers),
   * *FusionCatcher* does not support the FASTQ files where the reads' sequences contain barcode sequences (the barcode sequences shoud be removed/trimmed first and only then the trimmed FASTQ file should be given as input to *FusionCatcher*)
   * different fragment sizes, and
   * different read lengths.
  * **DO NOT POOL** samples from different cell lines or from different patients! Run FusionCatcher separately with one sample at the time! It is ok the pool together the samples, which come from the (i) same cell line, or (ii) from the same patient (but still do not concatenate yourself the FASTQ files and let FusionCatcher do it for you)!

## 6.2 - Output data {#output-data}

*FusionCatcher* produces a list of candidate fusion genes using the given input data. It is recommended that this list of candidate of fusion genes is further validated in the wet-lab using for example PCR/FISH experiments.

The output files are:
  * `final-list_candidate_fusion_genes.txt` - final list with the newly found candidates fusion genes (it contains the fusion genes with their junction sequence and points); Starting with version 0.99.3c the coordinates of fusion genes are given here for human genome using **only** assembly **hg38/GRCh38**; See [Table 1](#output-data) for columns' descriptions;
  * `final-list_candidate_fusion_genes.hg19.txt` - final list with the newly found candidates fusion genes (it contains the fusion genes with their junction sequence and points); Starting with version 0.99.3d the coordinates of fusion genes are given here for human genome using assembly **hg19/GRCh37**; See [Table 1](#output-data) for columns' descriptions;
  * `summary_candidate_fusions.txt` - contains an executive summary (meant to be read directly by the medical doctors or biologist) of candidate fusion genes found;
  * `final-list_candidate_fusion_genes.caption.md.txt` - explains in detail the labels found in column `Fusion_description` of files `final-list_candidate_fusion_genes.txt` and `final-list_candidate_fusion_genes.hg19.txt`;
  * `supporting-reads_gene-fusions_BOWTIE.zip` - sequences of short reads supporting the newly found candidate fusion genes found using only and exclusively the Bowtie aligner;
  * `supporting-reads_gene-fusions_BLAT.zip` - sequences of short reads supporting the newly found candidate fusion genes found using Bowtie and Blat aligners;
  * `supporting-reads_gene-fusions_STAR.zip` - sequences of short reads supporting the newly found candidate fusion genes found using Bowtie and STAR aligners;
  * `supporting-reads_gene-fusions_BOWTIE2.zip` - sequences of short reads supporting the newly found candidate fusion genes found using Bowtie and Bowtie2 aligners;
  * `viruses_bacteria_phages.txt` - (non-zero) reads counts for each virus/bacteria/phage from NCBI database  ftp://ftp.ncbi.nlm.nih.gov/genomes/Viruses/ 
  * `info.txt` - information regarding genome version, Ensembl database version, versions of tools used, read counts, etc.;
  * `fusioncatcher.log` -  log of the entire run (e.g. all commands/programs which have been run, command line arguments used, running time for each command, etc.).


FusionCatcher reports:
 * **multiple times** (up to four times) exactly the same candidate fusion gene, which has exactly the same fusion points/junction (i.e. FusionCatcher will output separately the fusions found for each of its four aligners/methods such that it is easy to see what method was used to find a fusion gene)
 * [reciprocal fusion genes](href='http://www.ncbi.nlm.nih.gov/pubmed/23340173) if they are found (e.g. geneA-geneB and also geneB-geneA)
 * every alternative splicing event found for each fusion gene (i.e. alternative fusion isoforms of the same fusion gene)


Table 1 - Columns description for file `final-list_candidate-fusion-genes.txt`

| **Column** | **Description** |
|:-----------|:----------------|
| **Gene\_1\_symbol(5end\_fusion\_partner)** | Gene symbol of the 5' end fusion partner |
| **Gene\_2\_symbol\_2(3end\_fusion\_partner)** | Gene symbol of the 3' end fusion partner |
| **Gene\_1\_id(5end\_fusion\_partner)** | Ensembl gene id of the 5' end fusion partner |
| **Gene\_2\_id(3end\_fusion\_partner)** | Ensembl gene id of the 3' end fusion partner |
| **Exon\_1\_id(5end\_fusion\_partner)** | Ensembl exon id of the 5' end fusion exon-exon junction |
| **Exon\_2\_id(3end\_fusion\_partner)** | Ensembl exon id of the 3' end fusion exon-exon junction |
| **Fusion\_point\_for\_gene\_1(5end\_fusion\_partner)** | Chromosomal position of the 5' end of fusion junction (chromosome:position:strand); 1-based coordinate |
| **Fusion\_point\_for\_gene\_2(3end\_fusion\_partner)** | Chromosomal position of the 3' end of fusion junction (chromosome:position:strand); 1-based coordinate |
| **Spanning\_pairs** | Count of pairs of reads supporting the fusion (**including** also the multimapping reads) |
| **Spanning\_unique\_reads** | Count of unique reads (i.e. unique mapping positions) mapping on the fusion junction. Shortly, here are counted all the reads which map on fusion junction minus the PCR duplicated reads. |
| **Longest\_anchor\_found** | Longest anchor (hangover) found among the unique reads mapping on the fusion junction |
| **Fusion\_finding\_method** | Aligning method used for mapping the reads and finding the fusion genes. Here are two methods used which are: (i) **BOWTIE** = only Bowtie aligner is used for mapping the reads on the genome and exon-exon fusion junctions, (ii) **BOWTIE+BLAT** = Bowtie aligner is used for mapping reads on the genome and BLAT is used for mapping reads for finding the fusion junction,  (iii) **BOWTIE+STAR** = Bowtie aligner is used for mapping reads on the genome and STAR is used for mapping reads for finding the fusion junction, (iv) **BOWTIE+BOWTIE2** = Bowtie aligner is used for mapping reads on the genome and Bowtie2 is used for mapping reads for finding the fusion junction. |
| **Fusion\_sequence** | The inferred fusion junction (the asterisk sign marks the junction point) |
| **Fusion\_description** | Type of the fusion gene (see the Table 2) |
| **Counts\_of\_common\_mapping\_reads** | Count of reads mapping simultaneously on both genes which form the fusion gene. This is an indication how similar are the DNA/RNA sequences of the genes forming the fusion gene (i.e. what is their homology because highly homologous genes tend to appear show as candidate fusion genes). In case of completely different sequences of the genes involved in forming a fusion gene then here it is expected to have the value zero. |
| **Predicted\_effect** | Predicted effect of the candidate fusion gene using the annotation from Ensembl database. This is shown in format **effect\_gene\_1**/**effect\_gene\_2**, where the possible values for effect\_gene\_1 or effect\_gene\_2 are: **intergenic**, **intronic**, **exonic(no-known-CDS)**, **UTR**, **CDS(not-reliable-start-or-end)**, **CDS(truncated)**, or **CDS(complete)**. In case that the fusion junction for both genes is within their CDS (coding sequence) then only the values **in-frame** or **out-of-frame** will be shown. |
| **Predicted\_fused\_transcripts** | All possible known fused transcripts in format ENSEMBL-TRANSCRIPT-1:POSITION-1/ENSEMBLE-TRANSCRIPT-B:POSITION-2, where are fused the sequence 1:POSITION-1 of transcript ENSEMBL-TRANSCRIPT-1 with sequence POSITION-2:END of transcript ENSEMBL-TRANSCRIPT-2 |
| **Predicted\_fused\_proteins** | Predicted amino acid sequences of all possible fused proteins (separated by ";").  |

Table 2 - Labels used to describe the found fusion genes (column *Fusion\_ description* from file `final-list_candidate-fusion-genes.txt`)

| **Fusion\_description** | **Description** |
|:------------------------|:----------------|
| **1000genomes**             | fusion gene has been seen in a healthy sample. It has been found in [RNA-seq data from some samples from 1000 genomes project](http://dx.doi.org/10.1371/journal.pone.0104567). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **18cancers**              | fusion gene found in a RNA-seq dataset of 18 types of cancers from 600 tumor samples published [here](http://dx.doi.org/10.1073/pnas.1606220113). |
| **adjacent**           | both genes forming the fusion are adjacent on the genome (i.e. same strand and there is no other genes situated between them on the same strand)|
| **antisense**           | one or both genes is a gene coding for [antisense RNA](http://en.wikipedia.org/wiki/Antisense_RNA)|
| **banned**              | fusion gene is on a list of known false positive fusion genes. These were found with very strong supporting data in healthy samples (i.e. it showed up in file final-list\_candidate\_fusion\_genes.txt). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **bodymap2**            | fusion gene is on a list of known false positive fusion genes. It has been found in healthy human samples collected from 16 organs from  [Illumina BodyMap2 RNA-seq database](http://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-513/). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **cacg**                | known conjoined genes (that is fusion genes found in samples from healthy patients) from the [CACG](http://cgc.kribb.re.kr/map/) database (please see CACG database for more information). *A candidate fusion gene having this label has a very high probability of being a false positive in case that one looks for fusion genes specific to a disease.*|
| **cell\_lines**         | known fusion gene from paper: C. Klijn et al., A comprehensive transcriptional portrait of human cancer cell lines, Nature Biotechnology, Dec. 2014, [DOI:10.1038/nbt.3080](http://dx.doi.org/10.1038/nbt.3080) |
| **ccle**         | known fusion gene found in human cancer cell lines that are in CCLE (Cancer Cell Line Encyclopedia); known fusions from [DepMap portal](https://depmap.org/portal/download/) |
| **ccle3**         | known fusion gene found in human cancer cell lines that are in CCLE (Cancer Cell Line Encyclopedia); known fusions from from paper: Vellichirammal et al., Pan-Cancer Analysis Reveals the Diverse Landscape of Novel Sense and Antisense Fusion Transcripts,  Mol. Ther. Nucleic Acids, 2020, [DOI:10.1016/j.omtn.2020.01.023](https://doi.org/10.1016/j.omtn.2020.01.023) |
| **cgp**                 | known fusion gene from the [CGP](http://www.sanger.ac.uk/genetics/CGP/Census/) database |
| **chimerdb2**           | known fusion gene from the [ChimerDB 2](http://ercsb.ewha.ac.kr/FusionGene/) database|
| **chimerdb3kb**           | known fusion gene from the [ChimerDB 3 KB (literature curration)](http://ercsb.ewha.ac.kr/FusionGene/) database |
| **chimerdb3pub**           | known fusion gene from the [ChimerDB 3 PUB (PubMed articles)](http://ercsb.ewha.ac.kr/FusionGene/) database |
| **chimerdb3seq**           | known fusion gene from the [ChimerDB 3 SEQ (TCGA)](http://ercsb.ewha.ac.kr/FusionGene/) database |
| **conjoing**            | known conjoined genes (that is fusion genes found in samples from healthy patients) from the [ConjoinG](http://metasystems.riken.jp/conjoing/) database (please use ConjoinG database for more information regarding the fusion gene). *A candidate fusion gene having this label has a very high probability of being a false positive in case that one looks for fusion genes specific to a disease.* |
| **cortex**            | fusion gene is on a list of known false positive fusion genes. It has been found in healthy human brains (BA9 prefrontal cortex) [here](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM1679648). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **cosmic**              | known fusion gene from the [COSMIC](http://cancer.sanger.ac.uk/cancergenome/projects/cosmic/) database (please use COSMIC database for more information regarding the fusion gene) |
| **distance1000bp**      | both genes are on the same strand and they are less than 1 000 bp apart. *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **distance100kbp**      | both genes are on the same strand and they are less than 100 000 bp apart. *A candidate fusion gene having this label has a higher probability than expected of being a false positive.* |
| **distance10kbp**       | both genes are on the same strand and they are less than 10 000 bp apart. *A candidate fusion gene having this label has a higher probability than expected of being a false positive.* |
| **duplicates**          | both genes involved in the fusion gene are [paralog](http://en.wikipedia.org/wiki/Paralog#Paralogy) for each other. For more see [Duplicated Genes Database (DGD) database](http://dgd.genouest.org/) . *A candidate fusion gene having this label has a higher probability than expected of being a false positive.* |
| **exon-exon**          | the fusion junction point is exactly at the known exon's borders of both genes forming the candidate fusion |
| **ensembl\_fully\_overlapping** | the genes forming the fusion gene are fully overlapping according to Ensembl database. *A candidate fusion gene having this label has a very high probability of being a false positive.*|
| **ensembl\_partially\_overlapping** | the genes forming the fusion gene are partially overlapping (on same strand or on different strands) according the Ensembl database. *A candidate fusion gene having this label has a good probability of being a false positive.</i> </font> |
| **ensembl\_same\_strand\_overlapping** | the genes forming the fusion gene are fully/partially overlapping and are both on the same strand according to Ensembl database. *A candidate fusion gene having this label has a very high probability of being a false positive (this is most likely and alternative splicing event).</i> </font> |
| **fragments** | the genes forming the fusion are supported by only and only one fragment of RNA. *A candidate fusion gene having this label has a medium probability of being a false positive.*|
| **gliomas**              | fusion gene found in a RNA-seq dataset of 272 glioblastoms published [here](http://dx.doi.org/10.1101/gr.165126.113). |
| **gtex**             | fusion gene has been seen in a healthy sample. It has been found in [GTEx database](http://www.gtexportal.org/home/) of healthy tissues (thru [FusionAnnotator](https://github.com/FusionAnnotator/FusionAnnotator)). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **healthy**             | fusion gene has been seen in a healthy sample. These have been found in healthy samples but the support for them is less strong (i.e. paired reads were found to map on both genes but no fusion junction was found) than in the case of **banned** label (i.e. it showed up in file preliminary list of candidate fusion genes). Also genes which have some degree of sequence similarity may show up marked like this.*A candidate fusion gene having this label has a small probability of being a false positive in case that one looks for fusion genes specific to a disease.* |
| **hpa**             | fusion gene has been seen in a healthy sample. It has been found in [RNA-seq database of 27 healthy tissues](http://dx.doi.org/10.1074/mcp.M113.035600). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **known**       | fusion gene which has been previously reported or published in scientific articles/reports/books/abstracts/databases indexed by [Google](http://www.google.com/), [Google Scholar](http://scholar.google.com/), [PubMed](http://www.ncbi.nlm.nih.gov/pubmed), etc. This label has only the role to answer with YES or NO the question "has ever before a given (candidate) fusion gene been published or reported?". This label does not have in anyway the role to provide the original references to the original scientific articles/reports/books/abstracts/databases for a given fusion gene. |
| **lincrna**             | one or both genes is a [lincRNA](http://en.wikipedia.org/wiki/Long_non-coding_RNA) |
| **matched-normal**      | candidate fusion gene (which is supported by paired reads mapping on both genes and also by reads mapping on the junction point) was found also in the matched normal sample given as input to the command line option '--normal' |
| **metazoa**             | one or both genes is a metazoa\_srp gene [Metazia\_srp](http://www.genecards.org/index.php?path=/Search/keyword/metazoa_srp) |
| **mirna**               | one or both genes is a [miRNA](http://en.wikipedia.org/wiki/MicroRNA) |
| **mt**                  | one or both genes are situated on [mitochondrion](http://en.wikipedia.org/wiki/Mitochondrion). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **mX** (where X is a number) | count of pairs of reads supporting the fusion (**excluding** the mutimapping reads). |
| **m0** | There are no pairs of non-multi-mapping reads supporting the fusion. Basically, there are supporting pairs of reads but all of them map also in some other places on genome (that is their mappings on genome are not unique). |
| **non\_cancer\_tissues**   | fusion gene which has been previously reported/found in non-cancer tissues and cell lines in [Babiceanu et al, Recurrent chimeric fusion RNAs in non-cancer tissues and cells, Nucl. Acids Res. 2016](http://nar.oxfordjournals.org/content/early/2016/02/01/nar.gkw032.abstract). These are considered as non-somatic mutation and therefore they may be skipped and not reported. |
| **non\_tumor\_cells**   | fusion gene which has been previously reported/found in non-tumor cell lines, like for example HEK293. These are considered as non-somatic mutation and therefore may be skipped and not reported. |
| **no\_protein** | one or both genes have no known protein product |
| **oesophagus**              | fusion gene found in a oesophageal tumors from TCGA samples, which are published [here](http://dx.doi.org/10.1038/nature20805). |
| **oncogene**            | one gene or both genes are a known [oncogene](http://en.wikipedia.org/wiki/Oncogene) according to [ONGENE database](https://doi.org/10.1016/j.jgg.2016.12.004) |
| **cancer**            | one gene or both genes are cancer associated according to [Cancer Gene database](http://www.bushmanlab.org/links/genelists) |
| **tumor**            | one gene or both genes are proto-oncogene or tumor suppresor gene according to [UniProt database](http://www.uniprot.org) |
| **short\_repeats** | the sequence of the fusion junction contains a highly repetitive region containing repeating short sequences or polyA/C/G/T (detected using kmer = 2) . *A candidate fusion gene having this label has a good probability of being a false positive.</i> </font> |
| **long\_repeats** | the sequence of the fusion junction contains a highly repetitive region containing repeating long sequences or polyA/C/G/T (detected using kmer = 9) . *A candidate fusion gene having this label has a good probability of being a false positive.</i> </font> |
| **pair\_pseudo\_genes** | one gene is the other's [pseudogene](http://en.wikipedia.org/wiki/Pseudogene). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **pancreases**           | known fusion gene found in pancreatic tumors from article: P. Bailey et al., Genomic analyses identify molecular subtypes of pancreatic cancer, Nature, Feb. 2016, http://dx.doi.org/110.1038/nature16965 |
| **paralogs**            | both genes involved in the fusion gene are  [paralog](http://en.wikipedia.org/wiki/Paralog#Paralogy) for each other (most likely this is a false positive fusion gene). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **multi**            | one of the genes of both have multi-mapping reads mapping (which map simultaneously also on other gene/genes |
| **partial-matched-normal** | candidate fusion gene (which is supported by paired reads mapping on both genes **but** _no_ reads were found which map on the junction point) was found also in the matched normal sample given as input to the command line option '--normal'. This is much weaker than **matched-normal**. |
| **prostates**           | known fusion gene found in 150 prostate tumors RNAs from paper: D. Robison et al, Integrative Clinical Genomics of Advanced Prostate Cancer, Cell, Vol. 161, May 2015, http://dx.doi.org/10.1016/j.cell.2015.05.001 |
| **pseudogene**          | one or both of the genes is a [pseudogene](http://en.wikipedia.org/wiki/Pseudogene) |
| **readthrough**         | the fusion gene is a readthrough event (that is both genes forming the fusion are on the same strand and there is no known gene situated in between); Please notice, that many of readthrough fusion genes might be false positive fusion genes due to errors in Ensembl database annotation (for example, one gene is annotated in Ensembl database as two separate genes). *A candidate fusion gene having this label has a high probability of being a false positive.* |
| **refseq\_fully\_overlapping** | the genes forming the fusion gene are fully overlapping according to RefSeq NCBI database. *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **refseq\_partially\_overlapping** | the genes forming the fusion gene are partially overlapping (on same strand or on different strands) according the RefSeq NCBI. *A candidate fusion gene having this label has a good probability of being a false positive.</i> </font> |
| **refseq\_same\_strand\_overlapping** | the genes forming the fusion gene are fully/partially overlapping and are both on the same strand according to RefSeq NCBI database. *A candidate fusion gene having this label has a very high probability of being a false positive (this is most likely and alternative splicing event).</i> </font> |
| **ribosomal**  | one or both gene is a gene encoding for [ribosomal protein](http://en.wikipedia.org/wiki/Ribosomal_protein) |
| **rrna**                | one or both genes is a [rRNA](http://en.wikipedia.org/wiki/Ribosomal_RNA).  *A candidate fusion gene having this label has a very high probability of being a false positive.*|
| **short\_distance**     | both genes are on the same strand and they are less than X bp apart, where X is set using the option '--dist-fusion' and by default it is 200 000 bp. *A candidate fusion gene having this label has a higher probability than expected of being a false positive.* |
| **similar\_reads**      | both genes have the same reads which map simultaneously on both of them (this is an indicator of how similar are the sequences of both genes; ideally this should be zero or as close to zero as possible for a real fusion). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **similar\_symbols**    | both genes have the same or very similar gene names (for example: RP11ADF.1 and RP11ADF.2). *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **snorna**              | one or both genes is a [snoRNA](http://en.wikipedia.org/wiki/Small_nucleolar_RNA) |
| **snrna**               | one or both genes is a [snRNA](http://en.wikipedia.org/wiki/Small_nuclear_RNA) |
| **tcga**                | known fusion gene from the [TCGA](https://tcga-data.nci.nih.gov/tcga/) database (please use Google for more information regarding the fusion gene) |
| **tcga-normal**                | known fusion gene from healthy samples from [TCGA](https://tcga-data.nci.nih.gov/tcga/) database (please use Google for more information regarding the fusion gene) |
| **tcga-cancer**                | known fusion gene from tumor samples from [TCGA](https://tcga-data.nci.nih.gov/tcga/) database (please use Google for more information regarding the fusion gene) |
| **tcga2**                | known fusion gene from the [TCGA](https://tcga-data.nci.nih.gov/tcga/) database (please use Google for more information regarding the fusion gene) |
| **tcga3**                | known fusion gene from the [TCGA](https://tcga-data.nci.nih.gov/tcga/) database (please use Google for more information regarding the fusion gene) |
| **ticdb**               | known fusion gene from the [TICdb](http://www.unav.es/genetica/TICdb/) database (please use TICdb database for more information regarding the fusion gene) |
| **trna**                | one or both genes is a [tRNA](http://en.wikipedia.org/wiki/Transfer_RNA) |
| **ucsc\_fully\_overlapping** | the genes forming the fusion gene are fully overlapping according to UCSC database. *A candidate fusion gene having this label has a very high probability of being a false positive.* |
| **ucsc\_partially\_overlapping** | the genes forming the fusion gene are partially overlapping (on same strand or on different strands) according the UCSC database.  *A candidate fusion gene having this label has a good probability of being a false positive.</i> </font> |
| **ucsc\_same\_strand\_overlapping** | the genes forming the fusion gene are fully/partially overlapping and are both on the same strand according to UCSC database. *A candidate fusion gene having this label has a very high probability of being a false positive (this is most likely and alternative splicing event).</i> </font> |
| **yrna**                | one or both genes is a [Y RNA](http://en.wikipedia.org/wiki/Y_RNA) |


## 6.3 - Visualization
*FusionCatcher* outputs also the zipped FASTA files containing the reads which support the found candidate fusions genes. The files are:
  * `supporting-reads_gene-fusions_BOWTIE.zip`,
  * `supporting-reads_gene-fusions_BLAT.zip`,
  * `supporting-reads_gene-fusions_STAR.zip`,
  * `supporting-reads_gene-fusions_BOWTIE2.zip`.

The reads which support the:
  * junction of the candidate fusion have their name ending with `_supports_fusion_junction`, and
  * candidate fusion (i.e. one reads map on one gene and the paired-read maps on the other fusion gene) have their name ending with `_supports_fusion_pair`.

These supporting reads (given as FASTA and FASTQ files) may be used for further visualization purposes. For example, one may use these supporting reads and align them himself/herself using his/her favourite:
  * aligner (e.g. `Bowtie/Bowtie2/TopHat/STAR/GSNAP/etc.`),
  * version/assembly of genome,
  * mapping format output (e.g. SAM/BAM), and
  * NGS visualizer (e.g. [IGV](http://www.broadinstitute.org/igv/)/[UCSC Genome Browser](http://genome.ucsc.edu/)/etc.)

### 6.3.1 - UCSC Genome Browser
For example, the sequences of supporting reads for a given candidate fusion gene may be visualized using [UCSC Genome Browser](http://genome.ucsc.edu/) by aligning them using the [UCSC Genome Browser](http://genome.ucsc.edu/)'s  BLAT aligner (i.e. copy and paste the reads here: [BLAT tool of UCSC Genome Browser](http://genome.ucsc.edu/cgi-bin/hgBlat?command=start) --> click the button **Submit** --> navigate into the [UCSC Genome Browser](http://genome.ucsc.edu/) to the genes that form the fusion genes). Also zooming out several times gives better view here.

### 6.3.2 - PSL format
If one uses the `--visualization-psl` command line option of the *FusionCatcher* then the BLAT alignment of the supporting reads will be done automatically by the *FusionCatcher* and the results are saved in [PSL](http://genome.ucsc.edu/FAQ/FAQformat.html#format2) format files with names that are ending with `_reads.psl` in the:
  * `supporting-reads_gene-fusions_BOWTIE.zip`,
  * `supporting-reads_gene-fusions_BLAT.zip`,
  * `supporting-reads_gene-fusions_STAR.zip`, and
  * `supporting-reads_gene-fusions_BOWTIE2.zip`.

The files with names ending in `_reads.psl` may be used further for visualization of the candidate fusion genes using [UCSC Genome Browser](http://genome.ucsc.edu/), [IGV (Integrative Genome Viewer)](http://www.broadinstitute.org/igv/) or any other viewer/browser which supports the [PSL](http://genome.ucsc.edu/FAQ/FAQformat.html#format2) format.

Note: If one generated the build files using `fusioncatcher-build.py` the command line `--visualization-psl` option should work just fine. If one **downloaded the build files** then the command line option `--visualization-psl` will not work an it needs to be enabled by creating manually first the file `fusioncatcher/data/current/genome.2bit` for FusionCatcher, something like this (here the assumption is that the build files for one's organism of interest are in `fusioncatcher/data/current/`):
```
# re-build the genome index using BLAT where the genome is given FASTA file genome.fa
fusioncatcher/tools/bowtie/bowtie-inspect fusioncatcher/data/current/genome_index/ > fusioncatcher/data/current/genome.fa
fusioncatcher/tools/blat/faToTwoBit fusioncatcher/data/current/genome.fa fusioncatcher/data/current/genome.2bit -noMask
```



### 6.3.3 - SAM format

#### 6.3.3.1 - Automatic method
If one uses the `--visualization-sam` command line option of the *FusionCatcher* then the BOWTIE2 alignment of the supporting reads will be done automatically by the *FusionCatcher* and the results are saved as [SAM](http://samtools.github.io/hts-specs/SAMv1.pdf) files with names that are ending with `_reads.sam` in the:
  * `supporting-reads_gene-fusions_BOWTIE.zip`,
  * `supporting-reads_gene-fusions_BLAT.zip`,
  * `supporting-reads_gene-fusions_STAR.zip`,
  * `supporting-reads_gene-fusions_BOWTIE2.zip`.

The files with names ending in `_reads.sam` (please note, that they still needed to be converted to BAM, coordiante sorted and indexed first) may be used further for visualization of the candidate fusion genes using [UCSC Genome Browser](http://genome.ucsc.edu/), [IGV (Integrative Genome Viewer)](http://www.broadinstitute.org/igv/) or any other viewer/browser which supports the [SAM](http://samtools.github.io/hts-specs/SAMv1.pdf) format.

#### 6.3.3.2 - Manual method
Here is an rough example of manually aligning the supporting reads (that is named as `supporting_reads.fq` in the below example; the FASTQ files needed here are the files ending in `_reads.fq` from the ZIP archives `supporting-reads_gene-fusions_*.zip` produced by *FusionCatcher*) using different aligners.
  * [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) aligner (where `your_choice_of_genome_bowtie2_index` may be for human, for example [this](ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/hg19.zip)):  
```
# alignment done ignoring the paired-end information (i.e. like single reads):

bowtie2 \
--local \
-k 10 \
-x your_choice_of_genome_bowtie2_index \
-U supporting_reads.fq \
-S fusion_genes.sam

samtools view -bS fusion_genes.sam | samtools sort - fusion_genes.sorted

samtools index fusion_genes.sorted.bam

# alignment done taking into account the paired-end information:

cat supporting_reads.fq | \
paste - - - - - - - - | \
awk '{print $1"\n"$2"\n"$3"\n"$4 > "r1.fq"; print $5"\n"$6"\n"$7"\n"$8 > "r2.fq"}'

bowtie2 \
--local \
-k 10 \
-x your_choice_of_genome_bowtie2_index \
-1 r1.fq \
-2 r2.fq \
-S fusion_genes.sam

samtools view -bS fusion_genes.sam | samtools sort - fusion_genes.sorted

samtools index fusion_genes.sorted.bam
```
  * [STAR](http://github.com/alexdobin/STAR) aligner (where `your_choice_of_genome_star_index` should be built according to the [STAR Manual](http://github.com/alexdobin/STAR/tree/master/doc))
```
# alignment done ignoring the paired-end information (i.e. like single reads):

STAR \
--genomeDir your_choice_of_genome_star_index \
--alignSJoverhangMin 9 \
--chimSegmentMin 17 \
--readFilesIn supporting_reads.fq \
--outFileNamePrefix .

samtools view -bS fusion_genes.sam | samtools sort - fusion_genes.sorted

samtools index fusion_genes.sorted.bam

# alignment done taking into account the paired-end information:

cat supporting_reads.fq | \
paste - - - - - - - - | \
awk '{print $1"\n"$2"\n"$3"\n"$4 > "r1.fq"; print $5"\n"$6"\n"$7"\n"$8 > "r2.fq"}'

STAR \
--genomeDir /your_choice_of_genome_star_index/ \
--alignSJoverhangMin 9 \
--chimSegmentMin 17 \
--readFilesIn r1.fq r2.fq\
--outFileNamePrefix .

samtools view -bS Aligned.out.sam | samtools sort - fusion_genes.sorted

samtools index fusion_genes.sorted.bam
```
  * [BLAT](http://users.soe.ucsc.edu/~kent/src/) aligner (where `your_choice_of_genome_blat_index` should be built according to the [BLAT's examples](https://genome.ucsc.edu/goldenpath/help/blatSpec.html))
```
# build the genome index using BLAT where the genome is given FASTA file genome.fa
faToTwoBit genome.fa genome.2bit -noMask


# align the supporting reads given by FusionCatcher (the FASTA 
# file for your fusion of interest can be found in ZIP files 
# generated as output by FusionCatcher, 
# e.g. EML4--ALK__42264951--29223528_reads.fa) using BLAT aligner
blat -stepSize=5 -repMatch=2253 -minScore=0 -minIdentity=0 genome.2bit supporting_reads.fa supporting_reads_mapped.psl 

# visualize the PSL file supporting_reads_mapped.pslin IGV or run psl2sam.pl to convert it into SAM format
psl2sam.pl supporting_reads_mapped.psl > supporting_reads_mapped.sam
```

Further, the files `fusion_genes.sorted.bam` and `fusion_genes.sorted.bam.bai` may be used with your favourite NGS visualizer!

### 6.3.4 - Chimera `R/BioConductor` package
For visualization of fusion genes found by *FusionCatcher* one may use also the `R/BioConductor` package [Chimera](http://www.bioconductor.org/packages/release/bioc/html/chimera.html), which supports *FusionCatcher*.

## 6.4 - Docker

Run *FusionCatcher* using Docker image, use the command::
```
docker run --rm fusioncatcher/docker fusioncatcher
```
In order to share a directory (for example: /data), use::
```
docker run --rm -v /data:/data fusioncatcher/docker fusioncatcher
```

## 6.5 - Examples

### 6.5.1 - Example 1

Here, is an example of how *FusionCatcher* can be used to search for fusion genes in human RNA-seq sample where:
  1. any distance at chromosomal level between the candidate fusion genes is acceptable, **and**
  1. the candidate fusion genes are allowed to be readthroughs (i.e. the genes forming a fusion gene maybe adjacent on the chromosome)
  1. the candidate fusion genes are not allowed to be less the 1000 bp apart on the same strand
  1. use two methods to find the fusion genes (i.e. use BOWTIE, BLAT, STAR, and BOWTIE2 aligners for mapping the reads and this allows to find the fusion genes even in the case that the annotation from Ensembl database is not entirely correct, like for example find a fusion junction even if it is in the middle of a exon or intron)
```
fusioncatcher \
-d /some/human/data/directory/ \
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/
```

### 6.5.2 - Example 2

Here, is an example of how *FusionCatcher* can be used to search for fusion genes in human RNA-seq sample where:
  1. any distance at chromosomal level between the candidate fusion genes is acceptable, **and**
  1. the candidate fusion genes are **not** allowed to be readthroughs (i.e. there is still at least one known gene situated one the same strand in between the genes which form the candidate fusion gene)
  1. the candidate fusion genes are not allowed to be less the 1000 bp apart on the same strand
  1. use only **one** method to find the fusion genes (i.e. use only BOWTIE aligner for mapping the reads and this allows to find the fusion genes only in the case that the annotation from Ensembl database is correct, like for example find a fusion junction only if it matches perfectly the known exon borders)
```
fusioncatcher \
-d /some/human/data/directory/ \
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/ \
--skip-readthroughs \
--skip-blat
```




---


# 7 - ALIGNERS

## 7.1 - Bowtie

By default, *FusionCatcher* its the Bowtie aligner for finding candidate fusion genes. This approach relies heavily on good is the annotation data for the given organism in the Ensembl database. If, for example, a gene is not annotated well and has several exons which are not annotated in the Ensembl database and if one of these exons is the one involved in the fusion point then this fusion gene will not be found by using only the Bowtie aligner. In order to find also the fusion genes where the the junction point is in the middle of exons or introns, `*FusionCatcher*` is using by default the BLAT, and STAR aligners in addition to Bowtie aligner. The command line options '`--skip-blat`','`--skip-star`', or '`--skip-bowtie2`' should be used in order to specify what aligners should not be used. The command line option '`--aligners`' specifies which aligners should be used by default. For example, '`--aligners=blat,star,bowtie2`' forces *FusionCatcher* too use all aligners for finding fusion genes

## 7.2 - Bowtie and Blat

The use of Bowtie and Blat aligners is the **default** approach of *FusionCatcher* for finding fusion genes.

In order not to use this approach the command line option '`--skip-blat`' should be added (or remove the string `blat` from line `aligners` from file `fusioncatcher/etc/configuration.cfg`), as following:

```
fusioncatcher \
-d /some/human/data/directory/ \ 
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/ \
--skip-blat
```

Please, read the license of Blat aligner before using this approach in order to see if you may use Blat! *FusionCatcher* will use Blat aligner when using this approach!

## 7.3 - Bowtie and STAR

The use of Bowtie and STAR aligners is the **default** approach of *FusionCatcher* for finding fusion genes.

In order not to use this approach the command line option '`--skip-star`' should be added, as following:

```
fusioncatcher \
-d /some/human/data/directory/ \ 
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/ \
--skip-star
```

## 7.4 - Bowtie and Bowtie2

The use of Bowtie and Bowtie2 aligners is **not** the **default** approach of *FusionCatcher* for finding fusion genes.

In order not to use this approach the command line option '`--skip-bowtie2`' should be added, as following:

```
fusioncatcher \
-d /some/human/data/directory/ \ 
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/ \
--skip-bowtie2
```

In order to use this approach the command line option '`--aligners`' should contain the string '`bowtie2`', like for example

```
fusioncatcher \
-d /some/human/data/directory/ \ 
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/ \
--aligners blat,star,bowtie2
```

## 7.5 - Bowtie2

The use of Bowtie2 aligner is **not** the **default** approach of *FusionCatcher* for finding fusion genes.

In order not to use this approach the command line option '`--skip-bowtie2`' should be added, as following:

```
fusioncatcher \
-d /some/human/data/directory/ \ 
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/ \
--skip-bowtie2
```

---
# 8 - Command line options

## fusioncatcher
It searchers for fusion genes and/or translocations in RNA-seq data (paired-end reads FASTQ files produced by Illumina next-generation sequencing platforms like Illumina Solexa and Illumina `HiSeq`) in diseased samples. Its command line is:
```
fusioncatcher [options]
```
and the command line options are:
```
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILENAME, --input=INPUT_FILENAME
                        The input file(s) or directory. The files should be in
                        FASTQ or SRA format and may be or not compressed using
                        gzip or zip. A list of files can be specified by given
                        the filenames separated by comma. If a directory is
                        given then it will analyze all the files found with
                        the following extensions: .sra, .fastq, .fastq.zip,
                        .fastq.gz, .fastq.bz2, fastq.xz, .fq, .fq.zip, .fq.gz,
                        .fq.bz2, fz.xz, .txt, .txt.zip, .txt.gz, .txt.bz2 .
  --batch               If this is used then batch mode is used and the input
                        specified using '--input' or '-i' is: (i) a tab-
                        separated text file containing a each line such that
                        there is one sample per line and first column are the
                        FASTQ files' full pathnames/URLs, separated by commas,
                        corresponding to the sample and an optional second
                        column containing the name for the sample, or (ii) a
                        input directory which contains a several
                        subdirectories such that each subdirectory corresponds
                        to only one sample and it contains all the FASTQ files
                        corresponding to that sample. This is useful when
                        several samples needs to be analyzed.
  --single-end          If this is used then it is assumed that all the input
                        reads are single-end reads which must be longer than
                        130 bp. Be default it is assumed that all input reads
                        come from a paired-end reads.
  -I NORMAL_MATCHED_FILENAME, --normal=NORMAL_MATCHED_FILENAME
                        The input file(s) or directory containing the healthy
                        normal-matched data. They should be given in the same
                        format as for '--input'. In case that this option is
                        used then the files/directory given to '--input' is
                        considered to be from the sample of a patient with
                        disease. This is optional.
  -o OUTPUT_DIRECTORY, --output=OUTPUT_DIRECTORY
                        The output directory where all the output files
                        containing information about the found candidate
                        fusiongenes are written. Default is 'none'.
  -d DATA_DIRECTORY, --data=DATA_DIRECTORY
                        The data directory where all the annotations files
                        from Ensembl database are placed, e.g. 'data/'. This
                        directory should be built using 'fusioncatcher-build'.
                        If it is not used then it is read from configuration
                        file specified with '--config' from 'data = ...' line.
  -T TMP_DIRECTORY, --tmp=TMP_DIRECTORY
                        The temporary directory where all the outputs files
                        and directories will be written. Default is directory
                        'tmp' in the output directory specified with '--
                        output'.
  -p PROCESSES, --threads=PROCESSES
                        Number or processes/threads to be used for running
                        SORT, Bowtie, BLAT, STAR, BOWTIE2 and other
                        tools/programs. If it is 0 (as it is by default) then
                        the number of processes/threads will be read first
                        from 'fusioncatcher/etc/configuration.cfg' file. If
                        even there it is still set to 0 then 'min(number-of-
                        CPUs-found,16)' processes will be used. Setting number
                        of threads in 'fusioncatcher/etc/configuration.cfg'
                        might be usefull in situations where one server is
                        shared between several users and in order to limit
                        FusionCatcher using all the CPUs/resources.Default is
                        '0'.
  --config=CONFIGURATION_FILENAME
                        Configuration file containing the paths to external
                        tools (e.g. Bowtie, Blat, fastq-dump.) in case that
                        they are not specified in PATH variable! Default is '/
                        apps/fusioncatcher/etc/configuration.cfg,/apps/fusionc
                        atcher/bin/configuration.cfg'.
  -z, --skip-update-check
                        Skips the automatic routine that contacts the
                        FusionCatcher server to check for a more recent
                        version. Default is 'False'.
  -V, --keep-viruses-alignments
                        If it is set then the SAM alignments files of reads
                        mapping on viruses genomes are saved in the output
                        directory for later inspection by the user. Default is
                        'False'.
  -U, --keep-unmapped-reads
                        If it is set then the FASTQ files, containing the
                        unmapped reads (i.e. reads which do not map on genome
                        and transcriptome), are saved in the output directory
                        for later inspection by the user. Default is 'False'.
  --aligners=ALIGNERS   The aligners to be used on Bowtie aligner. By default
                        always BOWTIE aligner is used and it cannot be
                        disabled. The choices are:
                        ['blat','star','bowtie2']. Any combination of
                        these is accepted if the aligners' names are comma
                        separated. For example, if one wants to used all four
                        aligners then 'blat,star,bowtie2' should be given.
                        The command line options '--skip-blat', '--skip-star',
                        and '--skip-bowtie2' have priority over this option.
                        If the first element in the list is the configuration
                        file (that is '.cfg' file) of FusionCatcher then the
                        aligners specified in the list of aligners specified
                        in the configuration file will be used (and the rest
                        of aligner specified here will be ignored). In case
                        that the configuration file is not found then the
                        following aligners from the list will be used. Default
                        is
                        '/apps/fusioncatcher/etc/configuration.cfg,blat,star'.
  --skip-blat           If it is set then the pipeline will NOT use the BLAT
                        aligner and all options and methods which make use of
                        BLAT will be disabled. BLAT aligner is used by
                        default. Please, note that BLAT license does not allow
                        BLAT to be used for commercial activities. Fore more
                        information regarding BLAT please see its license:
                        <http://users.soe.ucsc.edu/~kent/src/>. Default is
                        'False'.
  --skip-star           If it is set then the pipeline will NOT use the STAR
                        aligner and all options and methods which make use of
                        STAR will be disabled. STAR aligner is used by
                        default. Default is 'False'.
  --sort-buffer-size=SORT_BUFFER_SIZE
                        It specifies the buffer size for command SORT. Default
                        is '80%' if less than 32GB installed RAM else is set 
                        to 26 GB.
  --start=START_STEP    It re-starts executing the workflow/pipeline from the
                        given step number. This can be used when the pipeline
                        has crashed/stopped and one wants to re-run it from
                        from the step where it stopped without re-running from
                        the beginning the entire pipeline. 0 is for restarting
                        automatically and 1 is the first step. Default is '0'.


```

## fusioncatcher-build
It downloads the necessary data for a given organism from the Ensembl database and it builds the necessary files/indexes which are needed to running *FusionCatcher*. Its command line is:
```
fusioncatcher-build [options]
```
and the command line options are:
```
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o OUTPUT_DIRECTORY, --output=OUTPUT_DIRECTORY
                        The output directory where all the outputs files  and
                        directories will be written.
  -c CONFIGURATION_FILENAME, --config=CONFIGURATION_FILENAME
                        Configuration file containing the paths to external
                        tools (e.g. Bowtie, etc.) in case that they are not in
                        PATH! Default is '/apps/fusioncatcher/bin/../etc/confi
                        guration.cfg,/apps/fusioncatcher/bin/configuration.cfg
                        '.
  -g ORGANISM, --organism=ORGANISM
                        Organism for which the data is downloaded from Ensembl
                        database and built, for example: 'homo_sapiens',
                        'mus_musculus', 'rattus_norvegicus',
                        'canis_familiaris', etc. Default is 'homo_sapiens'.
  -w WEB_ENSEMBL, --web=WEB_ENSEMBL
                        Ensembl database web site from where the data is
                        downloaded.  e.g. 'www.ensembl.org',
                        'uswest.ensembl.org', 'useast.ensembl.org',
                        'asia.ensembl.org', etc. Default is 'www.ensembl.org'.
  -e FTP_ENSEMBL, --ftp-ensembl=FTP_ENSEMBL
                        Ensembl database FTP site from where the data is
                        downloaded. Default is 'ftp.ensembl.org'.
  --ftp-ensembl-path=FTP_ENSEMBL_PATH
                        The path for Ensembl database FTP site from where the
                        data is downloaded.
  -x FTP_UCSC, --ftp-ucsc=FTP_UCSC
                        UCSC database FTP site from where the data is
                        downloaded. Default is 'hgdownload.cse.ucsc.edu'.
  -n FTP_NCBI, --ftp-ncbi=FTP_NCBI
                        NCBI database FTP site from where the data is
                        downloaded. Default is 'ftp.ncbi.nlm.nih.gov'.
  --skip-blat           If it is set then the pipeline will NOT use the BLAT
                        aligner and all options and methods which make use of
                        BLAT will be disabled. BLAT aligner is used by
                        default. Please, note that BLAT license does not allow
                        BLAT to be used for commercial activities. Fore more
                        information regarding BLAT please see its license:
                        <http://users.soe.ucsc.edu/~kent/src/>. Default is
                        'False'.
  --enlarge-genes       If it is set then the genes are enlarged (i.e. their
                        introns include also in the transcriptome). Default is
                        'False'.
  -p PROCESSES, --threads=PROCESSES
                        Number or processes/threads to be used. Default is
                        '0'.
  --skip-database=SKIP_DATABASE
                        If it is set then the pipeline will skip the specified
                        database(s). The choices are ['cosmic','conjoing','chi
                        merdb2','ticdb','cgp','cacg']. If several databases
                        should be skipped, then their names shall be separated
                        by comma. Default is ''.
  -s START_STEP, --start=START_STEP
                        It starts executing the workflow from the given step
                        number. This can be used when the pipeline has
                        crashed/stopped and one wants to re-run it from from
                        the step where it stopped without re-running from the
                        beginning the entire pipeline. 0 is for restarting
                        automatically and 1 is the first step. This is
                        intended to be used for debugging. Default is '0'.
  -l HASH, --hash=HASH  Hash to be used for computing checksum. The choices
                        are ['no','crc32','md5','adler32','sha512','sha256'].
                        If it is set up to 'no' then no checksum is used and
                        the entire pipeline is executed as a normal shell
                        script. For more information see 'hash_library' in
                        'workflow.py'. This is intended to be used for
                        debugging. Default is 'no'.
  -k, --keep            Preserve intermediate files produced during the run.
                        By default, they are NOT deleted upon exit. This is
                        intended to be used for debugging. Default value is
                        'False'.
  -u CHECKSUMS_FILENAME, --checksums=CHECKSUMS_FILENAME
                        The name of the checksums file. This is intended to be
                        used for debugging. Default value is 'checksums.txt'.

```


---

# 9 - Methods

The main goal of *FusionCatcher* is to find **somatic** (and/or pathogenic) fusion genes in RNA-seq data.

*FusionCatcher* is doing its own quality filtering/trimming of reads. This is needed because most a very important factor for finding fusion genes in RNA-seq experiment is the length of RNA fragments.  **Ideally** the RNA fragment size for finding fusion genes should be over 300 bp.  Most of the RNA-seq experiments are designed for doing differentially expression analyses and not for finding fusion genes and therefore the RNA fragment size many times is less than 300bp and the trimming and quality filtering should be done in such a way that it does not decrease even more the RNA fragment size.

*FusionCatcher* is able to find fusion genes even in cases where the fusion junction is within known exon or within known intron (for example in the middle of an intron). The minimum condition for *FusionCatcher* to find a fusion gene is that both genes involved in the fusion are annotated in Ensembl database (even if their gene structure is not correct).

*FusionCatcher* is spending most of computational analysis on the most promising fusion genes candidate and tries as early as possible to filter out the candidate fusion genes which do not look promising, like for example:
  * candidate fusion gene is composed of a gene and its pseudogene, or
  * candidate fusion gene is composed of a gene and its paralog gene, or
  * candidate fusion gene is composed of a gene and a miRNA gene (but a gene which contains miRNA genes are not skipped), or
  * candidate fusion gene is composed of two genes which have a very sequence similarity (i.e. *FusionCatcher* is computing its homology score), or
  * candidate fusion gene is known to be found in samples from healthy persons (using the 16 organs RNA-seq data from the Illumina BodyMap2), or
  * candidate fusion gene is in one of the known databases of fusion genes found in healthy persons, i.e. ChimerDB2, CACG, and ConjoinG.

*FusionCatcher* is using by default three aligners for mapping the reads. The aligners are Bowtie, BLAT, and STAR. STAR is used here only and only for "splitting" the reads while aligning them.


---

# 10 - Comparisons to other tools
When performing comparisons where *FusionCatcher* is compared with other gene fusions finder we **always recommend strongly to use the default/recommended parameters** for *FusionCatcher* and also to use the raw FASTQ files which came directly from the Illumina sequencer.


The performance of *FusionCatcher* is decreased drastically, when using other parameters than the default/recommended ones! Especially **do not change** the defaults for: `--5keep`, `--anchor-fusion`, `--reads-fusion`, `--pairs-fusion`, `--pairs-fusion2`! The default parameters should work just fine for input reads which have the size range between 35 bp to 250 bp.


Also, when comparing the fusion genes found by *FusionCatcher* with fusion genes found by other tools one needs to keep in mind that *FusionCatcher* is a **SOMATIC** fusion gene finder and **NOT** a (general) fusion gene finder. This means that if a fusion gene is already known to exist in healthy individuals (from public literature or from our internal RNA-seq database of healthy sample) then that fusion gene will be skipped by *FusionCatcher* and it will not be reported at all! An example is the well known fusion gene TTTY15-USP9Y which is known to be found in healthy individuals (see [here](http://www.sciencedirect.com/science/article/pii/S0002944015001996)) and which *FusionCatcher* will skip it and will not report it on purpose because **it is not a somatic fusion gene**!

Also, when one is running *FusionCatcher* on some synthetic/simulated RNA-seq datasets which contain a set of random/ad-hoc fusion genes which are created randomly and without any biological support (for example, that fusion gene has never been reported in the literature to exist in a diseased patient), there most likely *FusionCatcher* will detect that these **random/ad-hoc** fusion genes are not fitting the already known biological knowledge (e.g. ad-hoc/random fusion gene might have been reported already to exist in healthy patients, or ad-hoc/random fusion is between a gene its paralog/homolog/pseudogene) and will skip them and will not report them even if it finds them. Therefore we strongly recommend not to run *FusionCatcher* on synthetic/simulated RNA-seq dataset which are known to contain fusion genes which are **not** somatic fusion genes. Also, we strongly recommend not to run *FusionCatcher* on downsampled input datasets, like for example, choosing randomly 30 million reads from an original datasets with 60 million reads. *FusionCatcher* has been specifically built for analyzing real input RNA-seq datasets which come directly from the sequencing machine.



---

# 11 - License
*FusionCatcher*'s code is released under [GNU GPL version 3 license](http://www.gnu.org/copyleft/gpl.html). *FusionCatcher* is using third-party tools and databases. The user is responsible to obtain licenses for the third-party tools and databases which are used by *FusionCatcher*.

**Most** (but not all) of the third-party tools and databases used by *FusionCatcher* are (i) free to use, or (ii) are released under GPL/MIT-type licenses. The most notable exception here of which we are aware is BLAT's aligner license, which requires one to buy a license when BLAT is used in commercial environment (please, see for more [here](http://www.kentinformatics.com/contact-us.html)). In case that one does not wish to use BLAT aligner then it is still possible to use *FusionCatcher* for finding fusion genes, by telling *FusionCatcher* not to use BLAT aligner but instead to use the BOWTIE2 aligner (BLAT is used by default and BOWTIE2 is not used by default), as following:

```
/apps/fusioncatcher/bin/fusioncatcher \
--aligners star,bowtie2
```



---

# 12 - Citing
If you use *FusionCatcher*, please cite:

D. Nicorici, M. Satalan, H. Edgren, S. Kangaspeska, A. Murumagi, O. Kallioniemi, S. Virtanen, O. Kilkku, **FusionCatcher – a tool for finding somatic fusion genes in paired-end RNA-sequencing data**, bioRxiv, Nov. 2014, [DOI:10.1101/011650](http://biorxiv.org/content/early/2014/11/19/011650)


---

# 13 - Reporting Bugs

Please, when reporting bugs include also the following files:
  * "fusioncatcher.log" (this contains just a list of the commands executed by *FusionCatcher*), and
  * "info.txt" (this contains info: regarding the version of *FusionCatcher* and tools used, statistics about input FASTQ files, counts of found reads, etc.)
which were generated by *FusionCatcher* during the run.

**NOTE**: Giving only step number where the error has appeared is not enough because the step numbers depend on the input type (e.g. raw FASTQ file, ZIP compressed FASTQ file, SRA file, etc.) and command line options used to run *FusionCatcher* (e.g. some command line option skip some steps). The step numbers are used by *FusionCatcher* for being able to re-start from the last step which was executed successfully last time in case that last time the run ended prematurely due to reasons which didn't depend on *FusionCatcher* (e.g. server crashed).


---

# NOTES
  * <font color='red'>The performance of <b>FusionCatcher</b> is decreased drastically, when using other parameters than the default/recommended ones! Especially <b>do not change</b> the defaults for: <code>--5keep, --anchor-fusion, --reads-fusion, --pairs-fusion, --pairs-fusion2</code>! The default parameters should work just fine for input reads which have the size range between 35 bp to 250 bp.</font>
  * * <font color='red'>The performance of <b>FusionCatcher</b> is decreased drastically, when running <b>FusionCatcher</b> on a subset of the reads. It is not recommended to run <b>FusionCatcher</b> on 20 million paired-reads sampled from a sample. All the reads from the sample shall be given as input to <b>FusionCatcher</b></font>
  * `fusioncatcher-build` takes several hours to run and it depends on the local internet connection speed. It needs to be run only once!
  * *FusionCatcher* can be run many times using the same data produced by the `fusioncatcher-build`;
  * Ensembl version 98 was found to work fine with *FusionCatcher* as November 2019;
  * *FusionCatcher* and `fusioncatcher-build` restart automatically from the point where have been interrupted at the previous run.
  * *FusionCatcher* by default is focusing on finding fusion genes specific to diseased/tumor/cancer samples. That means that *FusionCatcher* will skip the fusion genes which are already known to exist in healthy samples. If one wishes to find fusion genes in healthy samples then we suggest other fusion finders to be used.
  * *FusionCatcher* is able to find fusion genes **also** without using BLAT aligner but in this case we recommend to user BOWTIE2 aligner (which is not used by default) also in order to compensate!






