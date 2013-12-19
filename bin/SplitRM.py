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
python SplitRM.py --RM /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/input/mask/MSU_r7.fa.RepeatMasker.out
Split repeatmasker out file by chromosome
    '''
    print message


def splitRM(rm, output):
    s = re.compile(r'(\s*)(.*)')
        
    header = ''
    with open (rm,'r') as rmfh:
        for i in range(3):
            line = rmfh.readline()
            header = header + line
    header = header.rstrip()

    filehd = {}
    for i in range(1,13):
        filehd['Chr' + str(i)] = open (output + '/Chr'+ str(i) + '.fa.out', 'w')
        print >> filehd['Chr' + str(i)], header   
        print >> filehd['Chr' + str(i)], ''

    s1 = re.compile(r'^\s*\d+')
    temp = defaultdict(str)
    with open (rm,'r') as rmfh: 
        for line in rmfh:
            if not s1.search(line) or len(line) < 2:
                continue
            line = line.rstrip()
            space = '' 
            left  = ''
            m = s.search(line)
            if (m):
                space = m.groups(0)[0]
                left  = m.groups(0)[1]
            unit = re.split(r'\s+',left)
            temp[unit[4]] = '1'
            print >> filehd[unit[4]], line
    for fh in filehd.values():
        fh.close()
    
    for i in temp.keys():
        print i
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-R', '--RM')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.RM) > 0
    except:
        usage()
        sys.exit(2)

    if args.output is None:
        args.output = 'MSU7_masked'
    
    os.system('mkdir ' + args.output)
    splitRM(args.RM, args.output)

if __name__ == '__main__':
    main()

