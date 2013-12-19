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
python Iseq.py --gff
Get Insertion sequence in SV gff file
GFF:
Chr1    SVpipe  Deletion        1045592 1045658 .       .       .       Size=67;Method=pindel;INDEL=Deletion;Seq=TCAATCATTGGTACTCTTAATGGAAATTTAACACAAGCTCTATCCTTACAGAAAATTTCTTGATGTA;

FNA:
>Chr1:1045592-1045658:SVpipe
TCAATCATTGGTACTCTTAATGGAAATTTAACACAAGCTCTATCCTTACAGAAAATTTCTTGATGTA

    '''
    print message


'''
Chr1	SVpipe	Deletion	1045592	1045658	.	.	.	Size=67;Method=pindel;INDEL=Deletion;Seq=TCAATCATTGGTACTCTTAATGGAAATTTAACACAAGCTCTATCCTTACAGAAAATTTCTTGATGTA;
'''
def Iseq(gff, fna):
    s = re.compile(r'Seq=(.*?);')
    ofile = open (fna, 'w+')
    with open (gff, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2:
                unit = re.split(r'\t',line)
                m = s.search(unit[8])
                if m:
                    #print line
                    seq   = m.groups(0)[0]
                    seqid = '%s:%s-%s:%s' % (unit[0], unit[3], unit[4], unit[1])
                    newrecord = SeqRecord(Seq(seq),id=seqid,description="")
	    	    SeqIO.write(newrecord,ofile,"fasta")
                
    ofile.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gff')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.gff) > 0
    except:
        usage()
        sys.exit(2)

    fna = os.path.splitext(args.gff)[0] + '.fna'
    Iseq(args.gff, fna)

if __name__ == '__main__':
    main()

