#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It is add on for blat_parallel.py by pre-filtering the fusion candidates.

Date: January 24, 2014.



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

This file is executing BLAT.

"""
import sys
import os
import gc



def myfilter(txt):
    r = False
    lin = txt.rstrip('\r\n').split('\t')
    if ( lin and
        (float(lin[0])/float(lin[10])) >= 0.70 and  # number of matches / length of query sequence
        lin[17] == '2' and  # blockCount
        lin[6] == '1' and   # number inserts in target = tNumInserts
        (lin[4] == '0' or (lin[4] == '1' and int(lin[5]) <= 3)) and  # number inserts in query
        min(map(int,lin[18][:-1].split(','))) > 9  # blockSizes
        ):
        r = True
    return r



if __name__ == '__main__':

    #command line parsing
    # initializing
    # reading command line arguments
    filenames = sys.argv

    if len(filenames)>1:
        infile = filenames[1]
        outfile = filenames[2]
    else:
        print >>sys.stderr,"It is add on for blat_parallel.py by pre-filtering the fusion candidates from an input PSL file format generated by BLAT aligner."
        print >>sys.stderr,"ERROR: Not enough arguments!"
        sys.exit(1)

    fid = None
    if infile == "-":
        fid = sys.stdin
    else:
        fid = open(infile,'r')

    fod = None
    if outfile == "-":
        fod = sys.stdout
    else:
        fod = open(outfile,'w')


    # processing
    flag = True
    if os.path.exists(infile) or infile == '-':
        fid = open(infile,'r')
        while True:
            lines = fid.readlines(10**8)
            if not lines:
                break
            gc.disable()
            lines = [line for line in lines if myfilter(line)]
            gc.enable()
            if lines:
                if not lines[-1].endswith('\n'):
                    lines[-1] = lines[-1]+'\n'
                fod.writelines(lines)
                flag = False
    if outfile != '-' and flag:
        fod.write('')
    fid.close()
    fod.close()

    #
