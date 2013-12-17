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
python Net_ChrName.py --input chain_net/MSU7_OPU.all_net_level1/net.level
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

'''
net Chr1 43270923
 fill 1126 1189 Opunc_chr1 + 20617668 1143 id 34565 score 67229 ali 1106 qDup 98 type top
  gap 1663 27 Opunc_chr1 + 20618211 0
 fill 2450 58 Opunc_chr3 - 15013485 58 id 177783 score 2629 ali 58 qDup 58 type top
 fill 2531 398 Opunc_chr2 + 6129140 425 id 144837 score 22808 ali 351 qDup 373 type top
'''
def rename(infile):
    data = defaultdict(str)
    s = re.compile(r'^net')
    s1 = re.compile(r'^(\s+)(.*)')
    s2 = re.compile(r'(\d+)')
    ofile = open (infile + '.rename' ,'w')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if s.search(line):
                print >> ofile, line
            else:
                m1 = s1.search(line)
                if m1:
                    space = m1.groups(0)[0]
                    left  = m1.groups(0)[1]
                    unit = re.split(r' ',left)
                    m2   = s2.search(unit[3])
                    chrn = 'Chr' + m2.groups(0)[0].zfill(1)
                    unit[3] = chrn
                    newline = ' '.join(unit)
                    print >> ofile, '%s%s' % (space, newline)
                    #print >> ofile, '>%s%s' % (space, left)
                    #print >> ofile, '%s\t%s\t%s\t%s' % (unit[0], unit[1], unit[2], chrn)


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

    rename(args.input)

if __name__ == '__main__':
    main()

