#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
from numpy import *
import re
import os
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
def usage():
    test="name"
    message='''
python Rectify_gff.py --insertion svState_Insertion/HEG4.insertion.SV.gff --deletion svState_Deletion/HEG4.deletion.SV.gff
Parse rectified gff file, create new gff for insertion and deletion with that with ancestor state rectified.
For insertion.gff, we only keep these ancestor state of insertion. If ancestor state is deletion, which mean the deletion occurs in reference genome.
For deletion.gff, we only keep these ancestor state of deletion. If ancestor state is insertion, which mean the insertion occurs in reference genome.
    '''
    print message


'''
Chr1	SV	Insertion	2433412	2433412	.	.	.	AncestralState "Insertion"; INDEL=Insertio "INDEL=Insertion"; Method=soaps "Method=soapsv"; Rect "1:0"; Seq=ACCCAAAGTTTATAAGTCAAAAGTTTACATACCCGTTTCAAATTTGAATTTGAATTCAAATATTAGTTTATA "Seq=ACCCAAAGTTTATAAGTCAAAAGTTTACATACCCGTTTCAAATTTGAATTTGAATTCAAATATTAGTTTATAG"; Size=7 "Size=73"
'''
'''
Chr1	SVpipe	Deletion	80013	80066	.	.	.	Size=54;Method=soapsv;INDEL=Deletion;Seq=CTATGTGGTTTTGGAGGCTCGCCAGCGATCGGCCACACATAGCGGCGACCATGC;
'''
def Parsegff(gff, prefix, indeltype):
    s = re.compile(r'AncestralState \"(\w+?)\";.*\"(Method=\w+?)\";.*\"(Seq=\w+?)\";.*\"(Size=\d+)\"')
    indelfile = open (prefix + '.' + indeltype + '.SV.gff', 'w')
    with open (gff, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2:
                unit = re.split(r'\t',line)
                m = s.search(unit[8])
                if m:
                    #print line
                    indel = m.groups(0)[0]
                    method = m.groups(0)[1]
                    seq    = m.groups(0)[2]
                    size   = m.groups(0)[3]
                    unit[2]=indel
                    unit[8]='%s;%s;INDEL=%s;%s;' %(size, method, indel, seq)
                    record = '\t'.join(unit)
                    if indel == indeltype:
                        print >> indelfile, record
                
    indelfile.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--insertion')
    parser.add_argument('-d', '--deletion')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.insertion) > 0
    except:
        usage()
        sys.exit(2)
     
    if args.output is None:
        args.output = 'HEG4.rectify'
    
    Parsegff(args.deletion, args.output, 'Deletion')
    Parsegff(args.insertion, args.output, 'Insertion')

if __name__ == '__main__':
    main()

