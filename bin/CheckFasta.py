#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
from numpy import *
import re
import os
import argparse
from Bio import SeqIO

def usage():
    test="name"
    message='''
Python CheckFasta.py --input ./svState_Insertion_top/HEG4.insertion.SV
Input is prefix ./svState_Insertion_top/HEG4.insertion.SV, then three fasta file will be ./svState_Insertion_top/HEG4.insertion.SV.A.fa and ./svState_Insertion_top/HEG4.insertion.SV.B.fa and ./svState_Insertion_top/HEG4.insertion.SV.C.fa. Check for fasta has NN and remove then from all three file.
    '''
    print message

def kickoutbadseq(fain, faout, badseq):
    ofile = open(faout, 'w')
    for record in SeqIO.parse(fain, "fasta"):
        if not badseq.has_key(record.id):
            SeqIO.write(record, ofile, "fasta")
    ofile.close()
    
def checkN(fasta):
    data = defaultdict(lambda: int)
    s = re.compile(r'N{10,}')
    for record in SeqIO.parse(fasta, "fasta"):
        if str(record.seq.upper()).startswith('N') or s.search(str(record.seq.upper())):
            data[record.id] = 1
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)
    
    badseq = defaultdict(lambda: int)
    for word in ('A', 'B', 'C'):
        fa = args.input + '.' + word + '.fa'
        nseq = checkN(fa)
        for seq in nseq.keys():
            badseq[seq] = 1
            print word, seq

    for word in ('A', 'B', 'C'):
        fain   = args.input + '.' + word + '.fa'
        faout  = args.input + '.' + word + '.clean.fa'
        kickoutbadseq(fain, faout, badseq)
    
    
if __name__ == '__main__':
    main()

